from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

# import sentencepiece as spm

from SentensePiece import reply
# import os
# import requests


app = Flask(__name__)

# TALKAPI_KEY = os.environ['YOUR_API']
app.config['CHANNEL_ACCESS_TOKEN'] = 'U/oVg3fG2HXcIMdcLWeNcGJBGkIWZkmFQKlu6RbsiIGS0/5Skf//k4NBTelHhGEZO7muRgTldBTMYGK+tBlpYiBMuPOXWFed3s2lpjod4wCNG5Q1w/lWsGIaNyNEWSz0JouYkBv+VsOnqHtW6IsP6gdB04t89/1O/w1cDnyilFU='
app.config['CHANNEL_SECRET'] = '3105443c8351506641764c0ea3353fbd'

line_bot_api = LineBotApi(app.config['CHANNEL_ACCESS_TOKEN'])
handler = WebhookHandler(app.config['CHANNEL_SECRET'])

# def talkapi(text):
#    url = 'https://api.a3rt.recruit-tech.co.jp/talk/v1/smalltalk'
#    req = requests.post(url, {'apikey':TALKAPI_KEY,'query':text}, timeout=5)
#    data = req.json()

#    if data['status'] != 0:
#       return data['message']

#    msg = data['results'][0]['reply']
#    return msg

@app.route("/")
def say_hello():
    return "Hello"


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # sp = spm.SentencePieceProcessor()

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # push_text = event.message.text
    # msg = talkapi(push_text)
    # line_bot_api.reply_message(
    #     event.reply_token,
    #     TextSendMessage(text=msg))
    
    # ここで文章生成
    try:
        reply_text = reply()
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=reply_text))
    except BaseException:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="返信失敗..."))
    finally:
        print("aaa")


if __name__ == "__main__":
    app.run()