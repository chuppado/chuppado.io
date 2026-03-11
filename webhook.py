from http.server import BaseHTTPRequestHandler
import urllib.request
import json
import os


def send_reply(reply_token: str, message: str):
    token = os.environ["LINE_CHANNEL_ACCESS_TOKEN"]

    payload = {
        "replyToken": reply_token,
        "messages": [{"type": "text", "text": message}]
    }

    req = urllib.request.Request(
        "https://api.line.me/v2/bot/message/reply",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}"
        },
        method="POST"
    )
    with urllib.request.urlopen(req) as res:
        return res.status


def get_announcement_message(day: str = "") -> str:
    return (
        f"🧺 Schedule Reminder!\n"
        f"Time to do your Schedule{f' ({day})' if day else ''}!\n\n"
        f"✅ https://chuppado.github.io/\n"
    )


class handler(BaseHTTPRequestHandler):

    def do_POST(self):
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length)

        try:
            data = json.loads(body)
            events = data.get("events", [])

            for event in events:
                # Only handle text messages
                if event.get("type") != "message":
                    continue
                if event["message"].get("type") != "text":
                    continue

                user_text = event["message"]["text"].strip().lower()
                reply_token = event["replyToken"]

                # Trigger phrase — case-insensitive
                if user_text == "link please bot":
                    send_reply(reply_token, get_announcement_message())

        except Exception as e:
            print(f"Error: {e}")

        # Always return 200 to LINE
        self.send_response(200)
        self.end_headers()

    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"LINE Webhook is running!")
