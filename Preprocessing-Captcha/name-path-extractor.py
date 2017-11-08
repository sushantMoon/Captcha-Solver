import os 

path = "/media/feliz/Safira/GitHub/Captcha-Solver/Data/PrivateCircle/Captchas/"
listPics = "/media/feliz/Safira/GitHub/Captcha-Solver/Data/PrivateCircle/names.txt"

for i in os.listdir(path):
	if len(i) > 1 :
		with open(listPics , 'a') as f:
			f.write(path + str(i) + '\n')
		