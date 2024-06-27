from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import serial

app = Flask(__name__)

# LINE Developersで取得したアクセストークンとチャネルシークレットを設定
line_bot_api = LineBotApi('YOUR_CHANNEL_ACCESS_TOKEN')
handler = WebhookHandler('YOUR_CHANNEL_SECRET')

# Arduinoと接続するシリアルポートを設定
ser = serial.Serial('/dev/ttyUSB0', 9600)  # 適切なポートを設定

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

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    text = event.message.text
    if text.lower() == 'on':
        ser.write(b'1')
        reply_text = 'LEDを点灯しました。'
    elif text.lower() == 'off':
        ser.write(b'0')
        reply_text = 'LEDを消灯しました。'
    else:
        reply_text = '無効なコマンドです。ONまたはOFFを送信してください。'

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply_text))

if __name__ == "__main__":
    app.run(port=5000)
