
from datetime import timedelta

def default_message():
     return {
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                        {
                            "type": "image",
                            "url": "https://scdn.line-apps.com/n/channel_devcenter/img/flexsnapshot/clip/clip7.jpg",
                            "size": "5xl",
                            "aspectMode": "cover",
                            "aspectRatio": "150:196",
                            "gravity": "center",
                            "flex": 1
                        },
                        {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                                {
                                    "type": "image",
                                    "url": "https://scdn.line-apps.com/n/channel_devcenter/img/flexsnapshot/clip/clip8.jpg",
                                    "size": "full",
                                    "aspectMode": "cover",
                                    "aspectRatio": "150:98",
                                    "gravity": "center"
                                },
                                {
                                    "type": "image",
                                    "url": "https://scdn.line-apps.com/n/channel_devcenter/img/flexsnapshot/clip/clip9.jpg",
                                    "size": "full",
                                    "aspectMode": "cover",
                                    "aspectRatio": "150:98",
                                    "gravity": "center"
                                }
                            ],
                            "flex": 1
                        }
                    ]
                },
                {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                        {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                                {
                                    "type": "image",
                                    "url": "https://scdn.line-apps.com/n/channel_devcenter/img/flexsnapshot/clip/clip13.jpg",
                                    "aspectMode": "cover",
                                    "size": "full"
                                }
                            ],
                            "cornerRadius": "100px",
                            "width": "72px",
                            "height": "72px"
                        },
                        {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                                {
                                    "type": "text",
                                    "contents": [
                                        {
                                            "type": "span",
                                            "text": "brown_05",
                                            "weight": "bold",
                                            "color": "#000000"
                                        },
                                        {
                                            "type": "span",
                                            "text": "     "
                                        },
                                        {
                                            "type": "span",
                                            "text": "I went to the Brown&Cony cafe in Tokyo and took a picture"
                                        }
                                    ],
                                    "size": "sm",
                                    "wrap": True
                                },
                                {
                                    "type": "box",
                                    "layout": "baseline",
                                    "contents": [
                                        {
                                            "type": "text",
                                            "text": "1,140,753 Like",
                                            "size": "sm",
                                            "color": "#bcbcbc"
                                        }
                                    ],
                                    "spacing": "sm",
                                    "margin": "md"
                                }
                            ]
                        }
                    ],
                    "spacing": "xl",
                    "paddingAll": "20px"
                }
            ],
            "paddingAll": "0px"
        }
    }

