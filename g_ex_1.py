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


#https://api.ipify.org/
if __name__ == "__main__":
        proxy = my_proxy("127.0.0.1", 9050)
        #proxy.get("http://gexperiments.ru/")
        #proxy.get("https://www.google.com/search?q=putin")
        #proxy.get("https://www.cloudflare.com/")
        proxy.get("https://www.google.com/recaptcha/api2/demo") #6Le-wvkSAAAAAPBMRTvw0Q4Muexq9bi0DJwx_mJ-
        U = proxy.execute_script("""return window.location.href""")
        g_response = proxy.find_elements_by_xpath('//textarea[@class="g-recaptcha-response"]')[0]
        ##------------------------------------>
        recaptcha = proxy.find_elements_by_xpath('//div[@class="g-recaptcha"]')[0]
        data_s = recaptcha.get_attribute("data-s")
        print ("DATA S", data_s)
#        data-callback="submitCallback"
        ##--------------------------------------->
        #proxy.execute_script("arguments[0].setAttribute('data-callback', 'submitCallback');", recaptcha)
        proxy.execute_script("""arguments[0].style.display = 'block';arguments[0].value='..................................';
                             """, g_response)
                             
        proxy.switch_to.frame(proxy.find_elements_by_tag_name("iframe")[2])                       
        proxy.execute_script("""
(function(xhr) {
    var send = XMLHttpRequest.prototype.send;
    xhr.prototype.send = function() {
       //console.log("SEND", arguments);
       send.apply(this, arguments);
       
       //var performance = window.performance || window.mozPerformance || window.msPerformance || window.webkitPerformance || {};
       //console.log(performance.getEntries() || {});
       var p = performance.getEntriesByType("resource");
       console.log(">>>>>>>", p[p.length-1].initiatorType);
       console.log(">>>>>>>", p[p.length-1].name);
       //for (var i=0; i < p.length; i++) {
       //         console.log(p[i].initiatorType);
       //         console.log(p[i].name);
       //}
       
    };

    var open = XMLHttpRequest.prototype.open;
    xhr.prototype.open = function() {
        if ( arguments[1].search("userverify") == 16 ) {
                var newDiv = document.createElement("div");
                newDiv.id = "div_stop_new";
                parent.document.body.appendChild(newDiv);
                //console.log("OPEN", arguments);
       };
       
       open.apply(this, arguments);
    };

})(XMLHttpRequest);
                    console.log("load script")
                    
                       //var performance = window.performance || window.mozPerformance || window.msPerformance || window.webkitPerformance || {};
                       //console.log(performance.getEntries() || {});
                    
                    """)   
#        proxy.execute_script("""
#        
#document.querySelectorAll('.rc-imageselect-tile').forEach(item => {
#  item.addEventListener('click', event => {
#    console.log("TRRTSD.................");
#    
#  });
#});
#        """)                 
        time.sleep(5)         
        proxy.execute_script("""
G = function() {        
NEW_S = document.getElementsByClassName('rc-imageselect-tile');
for (var i = 0; i < NEW_S.length; i++) {
    NEW_S[i].addEventListener('click', (event) => {
         console.log(event, i)
         
         
        // Конфигурация observer (за какими изменениями наблюдать)
        const config = {
            attributes: true,
            childList: true,
            subtree: true
        };

        // Колбэк-функция при срабатывании мутации
        const callback = function(mutationsList, observer) {
            for (let mutation of mutationsList) {
                if (mutation.type === 'childList') {
                    console.log('A child node has been added or removed.');
                } else if (mutation.type === 'attributes') {
                    console.log('The ' + mutation.attributeName + ' attribute was modified.');
                }
            }
        };

        // Создаём экземпляр наблюдателя с указанной функцией колбэка
        const observer = new MutationObserver(callback);

        // Начинаем наблюдение за настроенными изменениями целевого элемента
        observer.observe(event.target, config);
         
    });
}
}
G();


                            """)  




        #### !!!!!!!!!! ВАЖНО            
        proxy.switch_to.default_content()                                          
        print (proxy.find_elements_by_tag_name("iframe")) 
        EL = WebDriverWait(proxy, 3000).until(EC.presence_of_element_located((By.ID, 'div_stop_new')))
        time.sleep(5)
        VG = proxy.execute_script("""var OPR = parent.document.getElementById('g-recaptcha-response'); 
                                         return OPR.value""") 
                                     
        print (VG)       
        #                   
