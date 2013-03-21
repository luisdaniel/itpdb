#!/usr/bin/env python
# -*- coding: utf8 -*- 
import os, sys
from mongoengine import *

from datetime import datetime

import logging



class Student(Document):
	firstName = StringField()
	lastName = StringField()
	nyuid = StringField()
	cardid = IntField()
	gradYear = IntField()








