const express = require("express");
const { Client, middleware } = require("@line/bot-sdk");
const channelAccessToken = process.env.CHANNEL_ACCESS_TOKEN;
const channelSecret = process.env.CHANNEL_SECRET;
const app = express();

const config = {
  channelAccessToken: process.env.CHANNEL_ACCESS_TOKEN,
  channelSecret: process.env.CHANNEL_SECRET,
};

const client = new Client(config);

app.post("/callback", middleware(config), (req, res) => {
  Promise.all(req.body.events.map(handleEvent))
    .then((result) => res.json(result))
    .catch((err) => {
      console.error(err);
      res.status(500).end();
    });
});

function handleEvent(event) {
  if (event.type !== "message" || event.message.type !== "text") {
    return Promise.resolve(null);
  }

  const message = event.message.text.toLowerCase();
  let reply;

  if (message === "on") {
    reply = { type: "text", text: "LEDを点灯します。" };
    // Bluetooth通信のコードを追加
  } else if (message === "off") {
    reply = { type: "text", text: "LEDを消灯します。" };
    // Bluetooth通信のコードを追加
  } else {
    reply = {
      type: "text",
      text: "無効なコマンドです。ONまたはOFFを送信してください。",
    };
  }

  return client.replyMessage(event.replyToken, reply);
}

const listener = app.listen(process.env.PORT || 3000, () => {
  console.log("Your app is listening on port " + listener.address().port);
});
