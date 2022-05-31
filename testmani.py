import os
import re
# import subprocess

def trans_event(strr,list):      #event in event_set?
	for k in range(0,len(list)):
		if strr==list[k]:
			return str(k)
	return "null"


def trans_guard(str):
	s = str[1]+" "
	if str[2]=='=':
		s = s+str.split('=')[1]+" 0 "
	else:
		if str[2]=='>':
			if str[3]=='=':
				s = s+str.split('=')[1]+" 3      "
			else:
				s = s+str.split('>')[1]+" 1 "
		else:
			if str[3]=='=':
				s = s+str.split('=')[1]+" 4 "
			else:
				s = s+str.split('<')[1]+" 2 "
	return s

def trans_reset(strr,l):
	s = ""
	for k in range(1,l+1):
		if str(k) in strr:
			s = s+"1 "
		else:
			s = s+"0 "
	return s


l_e_ob = []
l_e_no = []
file = open("modeleg.txt","r")
f_t = open("test_trans.txt","w")
# with open ('test_nothing.txt','w') as f_n:
# 	f_n.write(file.read())
# # print(fff.read())
line = file.readline()  #读一行 model.txt
bound = int(line.split(' ')[1])-1 #split:以空格分割，放入一个列表 　bound值是model里面bound－1
delta = 0.0
nb_c = 0
bound_limit = 0
list_obs = []
list_uno = []
list_fau = []
list_total = []
model = 1
# if len(line.split(' '))==4: #quand il n'y a pas de contraint de clock event ...
# 	delta = float(line.split(' ')[3].split("\n")[0])
# 	line = file.readline()
# 	while line:
# 		a = line.split(' ')
# 		if len(a[len(a)-1]) > 1:
# 		 	a[len(a)-1] = a[len(a)-1].split("\n")[0]
# 		f_t.write(a[0]+" "+a[len(a)-1]+" ") #etat original et etat destinaire
# 		t_e = trans_event(a[2])
# 		if int(t_e)>0:
# 			if t_e not in l_e_ob:
# 				l_e_ob.append(t_e)
# 		elif int(t_e)<0:
# 			if t_e not in l_e_no:
# 				l_e_no.append(t_e)
# 		f_t.write(t_e+" ")
# 		#apres c'est le traitement de a[1] et a[3]
# 		list_c = a[1].split(';')
# 		nb_c = len(list_c) #nombre de clock
# 		for i in range(0,len(list_c)):
# 			if '&' in list_c[i]:
# 				b = list_c[i].split('&')
# 				f_t.write(trans_guard(b[0]))
# 				f_t.write(trans_guard(b[1]))
# 			else:
# 				f_t.write(trans_guard(list_c[i]))
# 				f_t.write(str(i+1)+" 0 3 ")
# 		if len(a)==5:
# 			f_t.write(trans_reset(a[3],len(list_c)))
# 		else:
# 			for i in range(0,len(list_c)):
# 				f_t.write("0 ")
# 		f_t.write("\n")
# 		line = file.readline()
# 	print(l_e_ob,l_e_no)
# if len(line.split(' '))>4: #quand il y a le contraint de clock event ...
# 	if len(line.split(' '))==5:#/////////////////////////////////////////////////////////////////
# 		s = line.split(' ')[4].split('\n')[0]
# 		if s.split("={")[0]=="observable":
# 			list_obs = s.split("={")[1].split("}")[0].split(",")
# 		elif s.split("={")[0]=="unobservable":
# 			list_uno = s.split("={")[1].split("}")[0].split(",")

# 	if len(line.split(' '))==6:
# 		s1 = line.split(' ')[4]
# 		s2 = line.split(' ')[5].split('\n')[0]
# 		list_obs = s1.split("={")[1].split("}")[0].split(",")
# 		list_uno = s2.split("={")[1].split("}")[0].split(",")
# 	print("asas")


#on suppose qu'il faut definir tous les parametres dans la premiere ligne

s1 = line.split(' ')[6]   #observable = {ob1,ob2,ob3}
s2 = line.split(' ')[7]   #unobservable = {un1,un2}
s3 = line.split(' ')[8].split('\n')[0]  #避免最后一行读入换行符
list_obs = s1.split("={")[1].split("}")[0].split(",")  #['ob1', 'ob2', 'ob3']
list_uno = s2.split("={")[1].split("}")[0].split(",")   #['un1', 'un2']
list_fau = s3.split("={")[1].split("}")[0].split(",")   #['f1', 'f2']
list_total = list_obs+list_uno+list_fau  #['ob1', 'ob2', 'ob3', 'un1', 'un2', 'f1', 'f2']

bound_limit = int(line.split(' ')[3])
delta = line.split(' ')[5]
if delta=="infinite":
	delta = float("99999")
else:
	delta = float(delta)
