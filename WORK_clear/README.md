Алгоритм работы google recaptcha на странице поиска:   
- https://www.google.com/search?q=apple GET      
- https://www.google.com/sorry/index?continue= GET   
................    
При нажатии кнопки я не робот:
- https://www.google.com/recaptcha/api2/reload?k= POST (открываеться фрейм)      
- https://www.google.com/recaptcha/api2/payload?p= GET (получает каретинку)          
- https://www.google.com/recaptcha/api2/replaceimage?k= POST (если капча 3х3, получает новую картинку ячейки)          
- https://www.google.com/recaptcha/api2/userverify?k= POST (подтверждает выполнение задания/переход к следующему)


https://rucaptcha.com/api-rucaptcha#solving_recaptchav2_new   
https://rucaptcha.com/blog/recaptcha-google-search   
https://rucaptcha.com/blog/obkhod-recaptcha-v2-na-stranitsakh-poiska-google    
https://kreisfahrer.gitbooks.io/selenium-webdriver/content/webdriver_intro/ozhidaniya.html    
https://overcoder.net/q/3867615/%D0%BF%D0%B5%D1%80%D0%B5%D1%85%D0%B2%D0%B0%D1%82%D0%B8%D1%82%D1%8C-%D0%BE%D1%82%D0%B2%D0%B5%D1%82-ajax-%D1%81-%D0%BF%D0%BE%D0%BC%D0%BE%D1%89%D1%8C%D1%8E-python-selenium-phantomjs    
https://stackoverflow.com/questions/22172604/convert-image-url-to-base64/22172860    
https://paveltashev.medium.com/python-and-selenium-open-focus-and-close-a-new-tab-4cc606b73388    
https://www.lambdatest.com/blog/python-selenium-switch-tabs/    
https://intoli.com/blog/javascript-injection/    
https://stackoverflow.com/questions/1285917/how-to-disable-javascript-when-using-selenium   
https://gist.github.com/2captcha/2ee70fa1130e756e1693a5d4be4d8c70   
https://github.com/ad-m/python-anticaptcha/issues/21   
https://www.imagetyperz.com/Forms/bypassrecaptcha_automation.aspx    
https://gist.github.com/sergeimuller/a609a9df7d30e2625a177123797471e2    
https://gist.github.com/plmrry/ac0af595d41bdb3391d1e45f895fcbb6    
https://stackoverflow.com/questions/15058462/how-to-save-and-load-cookies-using-python-selenium-webdriver    
https://pypi.org/project/selenium-wire/    
https://hpbn.co/xmlhttprequest/    
https://learn.javascript.ru/fetch    
https://saucelabs.com/blog/capture-network-traffic-with-automation-scripts    
https://livebook.manning.com/book/progressive-web-apps/chapter-4/64    
https://gist.github.com/wooddar/df4c89f381fa20ce819e94782dc5bc04 #Easy Python script to run selenium web workers/browsers in parallel    
https://github.com/amiiit/e2e-test-network    
https://github.com/derekargueta/selenium-profiler/blob/master/web_profiler.py    
https://qna.habr.com/q/553673    
https://github.com/derekargueta/selenium-profiler   

