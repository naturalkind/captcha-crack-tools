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


# get a new selenium webdriver with tor as the proxy
def my_proxy(PROXY_HOST,PROXY_PORT):
    fp = webdriver.FirefoxProfile()
    fp.set_preference("network.proxy.type", 1)
    fp.set_preference("network.proxy.socks",PROXY_HOST)
    fp.set_preference("network.proxy.socks_port",int(PROXY_PORT))

    fp.update_preferences()
    options = Options()
    #options.headless = True
    return webdriver.Firefox(executable_path="geckodriver/geckodriver", options=options, firefox_profile=fp)
    #return webdriver.Firefox(options=options, firefox_profile=fp)
    
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
        proxy.get("https://www.google.com/search?q=apple")#search?keyword=rolex&upcoming=false
        proxy.switch_to.frame(proxy.find_elements_by_tag_name("iframe")[0]) 
        check_box = WebDriverWait(proxy, 10).until(EC.element_to_be_clickable((By.ID ,"recaptcha-anchor")))
        time.sleep(2)
        action =  ActionChains(proxy);
        human_like_mouse_move(action, check_box)
        check_box.click() 

        time.sleep(2)
        proxy.switch_to.default_content()
        iframes = proxy.find_elements_by_tag_name("iframe")
        proxy.switch_to.frame(iframes[2]) # Переходим к iframe

        # Поиск ссылки на изображение, класс поиска, тип reCaptcha
        html = proxy.page_source
        try:
            img_rc = proxy.find_elements_by_xpath('//img[@class="rc-image-tile-33"]')[0]
            t_type = 3
        except IndexError:
            img_rc = proxy.find_elements_by_xpath('//img[@class="rc-image-tile-44"]')[0]
            t_type = 4 
        try:
            required_class = proxy.find_elements_by_xpath('//div[@class="rc-imageselect-desc-no-canonical"]/strong')[0].text
        except IndexError:
            required_class = proxy.find_elements_by_xpath('//div[@class="rc-imageselect-desc"]/strong')[0].text
        print (t_type)
        print (required_class)
        time.sleep(2)
        answ = proxy.execute_script(''' 
                var img = new Image();
                var cnv = document.createElement('canvas');
                cnv.id = 'tutorial';
                    img.onload = function(){
                      cnv.height = img.height;
                      cnv.width = img.width;
                      console.log(cnv.width, cnv.height, img.width, img.height);
                      cnv.getContext('2d').drawImage(img, 0, 0);
                    }
                        var request = new XMLHttpRequest();
                        request.open('GET', arguments[0].src);
                        request.responseType = 'blob';
                        request.onload = function() {
                            var reader = new FileReader();
                            reader.readAsDataURL(request.response);
                            reader.onload =  function(e){
                                img.src = e.target.result;
                            };
                        };
                        request.send();
                var child = document.body.appendChild(cnv);
                ''', img_rc)
        time.sleep(4)
        answ = proxy.execute_script(''' 
                cnv = document.getElementById('tutorial');
                return cnv.toDataURL('image/jpeg').substring(22);
        ''')

        nparr = np.asarray(bytearray(io.BytesIO(base64.b64decode(answ)).read()), dtype=np.uint8)
        img_np = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        print (img_np.shape)
        imgs(img_np)
#---------------------------- >
#        answ_ocr = ocr(img_np, required_class, t_type)
#----------------------------->
#        # Нажимаем нужный квадрат
#        ids = proxy.find_elements_by_xpath('//td[@class="rc-imageselect-tile"]')
#        for i in answ_ocr:
#            ids[i].click()   

#        # Поиск и нажатие кнопки подтвердить/продолжить
#        confirm_btn = WebDriverWait(proxy, 4).until(EC.element_to_be_clickable((By.XPATH ,'//button[@id="recaptcha-verify-button"]'))) #Нахожу кнопку
#        action =  ActionChains(proxy);
#        human_like_mouse_move(action, confirm_btn) # Двигать курсор к кнопке  
#        confirm_btn.click() # Нажать



