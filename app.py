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
from tornado.escape import json_encode

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
			(r"/view/([a-zA-Z0-9]{5,7})", ViewStudentHandler),
			(r"/edit/([a-zA-Z0-9]{5,7})", EditStudentHandler),
			(r"/delete/([a-zA-Z0-9]{5,7})", StudentDeleteHandler),
			(r"/load/", LoadEveryone)
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
			page_title = "ITP Database",
			header_text = "Welcome to the ITP Databse. Behave.",
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
		cardid = self.get_argument('cardid', None)
		student = models.Student(
			firstName = firstName,
			lastName = lastName,
			nyuid = nyuid,
			cardid = cardid
		)
		student.save()
		self.redirect('/')

class ViewStudentHandler(tornado.web.RequestHandler):
	def get(self, sid):
		try: 
			type(int(sid))
			student = models.Student.objects.get(cardid=sid)
		except:
			student = models.Student.objects.get(nyuid=sid)
		if student is None:
			self.render("404.html", message=card_id)
		sObj = {
			"firstName": student.firstName,
			"lastName": student.lastName,
			"nyuid": student.nyuid,
			"cardid": student.cardid
		}
		self.write(json_encode(sObj))

class EditStudentHandler(tornado.web.RequestHandler):
	def get(self, sid):
		try: 
			type(int(sid))
			student = models.Student.objects.get(cardid=sid)
		except:
			student = models.Student.objects.get(nyuid=sid)
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
		student.cardid = self.get_argument('cardid', None)
		student.save()
		self.redirect('/')

class StudentDeleteHandler(tornado.web.RequestHandler):
	def get(self, sid):
		if len(sid) < 7:
			student = models.Student.objects.get(nyuid=sid)
		if len(sid) > 7:
			student = models.Student.objects.get(cardid=sid)
		student.delete()
		self.redirect("/")

class LoadEveryone(tornado.web.RequestHandler):
	def get(self):
		infilename = "/Users/slaffont/Dropbox/Semester4/itpdb/templates/students.json"
		infile = open(infilename, "r")
		students = []
		for line in infile:
			try:
				newStudent = json.loads(line)
			except:
				continue
			students.append(newStudent) 
		for student in students:
			student = models.Student(
				firstName = student["firstName"],
				lastName = student["lastName"],
				nyuid = student["nyuid"],
			)
			student.save()
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














