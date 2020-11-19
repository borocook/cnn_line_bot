from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    FollowEvent, MessageEvent, TextMessage, ImageMessage, TextSendMessage,
)
import os

import unown_class

app = Flask(__name__)

#環境変数取得
YOUR_CHANNEL_ACCESS_TOKEN = os.environ["YOUR_CHANNEL_ACCESS_TOKEN"]
YOUR_CHANNEL_SECRET = os.environ["YOUR_CHANNEL_SECRET"]

line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

hello_mes = '{Nickname}さん、はじめまして！友だち追加ありがとうございます。{AccountName}です。'
+'ポケモンのアンノーンの画像を送信して頂くと自動でAIが判別して結果を返信します。'
+'【画像の注意事項】１．画像はなるべく隙間を無くしてください。２．背景の色は統一してください。'

@handler.add(FollowEvent)
def handle_follow(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=hello_mes)
    )

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=hello_mes))

@handler.add(MessageEvent, message=(ImageMessage))
def handle_image_message(event):
    content = line_bot_api.get_message_content(event.message.id)
    img_dirname = event.message.id + ".jpg"
    with open(img_dirname, "wb") as f:
        for chunk in content.iter_content():
            f.write(chunk)
    result = unown_class.Classification(img_dirname)
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=result))
    
    
if __name__ == "__main__":
#    app.run()
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)