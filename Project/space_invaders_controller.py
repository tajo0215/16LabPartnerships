"""
Final Project 1: Grand Challenge
@author: Jun Park (A15745118)
"""

from ECE16Lib.Communication import Communication
from re import search
from time import sleep
import socket, pygame

# Setup the Socket connection to the Space Invaders game
host = "127.0.0.1"
port = 65432
mySocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
mySocket.connect((host, port))
mySocket.setblocking(False)

class PygameController:
  pause = None
  comms = None

  def __init__(self, serial_name, baud_rate):
    self.comms = Communication(serial_name, baud_rate)
    self.pause = False

  def receiveMessage(self):
    msg = None

    try:
      msg, _ = mySocket.recvfrom(1024)
      msg = msg.decode('utf-8')
    except BlockingIOError:
      pass

    return msg

  def run(self):
    # 1. make sure data sending is stopped by ending streaming
    self.comms.clear()
    sleep(.3)
    self.comms.send_message("stop")

    # 2. start streaming orientation data
    input("Ready to start? Hit enter to begin.\n")
    self.comms.send_message("start")

    # 3. Forever collect orientation and send to PyGame until user exits
    print("Use <CTRL+C> to exit the program.\n")
    while True:
      message = self.comms.receive_message()
      if(message != None):
        command = None
        message = int(message)
        #if message == 0:
        #   command = "FLAT"
        # if message == 1:
        #   command = "PAUSE"
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

        elif message == 10:
          command = "QUIT"

        elif message == 11:
          if self.pause:
            command = "RESUME"
            self.pause = False
          else:
            command = "PAUSE"
            self.pause = True
            self.comms.send_message("pause")

        if command is not None:
          mySocket.send(command.encode("UTF-8"))

        socketMsg = self.receiveMessage()
        if socketMsg == "BUZZ":
          self.comms.send_message("buzz")
          print("Enemy Hit")
        elif socketMsg == "Ending...":
          self.comms.send_message(socketMsg)
          print(socketMsg)
        elif socketMsg != None:
          if "Score" in socketMsg:
            print(socketMsg)
            self.comms.send_message(socketMsg)
          if "Lives" in socketMsg:
            print(socketMsg)
            self.comms.send_message(socketMsg)
          elif "TS" in socketMsg:
            print(socketMsg)
            self.comms.send_message(socketMsg)
        

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