#        check_box = WebDriverWait(proxy, 100).until(EC.element_to_be_clickable((By.ID ,"recaptcha-anchor")))
#        action =  ActionChains(proxy);
#        human_like_mouse_move(action, check_box)
#        check_box.click()

        #time.sleep(5)
#        proxy.switch_to.frame([1])

         
#        proxy.execute_script("""
#                        var element_007 = document.getElementById('recaptcha-verify-button');
#                        element_007.addEventListener('click', (event) => { 
#                        window.stop();
#                        console.log("OK");
#                        
#                        });
#                     """) 
                     
#        EL = WebDriverWait(proxy, 3000).until(EC.visibility_of_element_located) #lambda x: x.find_element_by_id('NEWdiv')
        
#        const selectElement = document.querySelector('.ice-cream');

#selectElement.addEventListener('change', (event) => {
#  const result = document.querySelector('.result');
#  result.textContent = `You like ${event.target.value}`;
#});
        
        
#        proxy.execute_script(f"window.open('');")#{U}
#        ## END TAB ONE
#        proxy.switch_to.window(proxy.window_handles[1])
#        proxy.get(U)
##        proxy.execute_script("""
##parent.window.onbeforeunload = (event) => {
##  const e = event || parent.window.event;
##    // Cancel the event
##    console.log("onbeforeunload");
##    var newDiv = document.createElement("div");
##    newDiv.id = "div_stop_new";
##    parent.document.body.appendChild(newDiv);
##};

##        """)
#      
#        recaptcha_1 = proxy.find_elements_by_xpath('//div[@class="g-recaptcha"]')[0]
#        proxy.execute_script("arguments[0].setAttribute('data-s', arguments[1])", recaptcha_1, data_s)
#        g_response_1 = proxy.find_elements_by_xpath('//textarea[@class="g-recaptcha-response"]')[0]
#        proxy.execute_script("""arguments[0].style.display = 'block';arguments[0].value='>>>>>>>>>>>>>>>';
#                             """, g_response_1)
#         
#        #func_1(proxy) 
#        proxy.switch_to.frame(proxy.find_elements_by_tag_name("iframe")[0]) 
#        check_box = WebDriverWait(proxy, 100).until(EC.element_to_be_clickable((By.ID ,"recaptcha-anchor")))
#        action =  ActionChains(proxy);
#        human_like_mouse_move(action, check_box)
#        check_box.click()
#        
#        proxy.switch_to.frame(proxy.find_elements_by_tag_name("iframe")[1])
#        EL = WebDriverWait(proxy, 3000).until(EC.visibility_of_element_located((By.ID, 'recaptcha-verify-button')))
#        print (EL) 
#        #proxy.switch_to.frame(proxy.find_elements_by_tag_name("iframe")[2]) 
#        proxy.execute_script = ("""
#(function(xhr) {
#    var send = XMLHttpRequest.prototype.send;
#    xhr.prototype.send = function() {
#       console.log("SEND");
#       send.apply(this, arguments);
#    };

#    var open = XMLHttpRequest.prototype.open;
#    xhr.prototype.open = function() {

#       console.log("OPEN")
#       open.apply(this, arguments);
#    };

