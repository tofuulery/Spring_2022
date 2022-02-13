# Kelly Partin - Lab 2
# Question 1:

# import datetime as dt
# import random
#
#
# class Emergency(object):
# 	emg_type = ''
# 	address = ''
# 	caller = ''
# 	date_time = dt.datetime.now().strftime("%Y/%m/%d, %H:%M:%S")
# 	x = random.randint(-90, 90)
# 	y = random.randint(-180, 180)
# 	z = random.randint(0, 100)  # Not sure how the z figures into an emergency call, so I am using range of 0-100.
# 	coords = str((x, y, z))
#
# 	def __init__(self):
# 		pass
#
# 	def set_emg_type(self, emg_t_pe):
# 		self.emg_type = emg_t_pe
#
# 	def set_address(self, addr_ss):
# 		self.address = addr_ss
#
# 	def set_caller(self, c_llr):
# 		self.caller = c_llr
#
# 	def gen_message(self):
# 		messg = str(
# 			self.emg_type + ' at ' + self.address + '. Caller: ' + self.caller + ', ' + self.date_time+ ', ' + 'Location: ' + self.coords)
# 		print(messg)
#
#
# def main():
# 	mayday = Emergency()
# 	mayday.set_emg_type('Fire')
# 	mayday.set_address('2222 W Hickory St, Denton TX')
# 	mayday.set_caller('(800) 867-5309')
# 	mayday.gen_message()
#
#
# if __name__ == '__main__':
# 	main()

# Lab2 - Kelly Partin
import random

outfile = open(r"C:\temp\lab2_deskpts.txt", "w")
# write 'headers'
outfile.write("ID, X, Y, Z" + "\n")

# Counter for number of points
i = 0
# assume this table is level, at 1.2m tall
z = 1.2
while i < 2000:
    x = random.uniform(0, 1.5)
    y = random.uniform(0, 3.6)
    outString = str(i) + "," + str(x) + "," + str(y) + "," + str(z)
    outfile.write(outString + "\n")
    i += 1

outfile.close()
print('Finished!')
