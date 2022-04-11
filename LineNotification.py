import requests

def line_noti(token, message):
    try:
        url = 'https://notify-api.line.me/api/notify'
        headers = {'content-type':'application/x-www-form-urlencoded','Authorization':'Bearer '+token}

        req = requests.post(url, headers=headers, data = {'message':message})
    except:
        return