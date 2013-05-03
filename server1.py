import sys,getopt
import os
import socket
import string
import struct
import threading
from threading import Thread
from time import sleep


mutual_lock=threading.Lock()
MCAST_GRP = '224.1.1.1'
#MCAST_GRP = '127.0.0.1'
MCAST_PORT = 5007
chat_name="surendra"

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "m:p:n:",['multicast','port','name'])
    except getopt.GetoptError:
        os._exit(1)

    for o,a in opts:
        if o in ("-m"):
	    global MCAST_GRP
            MCAST_GRP = a
        elif o in ("-p"):
	    global MCAST_PORT
            MCAST_PORT = int(a)
        elif o in ("-n"):
	    global chat_name
            chat_name = a

if __name__ == "__main__":
    main()

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)  # for sending msg

sock.bind(('', MCAST_PORT))
mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)

sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

msg= chat_name+"\@/**************** "+string.upper(chat_name)+ " has joined the room **********************\@/welcome"
sock.sendto(msg.strip(), (MCAST_GRP, MCAST_PORT))

def interrupt():
	import sys, tty, termios

	fd = sys.stdin.fileno()
	# save original terminal settings 
	old_settings = termios.tcgetattr(fd)

	# change terminal settings to raw read
	try:
		tty.setraw(sys.stdin.fileno())
		ch = sys.stdin.read(1)
	# restore original terminal settings 
	finally:
		termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
	return ch;
        



def receive_msg(sock):
	while True:
  		msg,(addr,port) =sock.recvfrom(10240)
		if(msg):
			try:
				mutual_lock.acquire()
				msg=msg.split('\@/')
				if not (msg[0] == chat_name):
					if not (msg[2]):
						print string.upper(msg[0])+" <<< "+msg[1]
					else:
						print msg[1]
			finally:
				mutual_lock.release()
		print "\r"

if __name__ == "__main__":
    main()

if __name__ == "__main__":
    thread = Thread(target = receive_msg, args = (sock, ))
    thread.start()
    #print "thread finished...exiting"

print "################################ WELCOME TO CHAT ROOM #####################################"

while 1:
	ch_val = '';
	ch_val = interrupt();
	if(ch_val):
		try:
			mutual_lock.acquire()
			
			msg=raw_input("ME >>> ")
			if(msg == "quit"):
				print " BYE !! "
				msg= chat_name+"\@/**************** "+string.upper(chat_name)+ " has left the room **********************\@/action"
				sock.sendto(msg.strip(), (MCAST_GRP, MCAST_PORT))
				os._exit(1)
				 
			if msg:
				msg= chat_name+"\@/"+msg+"\@/"
				sock.sendto(msg.strip(), (MCAST_GRP, MCAST_PORT))
			
			
		finally:
			mutual_lock.release()
	
	#print "\r"
