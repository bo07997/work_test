#-*- coding: utf-8 -*-
import tornado.web

class mainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")