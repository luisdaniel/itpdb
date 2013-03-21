#!/usr/bin/env python
# -*- coding: utf8 -*- 
import os, sys
from mongoengine import *

from datetime import datetime

import logging


class IndividualDeath(EmbeddedDocument):
	group = StringField(max_length=120)
	age = IntField(min_value=0, max_value=120)
	gender = StringField(max_length=6)

class GroupDead(EmbeddedDocument):
	group = StringField(max_length=120)
	numDead = IntField()

class Location(EmbeddedDocument):
	country = StringField(max_length=120, required=True)
	state = StringField(max_length=40)
	city = StringField(max_length=80)
	street = StringField()
	neighborhood = StringField()
	zipCode = IntField(max_value=100000)
	lat = ListField(IntField(min_value=-91, max_value=91))
	latV = IntField(min_value=-91, max_value=91)
	lon = ListField(IntField(min_value=-91, max_value=91))
	lonV = IntField(min_value=-181, max_value=181)

class Source(EmbeddedDocument):
	url = URLField(verify_exists=True)
	addTime = DateTimeField(default=datetime.now())

class Report(Document):
	ts = ComplexDateTimeField(default=datetime.now())
	loc = EmbeddedDocumentField(Location)
	date = DateTimeField()
	nDead = ListField(IntField()) #once a number has been inputed three times, it is saved in the numDeadVerified field.
	nDeadV = IntField()
	gDead = ListField(EmbeddedDocumentField(GroupDead)) #Array contains all inputs.
	gDeadV = ListField(EmbeddedDocumentField(GroupDead)) #This array contains only those inputs that have been repeated three times.
	iDead = ListField(EmbeddedDocumentField(IndividualDeath)) #array contains all inputs of people that died.
	iDeadV = ListField(EmbeddedDocumentField(IndividualDeath)) #once a IndividualDead is repeated three times in the previous field, it gets saved in this array
	bells = ListField(StringField())
	bellsV = ListField(StringField()) #once a belligerent is entered three times in the previous field, it's saved
	cat = ListField(StringField())
	catV = ListField(StringField()) #once a category is mentioned three times, it goes in here.
	tag = ListField(StringField())
	tagV = ListField(StringField()) #once a category is mentioned three times, it goes in here.
	sources = ListField(EmbeddedDocumentField(Source))

class UnverifiedReport(Document):
	ts = ComplexDateTimeField(default=datetime.now())
	loc = ListField(EmbeddedDocumentField(Location))
	date = ListField(DateTimeField())
	source = EmbeddedDocumentField(Source)










