def alta_ftpd(nom_usuario, nom_dominio):
	#!/usr/bin/env python
	# -*- coding: utf-8 -*-
	import MySQLdb
	import os
	import sys
	from herramientas import id_generator
	
	#Configuracion basica de mysql ftpd
	host_db = "localhost"
	user_db = "ftpd"
	pass_db = "passftpd"
	nom_db = "ftpd"

	f_cont = open("contador_id","r")
	id_num = f_cont.read()
	id_sum = str(int(id_num) + 1)
	f_cont.close()
	f_cont = open("contador_id","w")
	f_cont.write(id_sum)
	f_cont.close()

	#SQL/DML
	random_pass = id_generator(10)
	select_usuario_db = "select username from usuarios where username='%s';" % nom_usuario
	select_dom_db = "select dominio from usuarios where dominio='%s';" % nom_dominio
	insert_usuario = "insert into usuarios (username, password, dominio, uid, gid, homedir, shell, activa) values ('%s', password('%s'), '%s', %s, 6000, '/var/www/%s/', '/bin/false', 1); " % (nom_usuario, random_pass, nom_dominio, id_sum, nom_dominio)

	#Conexion DB
	con_mysql = MySQLdb.connect(host=host_db, user=user_db, passwd=pass_db, db=nom_db)
	cursor = con_mysql.cursor()
	cursor.execute(select_usuario_db)
	data = cursor.fetchone()
	if data != None:
		return 0

	cursor.execute(select_dom_db)
	data = cursor.fetchone()
	if data != None:
		return 1
	else:
		cursor.execute(insert_usuario)
		os.system('mkdir /var/www/%s/' % nom_dominio)
		os.system('chown -R %s:%s /var/www/%s/' % (id_sum, id_sum, nom_dominio))
		os.system('sudo chmod -R 777 /var/www/')
		con_mysql.commit()
		return random_pass

def alta_mysql(nom_usuario):
	#!/usr/bin/env python
	# -*- coding: utf-8 -*-
	import MySQLdb
	import os
	import sys
	from herramientas import id_generator

	#Configuracion basica de mysql ftpd
	host_db = "localhost"
	user_db = "root"
	pass_db = "root"

	#SQL/DML
	random_pass = id_generator(10)
	creacion_db = 'create database %s;' % nom_usuario
	creacion_usuario_db = 'create user "%s"@"%s" IDENTIFIED BY "%s";' % (nom_usuario, host_db , random_pass)
	permisos_db = 'GRANT ALL PRIVILEGES ON %s .*TO  "%s"@"%s";' % (nom_usuario, nom_usuario, host_db)

	#Conexion DB
	con_mysql = MySQLdb.connect(host=host_db, user=user_db, passwd=pass_db)
	cursor = con_mysql.cursor()
	cursor.execute(creacion_db)
	cursor.execute(creacion_usuario_db)
	cursor.execute(permisos_db)
	con_mysql.commit()
	return random_pass

def alta_bind9(nom_dominio):
	#!/usr/bin/env python
	# -*- coding: utf-8 -*-
	from herramientas import plantilla_generator

	ruta = "/var/cache/bind/db.%s" % (nom_dominio)

	#Generar Zona
	dom_local=open("/etc/bind/named.conf.local","a")
	dom_local.write(plantilla_generator('dom_local',nom_dominio))
	dom_local.close()

	#Generar db zona
	db_dom =open(ruta,"w")
	db_dom.write(plantilla_generator('db_dom',nom_dominio))
	db_dom.close()

def alta_apache2(nom_dominio, nom_usuario):
	#!/usr/bin/env python
	# -*- coding: utf-8 -*-
	import os
	import sys
	from herramientas import plantilla_generator

	ruta = "/etc/apache2/sites-available/%s" % nom_dominio
	ruta_php = "/etc/apache2/sites-available/php_%s" % nom_dominio
	ruta_index = '/var/www/%s/index.html' % nom_dominio
	mens_html = '%s esta en construccion.' % nom_dominio

	#Creacion del index.html
	db_dom =open(ruta_index,"w")
	db_dom.write(mens_html)
	db_dom.close()
	
	#Creacion de vh 
	db_dom =open(ruta,"w")
	db_dom.write(plantilla_generator('virtualhost',nom_dominio))
	db_dom.close()

	#Creacion de PHPMyAdmin
	db_dom =open(ruta_php,"w")
	db_dom.write(plantilla_generator('phpadmin',nom_dominio))
	db_dom.close()

	#Habilitar sitios
	os.system("sudo a2ensite php_%s" % nom_dominio)
	os.system("sudo a2ensite %s" % nom_dominio)
