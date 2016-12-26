
## Text messages sender api for Y853 EE router

:warning: This Project may not be maintained, I was bored, I did this :warning:

##### What is this about

Well, this lightweight python app allow you to send text message through a simple api call.

A POST request to the webservice once up send a text :
```
POST http://127.0.0.1:5000/

with Content-Type: application/json header and raw input in json :

{"dest": "+33XXXXXXXX",
"content": "Hi"}

```

Work with the latest firmware of Alcatel One Touch Y853 EE branded interface

##### Installation

1. Install requirements in a virtualenv (or not) with `pip install -r requirements.txt`
2. Make sure you are connected to the 4G router
3. Modify the config dict in **TextManager.py** if credentials or ip is not defaults ones
```python
config = {
    "router_addr": "http://192.168.1.1",
    "credentials": {
        "login": "admin",
        "password": "admin"
    }
}
```
4. Run app with a `python app.py`
5. Do a test request


##### Debug and Improvment

Do whatever you want to do or have to do with that code.