#})(XMLHttpRequest);
#                    console.log("OPEN")""")          
#        
#                               
#        EL = WebDriverWait(proxy, 3000).until(EC.presence_of_element_located((By.ID, 'div_stop_new')))
#        VG = proxy.execute_script("""var OPR = parent.document.getElementById('g-recaptcha-response'); 
#                                     return OPR.value""")
#        proxy.execute_script("window.stop();")
#        print (VG, "STOP")
#        #proxy.close()
#        proxy.switch_to.window(browser.window_handles[0])
#        g_response = proxy.find_elements_by_xpath('//textarea[@class="g-recaptcha-response"]')[0]
#        proxy.execute_script("""arguments[0].style.display = 'block';
#                                arguments[0].innerHTML = arguments[1];
#                                """, g_response, VG)
#        print ("END")        
        
#        proxy.execute_script("window.open(window.location.href);")      
#        proxy.execute_script("document.getElementById('captcha-form').submit();")        
#        proxy.execute_script("var submitCallback = function(response) {console.log('OK');};", g_response)
        
####--------------------------------------------------------------------->        
        
#        #### CAPTCHA CRACK
#        proxy.switch_to.frame(proxy.find_elements_by_tag_name("iframe")[0]) 
#        check_box = WebDriverWait(proxy, 10).until(EC.element_to_be_clickable((By.ID ,"recaptcha-anchor")))
#        time.sleep(2)
#        action =  ActionChains(proxy);
#        human_like_mouse_move(action, check_box)
#        check_box.click() 

#        time.sleep(2)
#        proxy.switch_to.default_content()
#        iframes = proxy.find_elements_by_tag_name("iframe")
#        proxy.switch_to.frame(iframes[2]) # Переходим к iframe

#        # Поиск ссылки на изображение, класс поиска, тип reCaptcha
#        html = proxy.page_source
#        try:
#            img_rc = proxy.find_elements_by_xpath('//img[@class="rc-image-tile-33"]')[0]
#            t_type = 3
#        except IndexError:
#            img_rc = proxy.find_elements_by_xpath('//img[@class="rc-image-tile-44"]')[0]
#            t_type = 4 
#        try:
#            required_class = proxy.find_elements_by_xpath('//div[@class="rc-imageselect-desc-no-canonical"]/strong')[0].text
#        except IndexError:
#            required_class = proxy.find_elements_by_xpath('//div[@class="rc-imageselect-desc"]/strong')[0].text
#        print (t_type)
#        print (required_class)
#        time.sleep(2)
#        answ = proxy.execute_script("""
#                function getBase64Image(img) {
#                      var canvas = document.createElement("canvas");
#                      canvas.width = img.naturalWidth;
#                      canvas.height = img.naturalHeight;
#                      var ctx = canvas.getContext("2d");
#                      ctx.drawImage(img, 0, 0);
#                      var dataURL = canvas.toDataURL("image/jpeg").substring(22);
#                      return dataURL;
#                }
#                var imgElement = document.querySelector('#rc-imageselect-target > table > tbody > tr:nth-child(2) > td:nth-child(2) > div > div.rc-image-tile-wrapper > img'); 
#                console.log(imgElement.width);
#                console.log(imgElement.naturalWidth);
#                console.log(imgElement.src);
#                var base64 = getBase64Image(imgElement);
#                return base64;""")

#        nparr = np.asarray(bytearray(io.BytesIO(base64.b64decode(answ)).read()), dtype=np.uint8)
#        img_np = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
#        print (img_np.shape)
#        WebDriverWait(proxy, 300).until(lambda x: x.find_element_by_css_selector('.g-recaptcha-response'))
#        #imgs(img_np)
        

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
#https://iqss.github.io/dss-webscrape/filling-in-web-forms.html
#https://www.techiedelight.com/check-for-existence-of-image-at-given-url-javascript/
#https://blog.logrocket.com/programmatic-file-downloads-in-the-browser-9a5186298d5c/
#https://bitsofco.de/handling-broken-images-with-service-worker/
#https://daily-dev-tips.com/posts/vanilla-javascript-event-listener-on-multiple-elements/
# Система в которой отдаю целую html страницу без капчи
# храню картинки
# Обучаю сеть перед изменением кода
# кодирую код нейронной сетью, и каждый раз его меняю, так как веса инициализируются




