#!/usr/bin/env python3

import socket

# Setup
dev = "192.168.178.69" # your G-Homa plug IP address (check on your router)
ctrl = "192.168.178.21" # your control server IP address
port = 4196           # port on the control server (default: 4196)

# No changes beyond this line

devport = 48899      # udp port of G-Homa
ctrl_default = "plug.g-homa.com" # the default server address
hello = "HF-A11ASSISTHREAD"

# enable this to restore the default
# ctrl = ctrl_default

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(('', 48899))

def send(msg):
	print('Sending: {}'.format(msg))
	sock.sendto(msg.encode('utf-8'), (dev, devport))

def recv():
	while True:
		data, addr = sock.recvfrom(1024)
		text = data.decode('ascii')
		print('Received data from addr {}'.format(addr))
		print('data = {}'.format(text))
		if (text != '+ERR=-1'):
			return text

send(hello)

ip, id, name = recv().strip().split(',')
print('ip = {}'.format(ip))
print('id = {}'.format(id))
print('name = {}'.format(name))

send('+ok')
recv()

# set to True to display help page
help = False

if (help):
	send('AT+H\r')
	for i in range(0, 65):
		recv()
		print("i = {}".format(i))

send('AT+NETP\r')
recv()

send('AT+VER\r')

data = recv().strip().split(',')
if (len(data) == 1):
	print('Error: {}'.format(data))
else:
	ok, what, version = data
	print('ok = {}'.format(ok))
	print('what = {}'.format(what))
	print('version = {}'.format(version))

send('AT+NETP=TCP,Client,{},{}\r'.format(port, ctrl))
recv()

send('AT+NETP\r')
recv()