def command_list( today ):
    return {
      "type": "bubble",
      "size": "mega",
      "header": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "text",
            "text": "指令",
            "color": "#e4f9ff",
            "size": "lg",
            "margin": "none"
          },
          {
            "type": "text",
            "text": "Updated: 2020-07-12",
            "size": "xs",
            "color": "#e4f9ff",
            "margin": "sm"
          }
        ]
      },
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "box",
            "layout": "vertical",
            "margin": "xxl",
            "spacing": "sm",
            "contents": [
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "text",
                    "text": "說明：查詢並分析特定公司時段內的留言情緒",
                    "margin": "md",
                    "size": "sm",
                    "color": "#555555",
                    "decoration": "underline"
                  },
                  {
                    "type": "text",
                    "text": "公司:起始日期:結束日期",
                    "size": "sm",
                    "color": "#555555",
                    "margin": "md",
                    "weight": "bold"
                  },
                  {
                    "type": "text",
                    "size": "sm",
                    "color": "#555555",
                    "flex": 0,
                    "text": "台積電:"+ ( today - timedelta( days = 2 )).strftime( "%Y-%m-%d" ) +":"+ today.strftime( "%Y-%m-%d" ) +"",
                    "margin": "md"
                  },
                  {
                    "type": "text",
                    "size": "sm",
                    "color": "#555555",
                    "flex": 0,
                    "text": "2330:"+ ( today - timedelta( days = 2 )).strftime( "%Y-%m-%d" ) +":"+ today.strftime( "%Y-%m-%d" ) +"",
                    "margin": "md"
                  },
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "查看公司評價",
                      "text": "台積電:"+ ( today - timedelta( days = 2 )).strftime( "%Y-%m-%d" ) +":"+ today.strftime( "%Y-%m-%d" ) +"",
                    },
                    "style": "secondary",
                    "margin": "md",
                    "color": "#a394804d",
                    "position": "relative"
                  }
                ],
                "margin": "xxl"
              },
              {
                "type": "separator",
                "margin": "xxl"
              },
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "text",
                    "text": "說明：查詢時段內留言，依照情緒正負歸納前後三名的公司",
                    "margin": "md",
                    "size": "sm",
                    "color": "#555555",
                    "wrap": True,
                    "decoration": "underline"
                  },
                  {
                    "type": "text",
                    "text": "風向:起始日期:結束日期",
                    "size": "sm",
                    "color": "#555555",
                    "flex": 0,
                    "margin": "md",
                    "weight": "bold"
                  },
                  {
                    "type": "text",
                    "size": "sm",
                    "color": "#555555",
                    "flex": 0,
                    "text": "風向:"+ ( today - timedelta( days = 2 )).strftime( "%Y-%m-%d" ) +":"+ today.strftime( "%Y-%m-%d" ) +"",
                    "margin": "md"
                  },
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "了解版內風向",
                      "text": "風向:"+ ( today - timedelta( days = 2 )).strftime( "%Y-%m-%d" ) +":"+ today.strftime( "%Y-%m-%d" ) +""
                    },
                    "style": "secondary",
                    "margin": "md",
                    "color": "#a394804d",
                    "position": "relative"
                  }
                ],
                "margin": "xxl"
              },
              {
                "type": "separator",
                "margin": "xxl"
              },
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "text",
                    "text": "說明：查詢意見領袖( 標的文作者 )評論",
                    "margin": "md",
                    "size": "sm",
                    "color": "#555555",
                    "wrap": True,
                    "decoration": "underline"
                  },
                  {
                    "type": "text",
                    "text": "ID:起始日期:結束日期",
                    "size": "sm",
                    "color": "#555555",
                    "flex": 0,
                    "margin": "md",
                    "weight": "bold"
                  },
                  {
                    "type": "text",
                    "size": "sm",
                    "color": "#555555",
                    "flex": 0,
                    "text": "Sunrisesky:"+ ( today - timedelta( days = 2 )).strftime( "%Y-%m-%d" ) +":"+ today.strftime( "%Y-%m-%d" ) +"",
                    "margin": "md"
                  },
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "查看作者評論",
                      "text": "Sunrisesky:"+ ( today - timedelta( days = 2 )).strftime( "%Y-%m-%d" ) +":"+ today.strftime( "%Y-%m-%d" ) +""
                    },
                    "style": "secondary",
                    "margin": "md",
                    "color": "#a394804d",
                    "position": "relative"
                  }
                ],
                "margin": "xxl"
              },
              {
                "type": "separator",
                "margin": "xxl"
              },
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "text",
                    "text": "說明：查詢時段內所有意見領袖，依時間區段計算其投資報酬率",
                    "margin": "md",
                    "size": "sm",
                    "color": "#555555",
                    "wrap": True,
                    "decoration": "underline"
                  },
                  {
                    "type": "text",
                    "text": "標的作者:起始日期:結束日期",
                    "size": "sm",
                    "color": "#555555",
                    "flex": 0,
                    "margin": "md",
                    "weight": "bold"
                  },
                  {
                    "type": "text",
                    "size": "sm",
                    "color": "#555555",
                    "flex": 0,
                    "text": "標的作者:"+ ( today - timedelta( days = 2 )).strftime( "%Y-%m-%d" ) +":"+ today.strftime( "%Y-%m-%d" ) +"",
                    "margin": "md"
                  },
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "分析作者報酬率",
                      "text": "標的作者:"+ ( today - timedelta( days = 2 )).strftime( "%Y-%m-%d" ) +":"+ today.strftime( "%Y-%m-%d" ) +""
                    },
                    "style": "secondary",
                    "margin": "md",
                    "color": "#a394804d",
                    "position": "relative"
                  }
                ],
                "margin": "xxl"
              }
            ]
          },
          {
            "type": "separator",
            "margin": "xxl"
          },
          {
            "type": "box",
            "layout": "horizontal",
            "margin": "md",
            "contents": [
              {
                "type": "text",
                "size": "xs",
                "color": "#aaaaaa",
                "flex": 0,
                "text": "Designer"
              },
              {
                "type": "text",
                "text": "Ben Wang",
                "color": "#aaaaaa",
                "size": "xs",
                "align": "end"
              }
            ]
          }
        ],
        "spacing": "md",
        "backgroundColor": "#ffffff4d"
      },
      "styles": {
        "header": {
          "backgroundColor": "#383e56",
          "separatorColor": "#383e56",
          "separator": True
        },
        "footer": {
          "separator": True
        }
      }
    }

