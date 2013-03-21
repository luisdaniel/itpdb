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


from tornado.options import define, options
define("port", default=8000, help="run on the given port", type=int )



class Application(tornado.web.Application):
	def __init__(self):
		handlers = [
			(r"/", MainHandler),
			(r"/reporte/agregar/", AddReportHandler),
			(r"/reporte/lugar/", LocationReportHandler),
			(r"/reporte/fecha/", DateReportHandler),
			(r"/reporte/doble/", DuplicateReportHandler),
			(r"/reporte/detalles/", DetailReportHandler),
			(r"/buscar/", SearchReportHandler),
			(r"/descargar/", DownloadReportHandler)
		]
		settings = dict(
			template_path=os.path.join(os.path.dirname(__file__), "templates"),
			static_path=os.path.join(os.path.dirname(__file__), "static"),
			debug=True
		)	
		tornado.web.Application.__init__(self, handlers, **settings)

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render(
			"index.html",
			page_title = "Reporta Violencia",
			header_text = ""
		)

class AddReportHandler(tornado.web.RequestHandler):
	def get(self):
		self.render(
			"agregarReporte.html",
			page_title="Agregar Artículos",
			header_text="Agregar Artículos"
		)
	def post(self):
		links = self.get_argument('links', None)
		#self.write(links)

class LocationReportHandler(tornado.web.RequestHandler):
	def get(self):
		self.render(
			"reportarLugar.html",
			page_title="Verificar Lugar",
			header_text="Verificar Lugar"
		)

class DateReportHandler(tornado.web.RequestHandler):
	def get(self):
		self.render(
			"reportarFecha.html",
			page_title="Verificar Fecha",
			header_text="Verificar Fecha"
		)

class DuplicateReportHandler(tornado.web.RequestHandler):
	def get(self):
		self.render(
			"reportarDuplicados.html",
			page_title="Eliminar Duplicados",
			header_text="Eliminar Duplicados"
		)

class DetailReportHandler(tornado.web.RequestHandler):
	def get(self):
		self.render(
			"reportarDetalles.html",
			page_title="Llenar Detalles de Reportes",
			header_text="Llenar Detalles de Reportes"
		)

class SearchReportHandler(tornado.web.RequestHandler):
	def get(self):
		self.render(
			"buscarReporte.html",
			page_title="Buscar Reportes",
			header_text="Buscar Reportes"
		)

class DownloadReportHandler(tornado.web.RequestHandler):
	def get(self):
		self.render(
			"descargarReportes.html",
			page_title="Descargar Reportes",
			header_text="Descargar Reportes"
		)

if __name__ == "__main__":
	tornado.options.parse_command_line()
	log = logging.getLogger('demo')
	log.setLevel(logging.DEBUG)
	http_server = tornado.httpserver.HTTPServer(Application())
	http_server.listen(os.environ.get("PORT", 8000))
	tornado.ioloop.IOLoop.instance().start()














