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
#    fp.set_preference("network.proxy.type", 1)
#    fp.set_preference("network.proxy.socks",PROXY_HOST)
#    fp.set_preference("network.proxy.socks_port",int(PROXY_PORT))

    fp.update_preferences()
    options = Options()
    options.add_argument("-devtools")
    #options.headless = True
    #return webdriver.Firefox(executable_path="geckodriver/geckodriver", options=options, firefox_profile=fp)
    return webdriver.Firefox(options=options, firefox_profile=fp)
    
def imgs(x):
      cv2.imshow('google image', np.array(x))
      cv2.waitKey(0)
      cv2.destroyAllWindows()

# Using B-spline for simulate humane like mouse movments

#https://api.ipify.org/
if __name__ == "__main__":
        proxy = my_proxy("127.0.0.1", 9050)
        #proxy.get("http://gexperiments.ru/")
        #proxy.get("https://www.google.com/search?keyword=rolex&upcoming=false")
        #proxy.get("https://www.cloudflare.com/")
        proxy.get("https://hackernoon.com/how-to-take-screenshots-in-the-browser-using-javascript-l92k3xq7") #6Le-wvkSAAAAAPBMRTvw0Q4Muexq9bi0DJwx_mJ- https://habr.com/ru/company/plarium/blog/345310/
        title = proxy.find_elements_by_tag_name("title")[0].get_attribute('innerHTML')
        img = proxy.find_elements_by_tag_name("img")
        
        for i in img:
            #print (i.get_attribute('width'))
            if int(i.get_attribute('width')) > 400:
                #-------------------------------------->
                print (i.get_attribute('src'), i)
                
#                # open the image in a new tab
#                proxy.execute_script('''window.open("''' + i.get_attribute('src') + '''","_blank");''')
#                proxy.switch_to.window(proxy.window_handles[1])
#                EL = WebDriverWait(proxy, 3000).until(EC.presence_of_element_located((By.TAG_NAME, 'img')))
#                S = proxy.get_screenshot_as_png()
#                S = np.frombuffer(S, np.uint8)
#                S = cv2.imdecode(S, cv2.IMREAD_COLOR)
#                imgs(S)
#                proxy.execute_script('''window.close();''')
#                proxy.switch_to.window(proxy.window_handles[0])

                #------------------------------------>
                # Full screan
#                S = proxy.get_screenshot_as_png()
#                S = np.frombuffer(S, np.uint8)
#                S = cv2.imdecode(S, cv2.IMREAD_COLOR)
#                location = i.location
#                size  = i.size
#                left = location['x']
#                top = location['y']
#                right = location['x'] + size['width']
#                bottom = location['y'] + size['height']
#                im = S[top:int(bottom), left:int(right)]
#                print (size, location, S.shape)
#                imgs(im)
#---------------------------------------------------------->
#                answ = proxy.execute_script("""
#                        function getBase64Image(img) {
#                              var canvas = document.createElement("canvas");
#                              canvas.width = img.naturalWidth;
#                              canvas.height = img.naturalHeight;
#                              var ctx = canvas.getContext("2d");
#                              ctx.drawImage(img, 0, 0);
#                              var dataURL = canvas.toDataURL("image/jpeg").substring(22);
#                              return dataURL;
#                        }
#                        arguments[0].crossOrigin = "";
#                        console.log(arguments[0].width);
#                        console.log(arguments[0].naturalWidth);
#                        console.log(arguments[0].src);
#                        var base64 = getBase64Image(arguments[0]);
#                        return base64;""", i)
#                nparr = np.asarray(bytearray(io.BytesIO(base64.b64decode(answ)).read()), dtype=np.uint8)
#                img_np = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
#                imgs(img_np)
#-------------------------------------------------------------->
        answ = proxy.execute_script(""" 
        var body = document.body,
            html = document.documentElement;

        var height = Math.max( body.scrollHeight, body.offsetHeight, 
                               html.clientHeight, html.scrollHeight, html.offsetHeight );
        return height;
        """)
        print (">>>>>>>>>>", answ)
        proxy.set_window_size(1920, answ)      #the trick
        #S = proxy.find_element_by_tag_name('html').screenshot("i.png") 
        S = proxy.get_screenshot_as_png()                 
        S = np.frombuffer(S, np.uint8)
        S = cv2.imdecode(S, cv2.IMREAD_COLOR)
#------------------------------------->
#        offset = 0 
#        height = proxy.execute_script('return Math.max('
#                                   'document.documentElement.clientHeight, window.innerHeight);')
#        img_li = []
#        while offset < answ:
#            # Scroll to height
#            proxy.execute_script(f'window.scrollTo(0, {offset});')
#            S = proxy.get_screenshot_as_png() 
#            S = np.frombuffer(S, np.uint8)
#            S = cv2.imdecode(S, cv2.IMREAD_COLOR)
#            img_li.append(S)
#            offset += height
#        Z = np.concatenate(img_li, 1)
#        print (Z.shape)  
#------------------------------------------------------>
#        S = proxy.get_screenshot_as_png()                 
#        S = np.frombuffer(S, np.uint8)
#        S = cv2.imdecode(S, cv2.IMREAD_COLOR)
        imgs(S)                 
                                                                
        print (len(img), title) 

#https://rucaptcha.com/api-rucaptcha#solving_recaptchav2_new
