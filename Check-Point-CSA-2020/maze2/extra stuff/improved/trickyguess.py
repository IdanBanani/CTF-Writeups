import socket
import random
import time

# read the words from the file:
file = open("words.txt","r")
words = file.readlines()

# create a stocket to connect the server:
s = socket.socket()
host = "tricky-guess.csa-challenge.com"
port = 2222
s.connect((host,port))

# to track connection
connected = True

# set connection count to 1 
c_count = 1
print("Connection number:", c_count)

# starting time
start_time1 = time.time()

# start connection loop
while True:
  
  # starting time of the connection
  start_time2 = time.time()
  try:
    # waiting for the message to be recieved:
    s.recv(1024)
    s.recv(10)
    for i in range(15):
    
      # sending a word to the server
      guess = random.choice(words)
      s.send(str.encode(guess))

      # receving the server respond
      resp = (s.recv(1024)).decode("utf-8")
      print("#" + str(i+1) + ':', resp, end="")

    s.close()

    print("----------------------------")
    r_time = time.time() - start_time2
    t_time = time.time() - start_time1
    a_time = t_time / c_count
    print(" Time: %s seconds" % (r_time))
    print(" Total time: %s seconds" % round((t_time), 2))
    print(" Average time per connection: %s seconds" % round(a_time))
    print("----------------------------")
    print("")

  except socket.error:
    connected = False

    s = socket.socket()
    while not connected:

      try:
        s.connect((host,port))

        c_count += 1
        print("Connection number:",c_count)

        connected = True
        
      except socket.error:
        print("...")

s.close()