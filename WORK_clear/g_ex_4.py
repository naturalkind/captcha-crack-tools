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

#51.15.197.24
#https://api.ipify.org/
if __name__ == "__main__":
        proxy = my_proxy("127.0.0.1", 9050)
        #proxy = my_proxy("91.233.61.210", "8000")
        #proxy.get("http://gexperiments.ru/")
        
        proxy.get("https://www.google.com/search?q=apple")
#        proxy.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.SHIFT + 'k')
#        A = ActionChains(proxy)
#        A.send_keys(Keys.F12)
        ##------------------------------------>
        g_response = proxy.find_elements_by_xpath('//textarea[@class="g-recaptcha-response"]')[0]
        recaptcha = proxy.find_elements_by_xpath('//div[@class="g-recaptcha"]')[0]
        data_s = recaptcha.get_attribute("data-s")
        U = proxy.execute_script("""return window.location.href""")
        #<form id="captcha-form" action="index" method="post">
        form_recaptcha = proxy.find_elements_by_xpath('//form[@id="captcha-form"]')[0]
        #proxy.execute_script("arguments[0].removeAttribute('action');arguments[0].removeAttribute('method');", form_recaptcha)
        
#        data-callback="submitCallback"
        ##--------------------------------------->
        #proxy.execute_script("arguments[0].setAttribute('data-callback', 'submitCallback_s');", recaptcha)
        
        proxy.execute_script("""arguments[0].style.display = 'block';arguments[0].value='..................................';
                                arguments[0].addEventListener('input', (event) => { 
                                    console.log("OK INPUT");
                                    parent.window.stop(); 
                                });
                  
                 //parent.window.location.reload();
                 
                                
            //var GH = document.getElementById('captcha-form');
                             """, g_response)
        # Важно вставлять скрипт в фрейм
        proxy.switch_to.frame(proxy.find_elements_by_tag_name("iframe")[2]) 
#        time.sleep(4)
        proxy.execute_script("""
//var scripts = parent.document.getElementsByTagName("script")[2];
//scripts.innerHTML = "var submitCallback = function(response) {console.log(response);};";
//console.log(scripts);
//parent.window.location.reload();   
parent.window.onunload = function (e) {
    e = e || parent.window.event;
    if(e.returnValue){
        console.log("ONUNLOAD"); 
    }
};
    
parent.window.onbeforeunload = (event) => {
  const e = event || parent.window.event;
  // Cancel the event
    console.log("onbeforeunload")
    var newDiv = document.createElement("div");
    newDiv.id = "div_stop_new";
    parent.document.body.appendChild(newDiv);
    parent.window.stop();
    window.stop();
};
        """)
        proxy.switch_to.window(proxy.window_handles[0])
#        EL = WebDriverWait(proxy, 3000).until(EC.visibility_of_element_located((By.ID, 'div_stop_new')))
        EL = WebDriverWait(proxy, 3000).until(EC.presence_of_element_located((By.ID, 'div_stop_new')))
        print (EL, "STOP")
        #EL.send_keys(Keys.CONTROL +'Escape')
        proxy.set_page_load_timeout(100)
        #proxy.execute_script("window.stop();")
#        A = ActionChains(EL)
#        A.send_keys(Keys.CONTROL +'Escape')


#parent.window.onbeforeunload = function (e) {
#    e = e || parent.window.event;
#    console.log("OK onbeforeunload");
#    parent.window.stop();
#    window.stop();
#};        
#                            """)  

#https://www.google.com/search?q=apple&google_abuse=GOOGLE_ABUSE_EXEMPTION=ID=df573b16c8ebba25:TM=1618935374:C=r:IP=104.244.72.36-:S=APGng0uuy6G5iKkognhQcSE_8pjJbLFQ8A; path=/; domain=google.com; expires=Tue, 20-Apr-2021 19:16:14 GMT



