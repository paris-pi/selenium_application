from selenium import webdriver
import time
import json
import os
import pyautogui



# save data to json file
def store(json_name,data):
    with open(json_name, 'w') as fw:
        json.dump(data,fw)
# load json data from file
def load(json_name):
    with open(json_name,'r') as f:
        data = json.load(f)
        return data
# add new data into the json (read the old data and append the new data)
def add_data(jsonname,new_data):
    list1 = []
    with open(jsonname,'r') as f:
        old_data = json.load(f)
        for i in range(len(old_data)):
            list1.append(old_data[i])
    list1.append(new_data)
    data = list1
    with open(jsonname, 'w') as fw:
        json.dump(data,fw)

def file_exist(filename):
    flag = os.path.exists(filename)
    return flag



def get_data(wd,coin):

    timeNow = time.localtime(time.time())
    now = time.strftime("%Y-%m-%d %H:%M:%S", timeNow)
    coin["time"] = now

    element_price = wd.find_element_by_css_selector("div.col-12 li.pair-price span")
    coin['price'] = element_price.text

    element_return_24h = wd.find_element_by_css_selector("div.col-12 li.mb-4 span")
    coin['return_24h'] = element_return_24h.text.replace('(24h: ','').replace(')','')


    element_pool_name = wd.find_elements_by_css_selector("div.col-12 li.data-volume span:nth-of-type(1)")

    element_pool_number = wd.find_elements_by_css_selector("div.col-12 li.data-volume span:nth-of-type(2)")
    # while True:
    #     element_volume = wd.find_element_by_css_selector("span.data-volume-right.pl-1.ng-star-inserted")
    #     if element_volume.text != 'Calculating...':
    #         break

    for i in range(len(element_pool_number)):
        coin[element_pool_name[i].text.replace(':','')] = element_pool_number[i].text


def open_browser(coin,r):
    try:
        time.sleep(5*r)
        wd = webdriver.Chrome(r'C:\Program Files\Google\Chrome\Application\chromedriver.exe')
        wd.implicitly_wait(100)
        url = coin['dextools']
        wd.get(url)
        time.sleep(60)
        while True:
            request(wd, coin)
            time.sleep(500)
    except:
        wd.close()


def request(wd,coin):

    get_data(wd,coin)
    print(coin)
    if file_exist("JsonDic\\" + coin["name"] + ".json"):
        add_data("JsonDic\\" + coin["name"] + ".json",coin)
    else:
        store("JsonDic\\" + coin["name"] + ".json",[coin])





















