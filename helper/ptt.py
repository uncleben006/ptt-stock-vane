import psycopg2
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import json
from config import database_url

class crawlerPtt():

    def __init__(self, url, date_limit):
        # TODO: 台股字典目前為手動匯入，新上市公司有可能不會被判斷到，之後要做自動化
        # 載入台股字典，作為篩選以及分析留言依據
        with open( 'data/company_dict.json', 'r' ) as read_file:
            self.dict_data = json.load( read_file )

        # 欲抓取的看板首頁
        self.url = url
        # 儲存每個標題網址
        self.urlList = []

        # 爬取今天之前的天數 ( date_limit )
        today = datetime.today()
        self.crawl_start = today - timedelta( days = date_limit )
        self.crawl_start = self.crawl_start.strftime( "%Y-%m-%d" )
        # 把時間區間做成時間陣列
        date_list = [(today - timedelta( days = x )).strftime( "%Y-%m-%d" ) for x in range( date_limit )]

        # 用 stock.json 初始化留言字典，字典格式如下
        # {
        #   '2020-07-07': { '8409': [], '2498': ['這檔未來也是概念股', '消息滿天飛 實際營收看不到 去年還在虧'... ] },
        #   '2020-07-08': { '4760': ['還早', '母公司超爛'], '6204': []... },
        # }
        self.messageDict = {}
        for date in date_list:
            self.messageDict[date] = {}
            for key in self.dict_data:
                self.messageDict[date][key] = []

        # 抓取首頁
        self.get_all_href(url=self.url)

        # 往前幾頁 抓取所有標題網址
        while True:
            try:
                r = requests.get(self.url)
                soup = BeautifulSoup(r.text, "html.parser")
                btn = soup.select('div.btn-group > a')
                # 抓取上一頁按鈕的網址
                up_page_href = btn[3]['href']
                # 在網址後加上上一頁的網址
                next_page_url = 'https://www.ptt.cc' + up_page_href
                # 爬取上一頁內容 並更新 url 成上一頁的網址
                self.url = next_page_url
                # 當爬到的時間與輸入的 crawl_start 重複，get_all_href 回傳 false，迴圈停止
                judge = self.get_all_href(url=self.url)
                if judge == False:
                    break
            except Exception as e:
                print(e)
                continue

        # 透過標題網址self.urlList抓取留言 並儲存到self.messageDict 最後再存下來 (邊抓邊存會漏掉很多留言)
        self.crawlerMessage()

    # 抓取標題網址，並將 title, url, date 存至 self.urlList
    def get_all_href(self,url):
        r = requests.get(url)
        soup = BeautifulSoup(r.text, "html.parser")

        # 抓取文章區塊
        results = soup.select("div.r-ent")
        for item in results:
            a_item = item.select_one("div.title").select_one("a")
            date = item.select_one("div.meta").select_one("div.date").text
            title = item.select_one("div.title").text
            # 把 date 變成 "%Y-%m-%d"
            date = self.format_datetime( date )
            # 爬到 crawl_start 就停止
            if str(date) == str(self.crawl_start):
                return False

            if a_item:
                #所要儲存的網站網址
                url = 'https://www.ptt.cc' + a_item.get('href')
                print(title,url,date)

                if url == 'https://www.ptt.cc/bbs/Stock/M.1422199105.A.84E.html':
                    break

                # 將 title, url, date 存至佇列
                self.urlList.append([url,title,date])

    # 對 ptt 抓到的時間做字串處理，因為其格式與 datetime 不相符
    def format_datetime( self, date ):
        if len( date.strip() ) < 5:
            date = '2020/0' + date.strip()
        else:
            date = '2020/' + date.strip()
        date = datetime.strptime( date, "%Y/%m/%d" ).strftime( "%Y-%m-%d" )
        return date

    # 從標題網址分析留言
    def crawlerMessage(self):

        for num in range(len(self.urlList)):
            # 找尋留言
            try:
                response = requests.get(self.urlList[num][0])
                soup = BeautifulSoup(response.text, 'html.parser')
                articles = soup.find_all('div', 'push')
                title = self.urlList[num][1]
                date = self.urlList[num][2]
            except Exception as e:
                print(e)
                continue

            print(self.urlList[num][0],self.urlList[num][1],self.urlList[num][2])

            # 如果 title 裡面有提及公司，則判斷該篇文章裡面所有的留言都指稱該公司
            referCompany = None
            for key in self.dict_data:
                for company in self.dict_data[key]:
                    # 這裡有一些資料不能用 title 來看，要打散出去
                    # 例如：2020，這個字串在 title 出現不是表示股票代號，而是指涉今年
                    if title.find( company ) != -1 and title.find('2020') == -1:
                        referCompany = self.dict_data[key][0]
                        break

            # 如果 title 有 referCompany 的話就把留言都指定給該 referCompany
            # 如果沒有則逐個留言尋找是否有批配的公司並指定給 referCompany
            if referCompany:
                for article in articles:
                    messages = article.find('span', 'f3 push-content')
                    # 如果留言裡面有資料 (有些留言過大被屏蔽會造成錯誤)
                    if messages:
                        # 去除掉冒號和左右的空白
                        messages = messages.getText().replace(':', '').replace('\'', '').replace('"', '').strip()
                    # 把每個留言存進 messageDict
                    print(messages)
                    self.messageDict[date][referCompany].append( messages )
            else:
                for article in articles:
                    messages = article.find( 'span', 'f3 push-content' )
                    if messages:
                        messages = messages.getText().replace(':', '').replace('\'', '').replace('"', '').strip()

                        # 逐個留言與公司字典批配檢查是否有留言指涉到公司，若有就把留言存入 messageDict
                        referCompany = None
                        for key in self.dict_data:
                            for company in self.dict_data[key]:
                                if messages.find( company ) != -1:
                                    referCompany = self.dict_data[key][0]
                                    break
                        if referCompany:
                            print(messages)
                            self.messageDict[date][referCompany].append( messages )

