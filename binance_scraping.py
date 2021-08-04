from selenium import webdriver
import time
import datetime
import pyautogui
import pyperclip

pyautogui.FAILSAFE = True

wd = webdriver.Chrome(r'C:\Program Files\Google\Chrome\Application\chromedriver.exe')
wd.implicitly_wait(100)

def get_url(element):
    url = element.get_attribute("href")
    return url

def get_text(element):
    text = element.text
    return text

def get_source_and_date(element):
    initial_page = wd.current_window_handle
    urlEle = element.get_attribute("href")  # 定位链接元素
    js = "window.open('" + urlEle + "')"  # 新窗口打开链接
    wd.execute_script(js)
    windows = wd.window_handles
    wd.switch_to.window(windows[-1])
    element1 = wd.find_element_by_css_selector(".css-1qw79v2 .css-vurnku :nth-child(1)")
    source = element1.text
    element2 = wd.find_element_by_css_selector(".css-1qw79v2 .css-vurnku :nth-child(2)")
    date = element2.text
    element3 = wd.find_element_by_css_selector(".mirror-bread-crumb a:nth-of-type(3)")
    section = element3.text
    wd.close()
    wd.switch_to.window(initial_page)
    return source,date,section


def get_text_dict(element_list):
    text_dict = {}
    for element in element_list:
        text_dict[element.text] = element
    return text_dict

def get_news_list():
    element_list = wd.find_elements_by_css_selector('.css-1s5qj1n .css-vurnku .css-ktxhrn a')
    for element in element_list:
        if element.text == '查看更多':
            element_list.remove(element)
    return element_list

def request():
    wd.get('https://www.binance.com/zh-CN/support/announcement')
    news_list = get_news_list()
    text_dict = get_text_dict(news_list)
    return news_list,text_dict




def white_list(text):
    white_list = ['上市']
    flag = False
    for item in white_list:
        if item in text:
            flag = True
            break
    return flag



def update(old_text_dict,x,y):
    try:
        new_news_list,new_text_dict = request()

        for newtext in new_text_dict.keys():
            if newtext not in old_text_dict.keys():
                old_news_list = new_news_list
                old_text_dict = new_text_dict
                if white_list(newtext):
                    send_to_qq(new_text_dict[newtext],x,y)
                    print('news updated!!!')
            else:
                now = datetime.datetime.now()
    except:
        alert(253,201)



def send_to_qq(newelement,x,y):
        source, date, section = get_source_and_date(newelement)
        pyautogui.hotkey('win', 'm')
        pyautogui.moveTo(x, y)
        pyautogui.click()
        time.sleep(0.05)
        pyautogui.click()
        time.sleep(0.05)
        pyperclip.copy(
                       '消息概览： \n'+'【' + get_text(newelement) + '】' +'\n'+
                       '-----------------------\n' +
                       '详情链接： \n'+ get_url(newelement)  +'\n'+
                       '-----------------------\n' +
                       '消息来源： '+ source                 +'\n'+
                       '-----------------------\n' +
                       '消息日期： '+ date                   +'\n'+
                       '-----------------------\n' +
                       '消息板块： '+ section                +'\n'
                       )
        pyautogui.hotkey('ctrl', 'v')
        pyautogui.press('enter')
        time.sleep(0.1)
        pyautogui.hotkey('win', 'm')
        time.sleep(0.1)


def alert(x,y):
    pyautogui.hotkey('win','m')
    pyautogui.moveTo(x,y)
    pyautogui.click()
    time.sleep(0.05)
    pyautogui.click()
    time.sleep(0.05)
    pyperclip.copy(
        'selenium运行异常'
    )
    pyautogui.hotkey('ctrl', 'v')
    pyautogui.press('enter')
    time.sleep(0.1)
    pyautogui.hotkey('win','m')
    time.sleep(0.1)





