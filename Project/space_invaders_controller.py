"""
@author: Ramsin Khoshabeh
"""

from ECE16Lib.Communication import Communication
from time import sleep
import socket, pygame

# Setup the Socket connection to the Space Invaders game
host = "127.0.0.1"
port = 65432
mySocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
mySocket.connect((host, port))
mySocket.setblocking(False)

class PygameController:
	comms = None
	pause = None

	def __init__(self, serial_name, baud_rate):
		self.comms = Communication(serial_name, baud_rate)
		self.pause = False

	def receieveMessage(self):
		msg = None

		try:
			msg, _ = mySocket.recvfrom(1024)
			msg = msg.decode('utf-8')
		except BlockingIOError as e:
			pass

		return msg

	def run(self):
		# 1. make sure data sending is stopped by ending streaming
		self.comms.clear()
		sleep(.5)
		self.comms.send_message("stop")

		# 2. start streaming orientation data
		input("Ready to start? Hit enter to begin.\n")
		self.comms.send_message('start')

		# 3. Forever collect orientation and send to PyGame until user exits
		print("Use <CTRL+C> to exit the program.\n")
		while True:
			message = self.comms.receive_message()
			if(message != None):
				command = None
				message = int(message)
				# if message == 0:
				#   command = "FLAT"
				# if message == 1:
				#   command = "UP"
				if message == 2:
					command = "FIRE"
				elif message == 3:
					command = "LEFT"
				elif message == 4:
					command = "LEFTx2"
				elif message == 5:
					command = "LEFTx3"
				elif message == 6:
					command = "RIGHT"
				elif message == 7:
					command = "RIGHTx2"
				elif message == 8:
					command = "RIGHTx3"
				elif message == 9:
					command = "FIRE"
					try:
						msg = mySocket.recv(1024)
						msg = msg.decode('utf-8')
						print(msg)
						self.comms.send_message(msg)
					except:
						pass
				elif message == 10:
					command = "QUIT"
				elif message == 11:
					if self.pause:
						command = "UNPAUSE"
						self.pause = False
					else:
						command = "PAUSE"
						self.pause = True
						self.comms.send_message("pause")
				if command is not None:
					mySocket.send(command.encode("UTF-8"))

				arduinoMsg = self.receieveMessage()

				if arduinoMsg == "BUZZ":
					self.comms.send_message("buzz")
				elif arduinoMsg == "quit":
					self.comms.send_message("quit")



if __name__== "__main__":
	serial_name = "COM5"
	baud_rate = 115200
	controller = PygameController(serial_name, baud_rate)

	try:
		controller.run()
	except(Exception, KeyboardInterrupt) as e:
		print(e)
	finally:
		print("Exiting the program.")
		controller.comms.send_message("stop")
		controller.comms.close()
		mySocket.send("QUIT".encode("UTF-8"))
		mySocket.close()

	input("[Press ENTER to finish.]")
