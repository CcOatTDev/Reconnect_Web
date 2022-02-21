import requests
import time
import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os
from dotenv import load_dotenv

#from webdriver_manager.chrome import ChromeDriverManager
#https://selenium-python.readthedocs.io/locating-elements.html

load_dotenv()

line_token = os.getenv('LINE_TOKEN')
user_name = os.getenv('USER_NAME')
pass_word = os.getenv('PASS_WORD')
chexk_time = True

print(line_token)

def check_internet():
    url='https://www.google.co.th/'
    timeout=5
    try:
        _ = requests.get(url, timeout=timeout)
        return True
    except requests.ConnectionError:
        print("İnternet Disconnect")
    return False

def reconnect_internet():
    try:
        print("reconnect")

        #driver = webdriver.Chrome(ChromeDriverManager().install())
        driver = webdriver.Chrome('C:\Program Files\Google\Chrome\Application\chromedriver')
        driver.implicitly_wait(0.5)
        #launch URL
        driver.get("http://10.0.0.1/login")
        #identify text box
        username = driver.find_element_by_xpath("//form[@name='login']/label/input[@name='username']")
        password = driver.find_element_by_xpath("//form[@name='login']/label/input[@name='password']")
        submit = driver.find_element_by_xpath("//form[@name='login']/input[@type='submit']")
    
        #send input
        username.send_keys("216")
        password.send_keys("25n")

        #send keyboard input
        submit.send_keys(Keys.ENTER)
        time.sleep(5)
    except:
        return

def line_noti(token, message):
    url = 'https://notify-api.line.me/api/notify'
    headers = {'content-type':'application/x-www-form-urlencoded','Authorization':'Bearer '+token}

    req = requests.post(url, headers=headers, data = {'message':message})
    #print(req.text)
    return

while True:
    time.sleep(5)
    now = datetime.datetime.now()
    print(now.strftime("%X"))
    if chexk_time:
        if now.strftime("%X") < "04:00:00" or now.strftime("%X") > "10:30:00":
            continue

    isConnected =  check_internet()
    print(f"loop => {isConnected}")
    if isConnected == True:
        continue

    reconnect_internet()
    isConnected =  check_internet()
    line_noti(line_token,f" Reconnect Internet => Sucesssed : [{isConnected}] at ({now})")



#pyinstaller
