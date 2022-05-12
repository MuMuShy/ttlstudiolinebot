#圖文選單的回覆模板
#可以透過圖文選單模擬器進行排版 https://developers.line.biz/flex-simulator/


def SimpleFlexMessage():
    json = {
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
            "text": "基礎圖文選單",
            "weight": "bold",
            "size": "xl"
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
                    "text": "測試",
                    "color": "#aaaaaa",
                    "size": "sm",
                    "flex": 1
                },
                {
                    "type": "text",
                    "text": "測試內文",
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
                    "text": "測試2",
                    "color": "#aaaaaa",
                    "size": "sm",
                    "flex": 1
                },
                {
                    "type": "text",
                    "text": "測試內文",
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
            "type": "message",
            "label": "按鈕測試",
            "text": "hello"
            }
        },
        {
            "type": "button",
            "style": "link",
            "height": "sm",
            "action": {
            "type": "message",
            "label": "按鈕測試",
            "text": "hello"
            }
        },
        {
            "type": "box",
            "layout": "vertical",
            "contents": [],
            "margin": "sm"
        }
        ],
        "flex": 0
    }
    }
    return json
