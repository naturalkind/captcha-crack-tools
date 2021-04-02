# -*- coding: utf-8 -*-
import ctypes
import cv2
import numpy as np

import os, sys, io, gc, re
import glob, uuid, base64, json, time

from tornado.escape import json_encode

from tornado import websocket, web, ioloop

import tornado.ioloop
import tornado.web
import tornado.websocket
import requests

site_key = "6LfMD5kaAAAAAA4gTPPtDGIZwDV1WKEh6UMakRuV"
secret_key = "6LfMD5kaAAAAAHC2ixz31rYAIrBK00niW2_S5GPg"



class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html", title="Нейронная сеть/Тренировка")
    def post(self):
#        data_json = json.loads(self.request.body)
#        print (data_json)
        URL = f'https://www.google.com/recaptcha/api/siteverify?secret={secret_key}&response={self.get_body_argument("g-recaptcha-response")}'
        
        #print (self.request.body, self.get_body_argument("text_surname"))
        r = requests.get(url = URL).json() 
        print (r, self.request.body)
        if r['success'] == True:
            self.write(self.get_body_argument("text_surname"))
        if r['success'] == False:
            self.write("Error Captcha")

        
class MainHandler2(tornado.web.RequestHandler):
    def get(self):
        self.render("index2.html", title="Нейронная сеть/Тренировка")
    def post(self):
        print (self.request.body)
        self.write(self.get_body_argument("text_surname"))
        

app = tornado.web.Application([
        (r"/", MainHandler),
        (r"/page1", MainHandler2),
        (r"/page2", MainHandler2),
    ])
    
app.listen(8800)

print("Starting server...") # IP

tornado.ioloop.IOLoop.current().start()

#https://github.com/search?l=Python&q=recaptcha+v2&type=Repositories
#https://coderoad.ru/42859813/Невидимая-форма-google-Recaptcha-и-ajax
#https://artisansweb.net/validate-google-recaptcha-using-javascript/
