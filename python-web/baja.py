def baja_apache_bind(nom_dominio):
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

	#SQL/DML
	select_usuario_db = 'select username from usuarios where dominio = "%s";' % nom_dominio
	com_local = "sed '/zone " + '"%s"'% nom_dominio + "/,/};/d' /etc/bind/named.conf.local > temporal"

	#Conexion DB
	con_mysql = MySQLdb.connect(host=host_db, user=user_db, passwd=pass_db, db=nom_db)
	cursor = con_mysql.cursor()
	cursor.execute(select_usuario_db)
	nom_usuario = cursor.fetchone()
	if nom_usuario != None:
		#Apache
		print nom_usuario
		os.system("rm -rf /var/www/%s" % nom_dominio)
		os.system("sudo a2dissite %s > /dev/null" % nom_dominio)
		os.system("sudo a2dissite php_%s > /dev/null" % nom_dominio)
		os.system("rm -rf /etc/apache2/sites-available/%s" % nom_dominio)
		os.system("rm -rf /etc/apache2/sites-available/php_%s" % nom_dominio)
		os.system("rm -rf /var/cache/bind/db.%s" % nom_dominio)
		os.system(com_local)
		os.system("mv temporal /etc/bind/named.conf.local")
		return nom_usuario
	else:
		return 0

def baja_ftpd_mysql(nom_usuario):
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
	drop_db = 'drop database %s' % nom_usuario
	drop_db_user = ' drop user %s@localhost' % nom_usuario
	drop_user_ftp = "delete FROM usuarios WHERE username = '%s';" % (nom_usuario)

	#Conexion DB
	con_mysql = MySQLdb.connect(host=host_db, user=user_db, passwd=pass_db)
	cursor = con_mysql.cursor()
	cursor.execute('use ftpd;')
	cursor.execute(drop_db_user)
	cursor.execute(drop_db)
	cursor.execute(drop_user_ftp)
	con_mysql.commit()

	#Borrar directorio FTP
	os.system('mkdir /var/www/%s' % nom_usuario)