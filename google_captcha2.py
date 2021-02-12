from stem import Signal
from stem.control import Controller
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from fake_useragent import UserAgent
from pynput.mouse import Button, Controller

from bs4 import BeautifulSoup
import numpy as np
import cv2
import requests as R
import time
import random
import json
import os
import ast
import io
import base64
import scipy.interpolate as si


# signal TOR for a new connection
def switchIP():
    with Controller.from_port(port = 9051) as controller:
        controller.authenticate()
        controller.signal(Signal.NEWNYM)

# get a new selenium webdriver with tor as the proxy
def my_proxy(PROXY_HOST,PROXY_PORT):
    fp = webdriver.FirefoxProfile()
    fp.set_preference("network.proxy.type", 1)
    fp.set_preference("network.proxy.socks",PROXY_HOST)
    fp.set_preference("network.proxy.socks_port",int(PROXY_PORT))

    #fp.set_preference("network.proxy.socks_remote_dns", False)
    fp.update_preferences()
    options = Options()
    #options.headless = True
    return webdriver.Firefox(executable_path="geckodriver/geckodriver", options=options, firefox_profile=fp)
    #return webdriver.Firefox(options=options, firefox_profile=fp)
def scroll():
    w = last_height//1000
    igg = 100
    for i in range(w):
        proxy.execute_script("window.scrollTo(0, {})".format(igg))
        time.sleep(0.3)
        igg += 100
    
def imgs(x):
      cv2.imshow('Rotat', np.array(x))
      cv2.waitKey(1)
      cv2.destroyAllWindows()
#
# Using B-spline for simulate humane like mouse movments
def human_like_mouse_move(action, start_element):

    points = [[6, 2], [3, 2],[0, 0], [0, 2]];
    points = np.array(points)
    x = points[:,0]
    y = points[:,1]


    t = range(len(points))
    ipl_t = np.linspace(0.0, len(points) - 1, 100)


    x_tup = si.splrep(t, x, k=1)
    y_tup = si.splrep(t, y, k=1)

    x_list = list(x_tup)
    xl = x.tolist()
    x_list[1] = xl + [0.0, 0.0, 0.0, 0.0]

    y_list = list(y_tup)
    yl = y.tolist()
    y_list[1] = yl + [0.0, 0.0, 0.0, 0.0]

    x_i = si.splev(ipl_t, x_list)
    y_i = si.splev(ipl_t, y_list)

    startElement = start_element

    action.move_to_element(startElement);
    action.perform();

    c = 5
    i = 0
    for mouse_x, mouse_y in zip(x_i, y_i):
        action.move_by_offset(mouse_x,mouse_y);
        action.perform();
        print("Move mouse to, %s ,%s" % (mouse_x, mouse_y))   
        i += 1    
        if i == c:
            break;
            
def ocr(x):
   pass
 
def imgs(x):
    cv2.imshow("Image", x) 
    cv2.waitKey(0)
    cv2.destroyAllWindows()
   
def cutimg(data, col):
    if True:
                im_w, im_h, im_c = data.shape
                w, h = im_w//col, im_h//col
                w_num, h_num = int(im_w/w), int(im_h/h)
                num = 0
                ls = []
                try: 
                        #print "post>"
                        for wi in range(0, w_num):
                           for hi in range(0, h_num):
                                num += 1
                                
                                imgs(data[wi*w:(wi+1)*w, hi*h:(hi+1)*h, :])
                        return ls
                except IndexError: 
                   pass    

#https://api.ipify.org/
if __name__ == "__main__":
        proxy = my_proxy("127.0.0.1", 9050)
        proxy.get("https://www.google.com/search?q=apple")#search?keyword=rolex&upcoming=false
        proxy.switch_to.frame(proxy.find_elements_by_tag_name("iframe")[0]) 
        check_box = WebDriverWait(proxy, 10).until(EC.element_to_be_clickable((By.ID ,"recaptcha-anchor")))
        time.sleep(5)
        action =  ActionChains(proxy);
        human_like_mouse_move(action, check_box)
        check_box.click() 

        for fps in range(10):
                data = proxy.get_screenshot_as_png()
                nparr = np.frombuffer(data, np.uint8)
                img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                #imgs(img)
        time.sleep(4)
        proxy.switch_to.default_content()
        iframes = proxy.find_elements_by_tag_name("iframe")
        proxy.switch_to.frame(iframes[2]) # Переходим к iframe

        # Поиск ссылки на изображение, 
        html = proxy.page_source
        soup = BeautifulSoup(html, features = "html.parser")
        J = soup.find_all('td', {"class": "rc-imageselect-tile"})
        JJ = soup.find('img', {"class" : "rc-image-tile-33"})
        JJJ = soup.find('img', {"class" : "rc-image-tile-44"})
        C = soup.find('div', {"class" : "rc-imageselect-desc-no-canonical"})
        title = C.find('strong').text # 
        print (title)
#        img_src = ""
#        t_type = ""
#        if JJ != None:
#           img_src = JJ["src"]
#           t_type = 3
#        if JJJ != None: 
#           img_src = JJJ["src"] 
#           t_type = 4 
#        print (t_type, img_src)#

        # Нажимаем нужный квадрат
        ids = proxy.find_elements_by_xpath('//td[@class="rc-imageselect-tile"]')
        ids[8].click()              

        #END
#        confirm_btn = WebDriverWait(proxy, 4).until(EC.element_to_be_clickable((By.XPATH ,'//button[@id="recaptcha-verify-button"]'))) #Нахожу кнопку
#        action =  ActionChains(proxy);
#        human_like_mouse_move(action, confirm_btn) # Двигать курсор к кнопке  
#        confirm_btn.click() # Нажимаю


#https://dev-gang.ru/article/perevod-teksta-s-pomosczu-google-translate-api-v-python-ahgm88wx1k/
