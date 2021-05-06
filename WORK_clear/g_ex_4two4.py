from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from pynput.mouse import Button, Controller
from selenium.webdriver.common.keys import Keys

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
    fp.set_preference("http.response.timeout", 1000)

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
            

#51.15.197.24
#https://api.ipify.org/
if __name__ == "__main__":
        proxy = my_proxy("127.0.0.1", 9050)
        #proxy = my_proxy("91.233.61.210", "8000")
        #proxy.get("http://gexperiments.ru/")
        
        proxy.get("https://www.google.com/search?q=big ban london")
        ##------------------------------------>
        #g_response = proxy.find_elements_by_xpath('//textarea[@class="g-recaptcha-response"]')[0]
        recaptcha = proxy.find_elements_by_xpath('//div[@class="g-recaptcha"]')[0]
        data_s = recaptcha.get_attribute("data-s")
        U = proxy.execute_script("""return window.location.href""")
        #<form id="captcha-form" action="index" method="post">
        #form_recaptcha = proxy.find_elements_by_xpath('//form[@id="captcha-form"]')[0]
        #proxy.execute_script("arguments[0].removeAttribute('action');arguments[0].removeAttribute('method');", form_recaptcha)
        #proxy.execute_script("arguments[0].setAttribute('data-callback', 'submitCallback_s');", recaptcha)
        ##---------------------------------------------->
#        proxy.execute_script("""arguments[0].style.display = 'block';arguments[0].value='START';
#                                arguments[0].addEventListener('input', (event) => { 
#                                    console.log("OK INPUT");
#                                    document.getElementById('captcha-form').submit();
#                                });
#                                
#                             """, g_response)
#    
        ## END TAB ONE
        proxy.execute_script("window.open('');")
        proxy.switch_to.window(proxy.window_handles[1])
        proxy.get(U)
        recaptcha_1 = proxy.find_elements_by_xpath('//div[@class="g-recaptcha"]')[0]
        proxy.execute_script("arguments[0].setAttribute('data-s', arguments[1])", recaptcha_1, data_s)
        #g_response_1 = proxy.find_elements_by_xpath('//textarea[@class="g-recaptcha-response"]')[0]
        g_response_1 = proxy.find_elements_by_xpath('//textarea[@id="g-recaptcha-response"]')[0]
#        proxy.execute_script("""arguments[0].style.display = 'block';arguments[0].value='..................................';
#                             """, g_response_1)
        proxy.execute_script("""arguments[0].style.display = 'block';arguments[0].value='AAAAAAAAAA';""", g_response_1)
#---------------------------------------->
        proxy.switch_to.frame(proxy.find_elements_by_tag_name("iframe")[2]) 
        proxy.execute_script("""

parent.window.onbeforeunload = (event) => {
  const e = event || parent.window.event;
    // Cancel the event
    console.log("onbeforeunload");
    var newDiv = document.createElement("div");
    newDiv.id = "div_stop_new";
    parent.document.body.appendChild(newDiv);
};
        """)
        proxy.switch_to.window(proxy.window_handles[1])
#        VG = proxy.execute_script("""var OPR = parent.document.getElementById('g-recaptcha-response'); 
#                                     return OPR.value""")
#        print (VG)
        EL = WebDriverWait(proxy, 3000).until(EC.presence_of_element_located((By.ID, 'div_stop_new')))
        VG = proxy.execute_script("""var OPR = parent.document.getElementById('g-recaptcha-response'); 
                                     return OPR.value""")
        proxy.execute_script("window.stop();")
        print (VG, "STOP")
        #------------------------------->
        proxy.switch_to.window(proxy.window_handles[0])
        g_response = proxy.find_elements_by_xpath('//textarea[@class="g-recaptcha-response"]')[0]
        proxy.execute_script("""arguments[0].style.display = 'block';
                                arguments[0].innerHTML = arguments[1];
                                document.getElementById('captcha-form').submit();
                                """, g_response, VG)
        print (VG, "STOP")
#        time.sleep(2)
#        proxy.execute_script("""document.getElementById('captcha-form').submit();
#                             """, g_response, VG)
        
        
#  https://stackoverflow.com/questions/57980022/java-selenium-2captcha-submit-form      
