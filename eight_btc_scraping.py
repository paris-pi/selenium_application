from selenium import webdriver
import time
import json
import pyperclip
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


def open_browser():
    wd = webdriver.Chrome(r'C:\Program Files\Google\Chrome\Application\chromedriver.exe')
    wd.implicitly_wait(100)
    url = 'https://www.8btc.com/flash'
    wd.get(url)
    big_news = wd.find_element_by_css_selector('.bbt-tab .bbt-tab__menu :nth-child(2)')
    big_news.click()

    broadcast_news = load('broadcast_news.json')

    while True:
        refresh(wd)
        for i in range(1,6):
            href, text = get_news(wd,i)
            if href not in broadcast_news:
                send_to_qq(284, 522)
                send_to_qq(262, 367)
                send_to_tg(text)
                add_data('broadcast_news.json',href)
        time.sleep(300)


def refresh(wd):
    refresh_button = wd.find_element_by_css_selector('.flash-timestamp__poll  button')
    refresh_button.click()

def get_news(wd,i):
    href = wd.find_element_by_css_selector('.flash-list .list-item--wrap:nth-child(' + str(i) + ') .flash-item h6 a').get_attribute('href')
    title = wd.find_element_by_css_selector('.flash-list .list-item--wrap:nth-child(' + str(i) + ') .flash-item h6 p').text.replace('巴比特早班车 | ',"")
    content_elements = wd.find_elements_by_css_selector('.flash-list .list-item--wrap:nth-child(' + str(i) + ') .flash-desc p')
    content = ''
    for element in content_elements:
        content = content + element.text + '\n'

    source = wd.find_element_by_css_selector('.flash-list .list-item--wrap:nth-child(' + str(i) + ') .flash-time span:nth-child(2) a').text

    text = "【" + title + "】" + '\n' + content + '-------------' + '\n' + '消息来源：' + source

    return href,text




def send_to_qq(text,x,y):
    pyautogui.hotkey('win', 'm')
    pyautogui.moveTo(x, y)
    pyautogui.click()
    time.sleep(0.1)
    pyautogui.click()
    time.sleep(0.1)
    pyperclip.copy(text)
    pyautogui.hotkey('ctrl', 'v')
    pyautogui.press('enter')
    time.sleep(0.1)
    pyautogui.hotkey('win', 'm')
    time.sleep(0.1)

def send_to_tg(text):
    pyautogui.hotkey('win', 'm')
    time.sleep(0.01)
    pyautogui.hotkey('win', '1')
    time.sleep(0.01)
    pyautogui.hotkey('ctrl', '1')
    time.sleep(0.01)

    pyperclip.copy(text)
    pyautogui.hotkey('ctrl', 'v')
    pyautogui.press('enter')
    time.sleep(0.1)
    pyautogui.hotkey('win', 'm')
    time.sleep(0.1)