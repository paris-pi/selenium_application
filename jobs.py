import eight_btc_scraping
import binance_scraping
import threading



if __name__ == '__main__':
    # 使用threading模块，threading.Thread()创建线程，其中target参数值为需要调用的方法，同样将其他多个线程放在一个列表中，遍历这个列表就能同时执行里面的函数了
    threads = [threading.Thread(target=eight_btc_scraping.open_browser),
               threading.Thread(target=binance_scraping.update,args=[binance_scraping.old_text_dict, 284, 522])]
    for t in threads:
        # 启动线程
        t.start()
