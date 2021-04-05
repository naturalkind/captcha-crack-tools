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


#<textarea id="g-recaptcha-response" name="g-recaptcha-response" class="g-recaptcha-response" style="width: 250px; height: 40px; border: 1px solid rgb(193, 193, 193); margin: 10px 25px; padding: 0px; resize: none; display: none;"></textarea>

#https://api.ipify.org/
if __name__ == "__main__":
        proxy = my_proxy("127.0.0.1", 9050)
        #proxy.get("http://gexperiments.ru/")
        #proxy.get("https://www.google.com/search?keyword=rolex&upcoming=false")
        #proxy.get("https://www.cloudflare.com/")
        proxy.get("https://www.google.com/recaptcha/api2/demo") #6Le-wvkSAAAAAPBMRTvw0Q4Muexq9bi0DJwx_mJ-
        g_response = proxy.find_elements_by_xpath('//textarea[@class="g-recaptcha-response"]')[0]
        proxy.execute_script("arguments[0].style.display = 'block';arguments[0].value='32sdfgsdssadasdsadasdasdasdawd';", g_response)
        #proxy.execute_script("arguments[0].value='32sdfgsdssadasdsadasdasdasdawd';", g_response)
        
        #### CAPTCHA CRACK
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
        answ = proxy.execute_script("""
                function getBase64Image(img) {
                      var canvas = document.createElement("canvas");
                      canvas.width = img.naturalWidth;
                      canvas.height = img.naturalHeight;
                      var ctx = canvas.getContext("2d");
                      ctx.drawImage(img, 0, 0);
                      var dataURL = canvas.toDataURL("image/jpeg").substring(22);
                      return dataURL;
                }
                var imgElement = document.querySelector('#rc-imageselect-target > table > tbody > tr:nth-child(2) > td:nth-child(2) > div > div.rc-image-tile-wrapper > img'); 
                console.log(imgElement.width);
                console.log(imgElement.naturalWidth);
                console.log(imgElement.src);
                var base64 = getBase64Image(imgElement);
                return base64;""")

        nparr = np.asarray(bytearray(io.BytesIO(base64.b64decode(answ)).read()), dtype=np.uint8)
        img_np = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        print (img_np.shape)
        imgs(img_np)
        

#https://rucaptcha.com/api-rucaptcha#solving_recaptchav2_new
#https://rucaptcha.com/blog/obkhod-recaptcha-v2-na-stranitsakh-poiska-google
#https://kreisfahrer.gitbooks.io/selenium-webdriver/content/webdriver_intro/ozhidaniya.html
#https://overcoder.net/q/3867615/%D0%BF%D0%B5%D1%80%D0%B5%D1%85%D0%B2%D0%B0%D1%82%D0%B8%D1%82%D1%8C-%D0%BE%D1%82%D0%B2%D0%B5%D1%82-ajax-%D1%81-%D0%BF%D0%BE%D0%BC%D0%BE%D1%89%D1%8C%D1%8E-python-selenium-phantomjs



#<div id="recaptcha" class="g-recaptcha" data-sitekey="6LfwuyUTAAAAAOAmoS0fdqijC2PbbdH4kjq62Y1b" data-callback="submitCallback" data-s="5E45C0MBp3uvJb2-w4sbwoigf2OAyrhF_CWQ5lvfdPveN6Ui_Py7ZBLU4W5Ul-pmEAAH5qquGQ6o_yU2RPF8kQ7V-9_H_PWKHuf8iLDu-psjbvYvO_UAwdNLSvhCzucN_mmvSSnagkcgufQLbN6S7WGQj-DbuTzO8skn5ZsjKjBlsu2psOVg26AGAiMnX842WMmlpTnny3t2yMji3auCYtoynJ51HOIQ2Cp0dyMcyhrcvPMndjW4lls"><div style="width: 304px; height: 78px;"><div><iframe src="https://www.google.com/recaptcha/api2/anchor?ar=1&amp;k=6LfwuyUTAAAAAOAmoS0fdqijC2PbbdH4kjq62Y1b&amp;co=aHR0cHM6Ly93d3cuZ29vZ2xlLmNvbTo0NDM.&amp;hl=ru&amp;v=5mNs27FP3uLBP3KBPib88r1g&amp;size=normal&amp;s=5E45C0MBp3uvJb2-w4sbwoigf2OAyrhF_CWQ5lvfdPveN6Ui_Py7ZBLU4W5Ul-pmEAAH5qquGQ6o_yU2RPF8kQ7V-9_H_PWKHuf8iLDu-psjbvYvO_UAwdNLSvhCzucN_mmvSSnagkcgufQLbN6S7WGQj-DbuTzO8skn5ZsjKjBlsu2psOVg26AGAiMnX842WMmlpTnny3t2yMji3auCYtoynJ51HOIQ2Cp0dyMcyhrcvPMndjW4lls&amp;cb=gpjlq6xy07fx" role="presentation" name="a-4i40o6b0issu" scrolling="no" sandbox="allow-forms allow-popups allow-same-origin allow-scripts allow-top-navigation allow-modals allow-popups-to-escape-sandbox allow-storage-access-by-user-activation" width="304" height="78" frameborder="0"></iframe></div><textarea id="g-recaptcha-response" name="g-recaptcha-response" class="g-recaptcha-response" style="width: 250px; height: 40px; border: 1px solid rgb(193, 193, 193); margin: 10px 25px; padding: 0px; resize: none; display: none;"></textarea></div><iframe style="display: none;"></iframe></div>
#var submitCallback = function(response) {document.getElementById('captcha-form').submit();};

