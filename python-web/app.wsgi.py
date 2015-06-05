#!/usr/bin/env python
# -*- coding: utf-8 -*- 
#By: Tedezed
import os
from bottle import *
#Parcheamos para poder hacer el import de alta,etc
sys.path.append('/var/www/python-web/')
from alta import *
from baja import *
from herramientas import *
os.chdir(os.path.dirname(__file__))
application = default_app()

@route('/')
def index():
	return template('index.html')
	
@route('/alta')
def index():
	return template('alta.html')

@post('/r_alta')
def resultado():
	nom_usuario= request.forms.get('username')
	nom_dominio= request.forms.get('dom')
	if nom_usuario == '' or nom_dominio == '':
		return 'ERROR: Los campos no pueden esta vacios.'
	elif len(nom_dominio) > 50:
		return 'ERROR: El dominio no puede ser tan larga.'
	elif len(nom_usuario) > 10:
		return 'ERROR: El nombre de usuario no puede ser tan largo.'
	else:
		pass_ftpd = alta_ftpd(nom_usuario, nom_dominio)
		if pass_ftpd == 0:
			return 'ERROR: El usuario ya existe.'
		elif pass_ftpd == 1:
			return 'ERROR: El dominio ya esta registrado.'
		else:
			pass_mysql = alta_mysql(nom_usuario)
			alta_bind9(nom_dominio)
			alta_apache2(nom_dominio, nom_usuario)
			reinicios()
			return 'Alta correcta de %s, su contrasena de usuario de MySQL es %s y la contrasena del usuario FTP es %s' % (nom_usuario, pass_mysql, pass_ftpd)

@route('/baja')
def index():
	return template('baja.html')

@post('/r_baja')
def resultado():
	nom_dominio= request.forms.get('dom')
	nom_usuario = baja_apache_bind(nom_dominio)
	if nom_usuario == 0:
		return 'ERROR: El dominio no existe.'
	else:
		baja_ftpd_mysql(nom_usuario)
		return 'Baja Correcta de dominio %s y usuario %s.' % (nom_dominio, nom_usuario)


@get('/images/<filename:re:.*>')
def sever_static(filename):
	return static_file(filename, root='statics/images')

@get('/css/<filename:re:.*>')
def sever_static(filename):
	return static_file(filename, root='statics/css')
