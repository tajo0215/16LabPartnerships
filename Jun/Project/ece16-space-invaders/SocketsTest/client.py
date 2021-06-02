import socket, pygame

host = "127.0.0.1"
port = 65432
mySocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
mySocket.connect((host, port))
mySocket.setblocking(False)

pygame.init()
pygame.display.set_caption(u"Keyboard Events")
pygame.display.set_mode((320, 240))

while True:
  event = pygame.event.wait()

  if event.type == pygame.QUIT: # close button in figure
    break

  if event.type == pygame.KEYDOWN:

    if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
      break

    if event.key == pygame.K_LEFT:
      mySocket.send("LEFT".encode("utf-8"))
    if event.key == pygame.K_RIGHT:
      mySocket.send("RIGHT".encode("utf-8"))
    if event.key == pygame.K_UP:
      mySocket.send("UP".encode("utf-8"))
    if event.key == pygame.K_DOWN:
      mySocket.send("DOWN".encode("utf-8"))

  try:
    data = mySocket.recv(1024)
    data = data.decode("utf-8")
    print("Response: " + data)
  except BlockingIOError:
    pass # do nothing if there's no data

mySocket.close()
pygame.quit()
