#!/usr/bin/env python
#coding: utf8 
import os.path
import sys
import re
import logging
import datetime
import json

import tornado.auth
import tornado.escape
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

import pymongo
import bson
from mongoengine import *
import models

from tornado.options import define, options
define("port", default=8000, help="run on the given port", type=int )


# --------- Database Connection ---------
# MongoDB connection to MongoLab's database
connect('mydata', host=os.environ.get('MONGOLAB_URI'))
# app.logger.debug("Connecting to MongoLabs")
# mongodb_uri = 'mongodb://localhost:27017'
# db_name = 'heroku_app13757832'
# print('Connecting to database...')
# try: 
# 	MONGOLAB_URI = os.environ.get('MONGOLAB_URI')
# 	connection = pymongo.Connection(MONGOLAB_URI)
# 	self.db = connection[db_name]
# 	print('connection succesful')
# except:
# 	print('Error: Unable to connect to database.')
# 	connection = None


class Application(tornado.web.Application):
	def __init__(self):
		handlers = [
			(r"/", MainHandler),
			(r"/add/", AddStudentHandler),
			(r"/view/", ViewStudentHandler),
			(r"/edit/([a-zA-Z0-9]{6})", EditStudentHandler),
			(r"/edit/([a-zA-Z0-9]{24})", EditStudentHandler)
		]
		settings = dict(
			template_path=os.path.join(os.path.dirname(__file__), "templates"),
			static_path=os.path.join(os.path.dirname(__file__), "static"),
			ui_modules={"Student": StudentModule},
			debug=True
		)	
		tornado.web.Application.__init__(self, handlers, **settings)

class MainHandler(tornado.web.RequestHandler):
	def get(self):
		students = models.Student.objects()
		self.render(
			"index.html",
			page_title = "Reporta Violencia",
			header_text = "",
			students = students
		)

class AddStudentHandler(tornado.web.RequestHandler):
	def get(self):
		self.render(
			"addStudent.html",
			page_title="Add Student",
			header_text=""
		)
	def post(self):
		firstName = self.get_argument('firstName', None)
		lastName = self.get_argument('lastName', None)
		nyuid = self.get_argument('nyuid', None)
		gradYear = self.get_argument('gradYear', None)
		cardid = self.get_argument('cardid', None)
		student = models.Student(
			firstName = firstName,
			lastName = lastName,
			nyuid = nyuid,
			gradYear = gradYear,
			cardid = cardid
		)
		student.save()
		self.redirect('/')

class ViewStudentHandler(tornado.web.RequestHandler):
	def get(self):
		self.render(
			"viewStudent.html",
			page_title="View Student",
			header_text=""
		)

class EditStudentHandler(tornado.web.RequestHandler):
	def get(self, sid):
		if len(sid) < 7:
			student = models.Student.objects.get(nyuid=sid)
		if len(sid) > 7:
			student = models.Student.objects.get(cardid=sid)
		if student is None:
			self.render("404.html", message=card_id)
		self.render(
			"editStudent.html",
			page_title="Edit Student",
			header_text="",
			student=student
		)
	def post(self, sid):
		if len(sid) < 7:
			student = models.Student.objects.get(nyuid=sid)
		if len(sid) > 7:
			student = models.Student.objects.get(cardid=sid)
		student.firstName = self.get_argument('firstName', None)
		student.lastName = self.get_argument('lastName', None)
		student.nyuid = self.get_argument('nyuid', None)
		student.gradYear = self.get_argument('gradYear', None)
		student.cardid = self.get_argument('cardid', None)
		student.save()
		self.redirect('/')

class ReportDeleteHandler(tornado.web.RequestHandler):
	def get(self, report_id):
		if len(sid) < 7:
			student = models.Student.objects.get(nyuid=sid)
		if len(sid) > 7:
			student = models.Student.objects.get(cardid=sid)
		student.delete()
		self.redirect("/")

class StudentModule(tornado.web.UIModule):
	def render(self, student):
		return self.render_string(
			"modules/student.html",
			student=student,
		)
	def css_files(self):
		return "/static/css/recommended.css"
	def javascript_files(self):
		return "/static/js/recommended.js"


if __name__ == "__main__":
	tornado.options.parse_command_line()
	log = logging.getLogger('demo')
	log.setLevel(logging.DEBUG)
	http_server = tornado.httpserver.HTTPServer(Application())
	http_server.listen(os.environ.get("PORT", 8000))
	tornado.ioloop.IOLoop.instance().start()














