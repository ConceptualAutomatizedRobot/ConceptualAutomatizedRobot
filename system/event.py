#!/usr/bin/python
#-*- coding: utf-8 -*-
class Event(object):

	def __init__(self,type,value):
		self.type = type
		self.value = value

	def __str__(self):
		return "type : "+str(self.type)+", value : "+str(self.value)