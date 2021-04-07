from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from pynput.mouse import Button, Controller

import numpy as np
import cv2
import time
import random
import os
import io
import base64
import scipy.interpolate as si
import pickle

# get a new selenium webdriver with tor as the proxy
def my_proxy(PROXY_HOST,PROXY_PORT):
    fp = webdriver.FirefoxProfile()
    fp.set_preference("network.proxy.type", 1)
    fp.set_preference("network.proxy.socks",PROXY_HOST)
    fp.set_preference("network.proxy.socks_port",int(PROXY_PORT))

    fp.update_preferences()
    options = Options()
    #options.headless = True
    #return webdriver.Firefox(executable_path="geckodriver/geckodriver", options=options, firefox_profile=fp)
    return webdriver.Firefox(options=options, firefox_profile=fp)
    
def imgs(x):
      cv2.imshow('google image', np.array(x))
      cv2.waitKey(0)
      cv2.destroyAllWindows()

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
        
        #proxy.get("http://gexperiments.ru/")
        proxy.get("https://www.google.com/search?q=putin")
        ##------------------------------------>
        g_response = proxy.find_elements_by_xpath('//textarea[@class="g-recaptcha-response"]')[0]
        recaptcha = proxy.find_elements_by_xpath('//div[@class="g-recaptcha"]')[0]
        data_s = recaptcha.get_attribute("data-s")
        U = proxy.execute_script("""return window.location.href""")
#        data-callback="submitCallback"
        ##--------------------------------------->
        #proxy.execute_script("arguments[0].setAttribute('data-callback', 'submitCallback');", recaptcha)
        
#        proxy.execute_script("""arguments[0].style.display = 'block';arguments[0].value='..................................';
#                                arguments[0].addEventListener('input', (event) => { 
#                                var i = 0;
#                                while (i == 0) { 
#                                    console.log("OK");
#                                    window.stop();
#                                }
#                                });

#                             """, g_response)


#                                        window.stop();
#                                        var newDiv = document.createElement("div");
#                                        newDiv.id = "NEWdiv";
#                                        document.body.appendChild(newDiv);
#           
#------------------------------------------------------------------>
        ## END TAB ONE
        proxy.switch_to.window(proxy.window_handles[1])
        proxy.get(U)
        recaptcha_1 = proxy.find_elements_by_xpath('//div[@class="g-recaptcha"]')[0]
        proxy.execute_script("arguments[0].setAttribute('data-s', arguments[1])", recaptcha_1, data_s)
        g_response_1 = proxy.find_elements_by_xpath('//textarea[@class="g-recaptcha-response"]')[0]
        proxy.execute_script("""arguments[0].style.display = 'block';arguments[0].value='..................................';
                                arguments[0].onchange = function() {
                                    document.getElementById('captcha-form').submit();
                                };""", g_response_1)
        #proxy.close()
        #proxy.switch_to.window(browser.window_handles[0])
        
        #
        #proxy.execute_script("window.open(window.location.href);")      
        #proxy.execute_script("document.getElementById('captcha-form').submit();")        
        #proxy.execute_script("var submitCallback = function(response) {console.log('OK');};", g_response)
        
        

####--------------------------------------------------------------------->        
        
        

#https://rucaptcha.com/api-rucaptcha#solving_recaptchav2_new
#https://rucaptcha.com/blog/recaptcha-google-search
#https://rucaptcha.com/blog/obkhod-recaptcha-v2-na-stranitsakh-poiska-google
#https://kreisfahrer.gitbooks.io/selenium-webdriver/content/webdriver_intro/ozhidaniya.html
#https://overcoder.net/q/3867615/%D0%BF%D0%B5%D1%80%D0%B5%D1%85%D0%B2%D0%B0%D1%82%D0%B8%D1%82%D1%8C-%D0%BE%D1%82%D0%B2%D0%B5%D1%82-ajax-%D1%81-%D0%BF%D0%BE%D0%BC%D0%BE%D1%89%D1%8C%D1%8E-python-selenium-phantomjs
#https://stackoverflow.com/questions/22172604/convert-image-url-to-base64/22172860
#https://paveltashev.medium.com/python-and-selenium-open-focus-and-close-a-new-tab-4cc606b73388
#https://www.lambdatest.com/blog/python-selenium-switch-tabs/
#https://intoli.com/blog/javascript-injection/
#https://stackoverflow.com/questions/1285917/how-to-disable-javascript-when-using-selenium
#https://gist.github.com/2captcha/2ee70fa1130e756e1693a5d4be4d8c70
#https://github.com/ad-m/python-anticaptcha/issues/21
#https://www.imagetyperz.com/Forms/bypassrecaptcha_automation.aspx


# Вручную заменить callback
# поменять из одной ссессию в другую
# встраивать для перехвата js eval selenium
# Транслировать в окне страницу гугла
# 2 cсесии
# в одной получаю параметры
# в другую вставляю
# Повесил одно событие
#https://www.google.com/recaptcha/api2/userverify
# все клики которые есть на странице
# FIERFOX после перезагрузки не очищать лог

# userverify
# Путь кнопки подтверждения капчи
# Выследить userverify
# #CONSENT=PENDING+162
# TE: Trailers
#https://stackoverflow.com/questions/15058462/how-to-save-and-load-cookies-using-python-selenium-webdriver
#https://pypi.org/project/selenium-wire/
