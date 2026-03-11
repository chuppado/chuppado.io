#!/usr/bin/env python3
"""
LINE Bot Webhook Server
Run with: python3 webhook.py
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.request
import json
import os

LINE_CHANNEL_ACCESS_TOKEN = os.environ.get("LINE_CHANNEL_ACCESS_TOKEN", "")

TRIGGER_PHRASE = "link please bot"
ANNOUNCEMENT_URL = "https://chuppado.github.io/"
ANNOUNCEMENT_URL_2 = "https://chuppado.github.io.order/"


def send_reply(reply_token: str, message: str):
    payload = {
        "replyToken": reply_token,
        "messages": [{"type": "text", "text": message}]
    }
    req = urllib.request.Request(
        "https://api.line.me/v2/bot/message/reply",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {LINE_CHANNEL_ACCESS_TOKEN}"
        },
        method="POST"
    )
    with urllib.request.urlopen(req) as res:
        print(f"✅ Reply sent! Status: {res.status}")


def get_message() -> str:
    return (
        f"🧺 Schedule Reminder!\n"
        f"Time to do your Schedule!\n\n"
        f"✅ {ANNOUNCEMENT_URL}\n"
        f"✅ {ANNOUNCEMENT_URL_2}\n"
    )


class WebhookHandler(BaseHTTPRequestHandler):

    def do_POST(self):
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length)

        try:
            data = json.loads(body)
            for event in data.get("events", []):
                if event.get("type") != "message":
                    continue
                if event["message"].get("type") != "text":
                    continue

                user_text = event["message"]["text"].strip().lower()
                reply_token = event["replyToken"]

                print(f"📩 Received: '{user_text}'")

                if user_text == TRIGGER_PHRASE:
                    send_reply(reply_token, get_message())
                    print(f"📤 Replied with announcement!")

        except Exception as e:
            print(f"⚠️  Error: {e}")

        # Always return 200 to LINE
        self.send_response(200)
        self.end_headers()

    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Webhook is running!")

    def log_message(self, format, *args):
        # Custom log format
        print(f"🌐 {args[0]} {args[1]}")


if __name__ == "__main__":
    PORT = int(os.environ.get("PORT", 5000))
    print(f"🚀 Webhook server running on port {PORT}")
    print(f"💬 Trigger phrase: '{TRIGGER_PHRASE}'")
    print(f"   (waiting for messages...)\n")
    server = HTTPServer(("0.0.0.0", PORT), WebhookHandler)
    server.serve_forever()