#        proxy.execute_script("""
#var scripts = parent.document.getElementsByTagName("script")[2];
#scripts.innerHTML = "var submitCallback = function(response) {console.log(response);};";
#console.log(scripts);

#function logSubmit(event) {
#     console.log("OK>>>>>>>>>>>>>>>");
#}   
#   
#            
#(function(xhr) {
#    var send = XMLHttpRequest.prototype.send;
#    xhr.prototype.send = function() {
#       console.log("SEND")
#            parent.window.stop();
#            var Asd_S = parent.document.getElementsByClassName('g-recaptcha')[0]; 
#            console.log(Asd_S);
#            Asd_S.removeAttribute('data-callback');
#       send.apply(this, arguments);
#       //----------------->
#       var scripts = parent.document.getElementsByTagName("script")[2];
#       scripts.innerHTML = "var submitCallback = function(response) {console.log(response);};";
#       //----------------->
#    };

#    var open = XMLHttpRequest.prototype.open;
#    xhr.prototype.open = function() {
#       if ( arguments[1].search("userverify") == 16 )
#       {
#            //submitCallback = function(response) {document.getElementById('captcha-form').submit();}
#            
#            var Asd_S = parent.document.getElementsByClassName('g-recaptcha')[0]; 
#            console.log(Asd_S);
#            Asd_S.removeAttribute('data-callback');
#    
#            
#            parent.window.stop();
#            var d = parent.document.getElementById('captcha-form'); //getElementsByTagName("body")[0];
#            d.removeAttribute('action');
#            d.removeAttribute('method');
#            console.log("STOP", d);
#            d.addEventListener('submit', logSubmit);
#            //----------------------->
#            var scripts = parent.document.getElementsByTagName("script")[2];
#            scripts.innerHTML = "var submitCallback = function(response) {console.log(response);};";
#            //----------------------->
#            
#            
#       };
#       
#       open.apply(this, arguments);
#    };

#})(XMLHttpRequest);     
#     
#       
#                            """)  


#           
#------------------------------------------------------------------>
        ## END TAB ONE
#        proxy.execute_script("window.open('');")
#        proxy.switch_to.window(proxy.window_handles[1])
#        proxy.get(U)
#        recaptcha_1 = proxy.find_elements_by_xpath('//div[@class="g-recaptcha"]')[0]
#        proxy.execute_script("arguments[0].setAttribute('data-s', arguments[1])", recaptcha_1, data_s)
#        g_response_1 = proxy.find_elements_by_xpath('//textarea[@class="g-recaptcha-response"]')[0]
#        proxy.execute_script("""arguments[0].style.display = 'block';arguments[0].value='..................................';
#                             """, g_response_1)
        #proxy.close()
        #proxy.switch_to.window(browser.window_handles[0])
        
        #
        #proxy.execute_script("window.open(window.location.href);")      
        #proxy.execute_script("document.getElementById('captcha-form').submit();")        
        #proxy.execute_script("var submitCallback = function(response) {console.log('OK');};", g_response)
        
        

####--------------------------------------------------------------------->        
#https://gist.github.com/Tomas2D/ed9e0a5ff196704d205b2fbd3a9880f6        
#https://github.com/ad-m/python-anticaptcha
#https://gist.github.com/2captcha/2ee70fa1130e756e1693a5d4be4d8c70
#https://github.com/derekargueta/selenium-profiler/blob/master/web_profiler.py
#https://dev.to/eons/detect-page-refresh-tab-close-and-route-change-with-react-router-v5-3pd
#https://www.testim.io/blog/how-to-wait-for-a-page-to-load-in-selenium/
#https://developer.mozilla.org/ru/docs/Web/API/Event/preventDefault
#https://developer.mozilla.org/en-US/docs/Web/API/Window/captureEvents
#https://developer.mozilla.org/ru/docs/Web/API/Window
#https://github.com/miyakogi/pyppeteer
#https://github.com/HDE/arsenic
