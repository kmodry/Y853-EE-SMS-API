from flask import Flask, request
from TextManager import TextManager
app = Flask(__name__)

"""
Light Flask api to send text messages for
Alcatel One Touch Y853 EE branded interface
"""

@app.route("/", methods=['POST'])
def send():
  json = request.get_json()
  if not json or "dest" not in json or "content" not in json:
    return "error 400, missing parameters"

  txt_manager = TextManager()
  txt_manager.send_text(json.get("dest"), json.get("content"))
  return "Done"

if __name__ == "__main__":
  app.run()