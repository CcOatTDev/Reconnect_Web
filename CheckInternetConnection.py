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
second_check = os.getenv('SECOND_CHECK')
com_name = os.getenv('COMPUTERNAME')
mode = os.getenv('MODE')
check_time = bool(os.getenv('CHECK_TIME'))
begin_time = os.getenv('BEGIN_TIME')
end_time = os.getenv('END_TIME')

is_send_noti = True
disconnect_date = datetime.datetime.now()

print(f"LINE_TOKEN : {line_token}")
print(f"SECOND_CHECK : {second_check}")
print(f"COMPUTERNAME : {com_name}")
print(f"MODE : {mode}")
print(f"CHECK_TIME : {check_time}")
print(f"BEGIN_TIME : {begin_time}")
print(f"END_TIME : {end_time}")

def run():
    while True:
        time.sleep(int(second_check))
        now = datetime.datetime.now()
        print(now.strftime("%X"))
        if check_time:
            if now.strftime("%X") < begin_time or now.strftime("%X") > end_time:
                continue

        isConnected =  check_internet()
        print(f"loop => {isConnected}")
        if isConnected == False:
            if mode == "Reconnect_CCA":
                reconnect_internet()

            global is_send_noti
            global disconnect_date
            if(is_send_noti == True):
                is_send_noti = False
                disconnect_date = datetime.datetime.now()

        text = f"Computer : {com_name} \n Disconnected when :({disconnect_date}) \n Reconnected => Sucesssed : ({datetime.datetime.now()})"
        check_line_noti(text,isConnected)

def check_line_noti(text,isConnected):
    global is_send_noti
    if is_send_noti == False and isConnected == True:
        line_noti(line_token,text)
        is_send_noti = True
    return

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
    try:
        url = 'https://notify-api.line.me/api/notify'
        headers = {'content-type':'application/x-www-form-urlencoded','Authorization':'Bearer '+token}

        req = requests.post(url, headers=headers, data = {'message':message})
    except:
        return

run()
