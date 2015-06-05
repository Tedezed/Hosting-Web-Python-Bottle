f_cont = open("contador_id","r")
id_num = f_cont.read()
id_sum = str(int(id_num) + 1)
f_cont.close()
f_cont = open("contador_id","w")
f_cont.write(id_sum)
f_cont.close()
print id_num
print id_sum