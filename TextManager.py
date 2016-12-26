import requests, datetime, re
from random import randint

config = {
    "router_addr": "http://192.168.1.1",
    "credentials": {
        "login": "admin",
        "password": "admin"
    }
}


class TextManager:
  """Sms manager for 4g router."""

  def __init__(self):
    """Init stuff.

    Set Requests session instance
    Set meta_header to None: needed for auth tokenized hxr call
    """
    self.session = requests.Session()
    self.meta_header = None

  def call(self, uri, data=None):
    """Make request with a new generated auth header.

    Use Requests session POST to call with a different tokenized header for each action
    """
    # Get token first
    token_response = self.session.post('%s/goform/getToken?rand=%s' % (config["router_addr"], randint(1000000000, 9000000000)))
    if token_response.status_code != 200:
        raise Exception("Can't get action token")
    json_reponse = token_response.json()
    token = str(json_reponse.get("token"))

    # Weird token modification from EE router
    # Since an update, EE router interface need a special header built from
    # meta header content attribute in index.html page and from a != token on every important call
    def build_auth_token_header(meta_header, token):
      """Let the magic happen: this code is javascript translated from an uglified file."""
      n = list(meta_header)
      r = list(meta_header)[::-1]
      o = list(token)
      z = "%s%s%s" % (n[int(o[2])], o[1], n[int(o[4])])
      w = o[2] + "".join(r) + z.join(o)
      return {"_TclRequestVerificationToken": w}

    # add special header
    headers = {}
    if self.meta_header is not None:
        headers.update(build_auth_token_header(self.meta_header, token))
    return self.session.post("%s?rand=%s" % (uri, randint(1000000000, 9000000000)), data=data, headers=headers)

  def log_in(self):
    """Log into the webservice && retrieve session token."""
    meta_request = self.call('%s/default.html' % config["router_addr"])
    # grep content attribute in meta (needed for auth/tokenized actions)
    matches = re.search("<meta name=\"header-meta\" content=\"(.*)\"", meta_request.text)
    self.meta_header = matches.group(1)

    # log in
    data = {"username": config["credentials"]["login"],
            "password": config["credentials"]["password"]}
    self.call('%s/goform/setLogin' % config["router_addr"], data=data)

  def send_text(self, dest, content):
    """Send a text to someone."""
    self.log_in()

    # prepare xhr
    data = {"sms_id": "NaN",
            "action_type": "new",
            "sms_time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "sms_number": "%s" % dest,
            "sms_content": "%s" % content}

    # execute
    r = self.call('%s/goform/sendSMS' % config["router_addr"], data=data)
    if r.status_code != 200:
        raise Exception("SomeThing is broken")
    json_reponse = r.json()

    """
    Acutally there is way more verifications on the interface.
    Error 0 only mean that the router is going to try to send the text
    Network can fail to send it
    """

    if json_reponse.get("error") != 0:
        raise Exception("It's broken")