def company_list():
    return {
      "type": "bubble",
      "hero": {
        "type": "image",
        "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/01_1_cafe.png",
        "size": "full",
        "aspectRatio": "20:13",
        "aspectMode": "cover",
        "action": {
          "type": "uri",
          "uri": "http://linecorp.com/"
        }
      },
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "text",
            "text": "Brown Cafe",
            "weight": "bold",
            "size": "xl"
          },
          {
            "type": "box",
            "layout": "baseline",
            "margin": "md",
            "contents": [
              {
                "type": "icon",
                "size": "sm",
                "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png"
              },
              {
                "type": "icon",
                "size": "sm",
                "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png"
              },
              {
                "type": "icon",
                "size": "sm",
                "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png"
              },
              {
                "type": "icon",
                "size": "sm",
                "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png"
              },
              {
                "type": "icon",
                "size": "sm",
                "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gray_star_28.png"
              },
              {
                "type": "text",
                "text": "4.0",
                "size": "sm",
                "color": "#999999",
                "margin": "md",
                "flex": 0
              }
            ]
          },
          {
            "type": "box",
            "layout": "vertical",
            "margin": "lg",
            "spacing": "sm",
            "contents": [
              {
                "type": "box",
                "layout": "baseline",
                "spacing": "sm",
                "contents": [
                  {
                    "type": "text",
                    "text": "Place",
                    "color": "#aaaaaa",
                    "size": "sm",
                    "flex": 1
                  },
                  {
                    "type": "text",
                    "text": "Miraina Tower, 4-1-6 Shinjuku, Tokyo",
                    "wrap": True,
                    "color": "#666666",
                    "size": "sm",
                    "flex": 5
                  }
                ]
              },
              {
                "type": "box",
                "layout": "baseline",
                "spacing": "sm",
                "contents": [
                  {
                    "type": "text",
                    "text": "Time",
                    "color": "#aaaaaa",
                    "size": "sm",
                    "flex": 1
                  },
                  {
                    "type": "text",
                    "text": "10:00 - 23:00",
                    "wrap": True,
                    "color": "#666666",
                    "size": "sm",
                    "flex": 5
                  }
                ]
              }
            ]
          }
        ]
      },
      "footer": {
        "type": "box",
        "layout": "vertical",
        "spacing": "sm",
        "contents": [
          {
            "type": "button",
            "style": "link",
            "height": "sm",
            "action": {
              "type": "uri",
              "label": "CALL",
              "uri": "https://linecorp.com"
            }
          },
          {
            "type": "button",
            "style": "link",
            "height": "sm",
            "action": {
              "type": "uri",
              "label": "WEBSITE",
              "uri": "https://linecorp.com"
            }
          },
          {
            "type": "spacer",
            "size": "sm"
          }
        ],
        "flex": 0
      }
    }

def company_comment(start_date,end_date):
    return {
        "type":"carousel",
        "contents":[
            {
                "type":"bubble",
                "size":"nano",
                "header":{
                    "type":"box",
                    "layout":"vertical",
                    "contents":[
                        {
                            "type":"text",
                            "text":"查看留言",
                            "color":"#e4f9ff",
                            "align":"center",
                            "size":"md",
                            "gravity":"center"
                        }
                    ],
                    "backgroundColor":"#383e56",
                    "paddingTop":"19px",
                    "paddingAll":"12px",
                    "paddingBottom":"16px"
                },
                "body":{
                    "type":"box",
                    "layout":"vertical",
                    "contents":[
                        {
                            "type":"box",
                            "layout":"horizontal",
                            "contents":[
                                {
                                    "type":"button",
                                    "action":{
                                        "type":"uri",
                                        "label":"前往網站",
                                        "uri":"https://ptt-stock-vane.herokuapp.com/comments?start_date="+start_date+"&end_date="+end_date+"&company="
                                    },
                                    "style":"secondary",
                                    "color":"#a394804d"
                                }
                            ],
                            "flex":1
                        }
                    ],
                    "spacing":"md",
                    "paddingAll":"12px"
                },
                "styles":{
                    "footer":{
                        "separator":False
                    }
                }
            }
        ]
    }