line = file.readline() # 读入第二行。。。
while line:
	a = line.split(' ')
    if len(a[len(a)-1]) > 1:  #最后一个数的长度大于1(终态数字和换行符)，有换行符
        a[len(a)-1] = a[len(a)-1].split("\n")[0]  #去掉换行符
	f_t.write(a[0]+" "+a[len(a)-1]+" ") #etat original et etat destinaire 写入路径的初态和终态
    t_e = trans_event(a[2],list_total)  #a[2]:event  list_total: all event  t_e:event在eventset在list_totla里面的下标
	# if int(t_e)>0:
	# 	if t_e not in l_e_ob:
	# 		l_e_ob.append(t_e)
	# elif int(t_e)<0:
	# 	if t_e not in l_e_no:
	# 		l_e_no.append(t_e)
    f_t.write(t_e+" ") #write 事件下标
	#apres c'est le traitement de a[1] et a[3]
    list_c = a[1].split(';') #clock[],if the number of clocks more than one, prsent it by x;x, thir code is clean ";"
	nb_c = len(list_c) #nombre de clock; number of clock
	for i in range(0,len(list_c)):
		if '&' in list_c[i]:
			b = list_c[i].split('&')
			f_t.write(trans_guard(b[0]))
			f_t.write(trans_guard(b[1]))
		else:
			f_t.write(trans_guard(list_c[i]))
			f_t.write(str(i+1)+" 0 3 ")
	if len(a)==5:
		f_t.write(trans_reset(a[3],len(list_c)))
	else:
		for i in range(0,len(list_c)):
			f_t.write("0 ")
	f_t.write("\n")
	line = file.readline()
# print(l_e_ob,l_e_no)
# print(list_total)

file.close()
f_t.close()





file = open("test_trans.txt","r")
line = file.readlines()
nb_trans = len(line)

f_smt = open("test.smt","w")

f_smt.write("; model\n\n(declare-datatypes (T1 T2) ((Pair (mk-pair (first T1) (second T1) (third T1)")
for k in range(1,2*nb_c+1):
	f_smt.write(" (fourth"+str(k)+" T1) (fourfifth"+str(k)+" T2) (fifth"+str(k)+" T1)")
for k in range(1,nb_c+1):
	f_smt.write(" (sixth"+str(k)+" T1)")

f_smt.write("))))\n\n(declare-fun trS (Int) (Pair Int Real))\n\n(declare-const p0 (Pair Int Real))\n(assert (= (first p0) 0))\n\n(define-fun trM ((x Int)) (Pair Int Real)\n  (if (and (<= x "+str(nb_trans)+") (> x 0))\n    (trS x)\n    p0))\n\n(define-fun obs ((o Int)) Bool\n  (if (and (>= o 0) (< o "+str(len(list_obs))+"))\n    true\n    false))\n\n")

for i in range(0,nb_trans):
	l = line[i].split(' ')
	f_smt.write("(declare-const p"+str(i+1)+" (Pair Int Real))\n(assert (= (first p"+str(i+1)+") "+l[0]+"))\n(assert (= (second p"+str(i+1)+") "+l[1]+"))\n(assert (= (third p"+str(i+1)+") "+l[2]+"))\n")
	for k in range(1,2*nb_c+1):
		f_smt.write("(assert (= (fourth"+str(k)+" p"+str(i+1)+") "+l[3*k]+"))\n(assert (= (fourfifth"+str(k)+" p"+str(i+1)+") "+l[3*k+1]+"))\n(assert (= (fifth"+str(k)+" p"+str(i+1)+") "+l[3*k+2]+"))\n")
	for k in range(0,nb_c):
		f_smt.write("(assert (= (sixth"+str(k+1)+" p"+str(i+1)+") "+l[6*nb_c+3+k]+"))\n")
	f_smt.write("(assert (= (trS "+str(i+1)+") p"+str(i+1)+"))\n\n")

f_smt.write("; diagnosability property\n; Initial state\n\n")
for k in range(1,nb_c+1):
	f_smt.write("(declare-fun clock"+str(k)+" (Int) Real)\n(declare-fun clockFault"+str(k)+" (Int) Real)\n")
f_smt.write("(declare-fun clockG (Int) Real)\n(declare-fun clockGF (Int) Real)\n(declare-fun loc (Int) Int)\n(declare-fun locFault (Int) Int)\n(declare-fun isFault (Int) Int)\n")
for k in range(1,nb_c+1):
	f_smt.write("(assert (= (clock"+str(k)+" 0) 0.0))\n(assert (= (clockFault"+str(k)+" 0) 0.0))\n")
f_smt.write("(assert (= (clockG 0) 0.0))\n(assert (= (clockGF 0) 0.0))\n(assert (=(loc 0) 1))\n(assert (=(locFault 0) 1))\n(declare-const firstF Int)\n\n\n;well-formedness\n\n(declare-fun delay (Int) Real)\n(declare-fun delayFault (Int) Real)\n(declare-fun even (Int) Int)\n(declare-fun evenFault (Int) Int)\n")

for k in range(0,bound+1):
	f_smt.write("(assert (>= (delay "+str(k)+") 0.0))\n(assert (and (>= (even "+str(k)+") 0) (< (even "+str(k)+") "+str(len(list_total))+")))\n\n")
for k in range(0,bound+1+bound_limit):
	f_smt.write("(assert (>= (delayFault "+str(k)+") 0.0))\n(assert (and (>= (evenFault "+str(k)+") 0) (< (evenFault "+str(k)+") "+str(len(list_total))+")))\n\n")
