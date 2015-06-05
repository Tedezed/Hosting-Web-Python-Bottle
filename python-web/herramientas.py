def id_generator(size):
    import random
    chars = 'ABCDEFZYTHSX0123456789'
    pass_final = ''
    rango = range(size)
    for i in rango:
        pass_final = pass_final + random.choice(chars)
    return pass_final

def plantilla_generator(plantilla,param1):
    #!/usr/bin/env python
    # -*- coding: utf-8 -*-
    ruta = '/var/www/python-web/plantillas/%s.tl' % plantilla

    f_plantilla=open(ruta,"r")
    list_plantilla=f_plantilla.read()
    f_plantilla.close()
    list_plantilla=list_plantilla.replace("&dom&","%s" % param1)
    return list_plantilla

def gestion_dns(parametro,param1,param2):
    #!/usr/bin/env python
    # -*- coding: utf-8 -*-
    import re
    import sys
    import commands
    #Para anadir: gestion_dns('-a','inma','correo', '/')
    #Para borrar: gestion_dns('-b','inma','', '/etc/')

    #Metodo para anadir
    def addnoob(ruta,metodo,param1,param2):
        f = open (ruta, "a")
        f.write(param1 + "      IN  " + metodo + "  " + param2 + "\n")
        f.close()

    #Metodo para borrar
    def delnoob(ruta,re_ex):
        directo = open(ruta,"r")
        list_directo = directo.readlines()
        contador = 0
        list_id_list = []
        for x in list_directo:
            ex_1 = re_ex
            parametro_encontrado = re.findall(ex_1, x)
            if parametro_encontrado != []:
                list_id_list.append(contador)
            contador += 1
        contador = 0
        for x in list_id_list:
            x_final = x-contador
            del list_directo[x_final]
            contador += 1
            final = ''
        try:
            for x in list_directo:
                final = final + x
                f = open (ruta, "w")
                f.write(final)
                f.close()
            print "Parametro encontrado y borrado."
        except:
            print "ERROR-0001: No se encontro el parametro para eliminar."
            final = ''
        print ".................................."
        directo.close()

    #Ejecucion
    #Metodo -a para aniadir
    if parametro == "-a":
        metodo = "CNAME"
        addnoob(ruta,metodo,param1,param2)
        print "Anadido %s %s %s" % (metodo, param1, param2)

    #Metodo -b para borrar
    elif parametro == "-b":
        print "Zona Directa:"
        ex_para_del = "^" + param1
        delnoob(ruta,ex_para_del)

def reinicios():
    #!/usr/bin/env python
    # -*- coding: utf-8 -*-
    import os
    
    list_servicios = ['apache2', 'bind9']
    list_restart = ['proftpd']
    
    for i in list_servicios:
        com = 'sudo service %s reload' % i
        os.system(com)

    for i in list_restart:
        com = 'sudo service %s restart' % i
        os.system(com)