f_smt.write("(define-fun event ((e1 Int)) Int\n  (if (and (<= e1 "+str(bound)+") (>= e1 0))\n    (even e1)\n    0))\n\n(define-fun eventFault ((e2 Int)) Int\n  (if (and (<= e2 "+str(bound+bound_limit)+") (>= e2 0))\n    (evenFault e2)\n    0))\n\n;acceptance\n\n")

for k in range(1,nb_c+1):
	f_smt.write("(define-fun prog"+str(k)+" ((res"+str(k)+" Int) (s Int)) Bool\n  (if (= res"+str(k)+" 1)\n    (= (clock"+str(k)+" (+ s 1)) 0)\n    (= (clock"+str(k)+" (+ s 1)) (+ (clock"+str(k)+" s) (delay s)))))\n\n")
f_smt.write("(define-fun progress (")
for k in range(1,nb_c+1):
	f_smt.write("(res"+str(k)+" Int) ")
f_smt.write("(s Int)) Bool\n    (and (= (clockG (+ s 1)) (+ (clockG s) (delay s)))")
for k in range(1,nb_c+1):
	f_smt.write(" (= (prog"+str(k)+" res"+str(k)+" s) true)")
f_smt.write("))\n\n")

for k in range(1,nb_c+1):
	f_smt.write("(define-fun progF"+str(k)+" ((res"+str(k)+" Int) (s Int)) Bool\n  (if (= res"+str(k)+" 1)\n    (= (clockFault"+str(k)+" (+ s 1)) 0)\n    (= (clockFault"+str(k)+" (+ s 1)) (+ (clockFault"+str(k)+" s) (delayFault s)))))\n\n")
f_smt.write("(define-fun progressF (")
for k in range(1,nb_c+1):
	f_smt.write("(res"+str(k)+" Int) ")
f_smt.write("(s Int)) Bool\n    (and (= (clockGF (+ s 1)) (+ (clockGF s) (delayFault s)))")
for k in range(1,nb_c+1):
	f_smt.write(" (= (progF"+str(k)+" res"+str(k)+" s) true)")
f_smt.write("))\n\n")

f_smt.write("(define-fun guard ((con Real) (comp Int) (cl Real)) Bool\n  (if (= comp 3)\n    (>= cl con)\n    (if (= comp 1)\n      (> cl con)\n      (if (= comp 2)\n        (< cl con)\n        (<= cl con)))))\n\n(define-fun sat ((d Int) (s Int)) Bool\n  (and")
for k in range(1,2*nb_c+1):
	f_smt.write(" (guard (fourfifth"+str(k)+" (trM s)) (fifth"+str(k)+" (trM s)) (+ (clock"+str(int((k-1)/2+1))+" d) (delay d)))")
f_smt.write("))\n\n(define-fun satFault ((d Int) (s Int)) Bool\n   (and")
for k in range(1,2*nb_c+1):
	f_smt.write(" (guard (fourfifth"+str(k)+" (trM s)) (fifth"+str(k)+" (trM s)) (+ (clockFault"+str(int((k-1)/2+1))+" d) (delayFault d)))")
f_smt.write("))\n\n")

for k in range(0,bound+1):
	f_smt.write("(assert (exists ((j Int)) (and (>= j 1) (<= j "+str(nb_trans)+") (= (first (trM j)) (loc "+str(k)+")) (= (sat "+str(k)+" j) true) (= (event "+str(k)+") (third (trM j))) (= (progress")
	for j in range(1,nb_c+1):
		f_smt.write(" (sixth"+str(j)+" (trM j))")
	f_smt.write(" "+str(k)+") true) (= (loc (+ "+str(k)+" 1)) (second (trM j))))))\n\n")

for k in range(0,bound+1+bound_limit):
	f_smt.write("(assert (exists ((jf Int)) (and (>= jf 1) (<= jf "+str(nb_trans)+") (= (first (trM jf)) (locFault "+str(k)+")) (= (satFault "+str(k)+" jf) true) (= (eventFault "+str(k)+") (third (trM jf))) (= (progressF")
	for j in range(1,nb_c+1):
		f_smt.write(" (sixth"+str(j)+" (trM jf))")
	f_smt.write(" "+str(k)+") true) (= (locFault (+ "+str(k)+" 1)) (second (trM jf))))))\n\n")

f_smt.write("; fault-normal\n\n(define-fun existF((fau Int)) Bool\n  (if(and (>= (eventFault fau) "+str(len(list_obs)+len(list_uno))+") (< (eventFault fau) "+str(len(list_total))+"))\n true false))\n\n(assert (or")
for k in range(0,bound):
	f_smt.write(" (existF "+str(k)+")")
f_smt.write("))\n\n")


f_smt.write("(check-sat)\n(get-model)\n(get-info :all-statistics)\n")

file.close()
f_smt.close()
os.system("z3 -smt2 test.smt > result.txt")

re = open("result.txt", "r")
l_re = re.readlines()
re.close()
if l_re[0]!='sat\n':
	print("UNSAT! Please increase the Bound.")
else:
	os.system("python3 verification.py")