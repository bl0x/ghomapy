#!/usr/bin/env python3

import socket
from threading import Thread
import time
import sys

port = 4196

pre = [0x5a, 0xa5]
post = [0x5b, 0xb5]

init1a = [0x02, 0x05, 0x0d, 0x07, 0x05, 0x07, 0x12]
init1b = [0x02]
init2 = [0x05, 0x01]
heartbeat_reply = [0x06]

OFF = 'off'
ON = 'on'

do_switch = 0
new_state = OFF

cmd = {
	'init1_reply': 0x03,
	'init2_reply': 0x07,
	'heartbeat': 0x04,
	'status': 0x90,
	'measure': [0xff, 0xfe, 0x01, 0x81, 0x39, 0x00, 0x00, 0x01]
}

def usage():
	print('usage: {} [on|off]'.format(sys.argv[0]))

def send(sock, what, data):
	# print('Sending {} data = {}'.format(what, bytes2str(data)))
	sock.send(data)

def init(sock):
	send(sock, 'init1', pack(init1a) + pack(init1b))

def bytes2str(data):
	return ''.join('{:02x}'.format(x) for x in data)

def switch(client, g, state_name, state):
	send(client, state_name, pack(
		[0x10, 0x01, 0x01, 0x0a, 0xe0] +
		g['trg'] +
		g['shortmac'] +
		[0xff, 0xfe, 0x00, 0x00,
		 0x10, 0x11, 0x00, 0x00,
		 0x01, 0x00, 0x00, 0x00,
		 state])
	)

def switch_on(client, g):
	switch(client, g, 'on', 0xff)

def switch_off(client, g):
	switch(client, g, 'off', 0x00)

def checksum(data):
	return [0xff - (sum(data) & 0xff)]

def pack(data):
	length = [int(len(data) / 256), len(data) & 0xff]
	chk = checksum(data)
	return bytearray(pre + length + data + chk + post)

def unpack(data):
	if len(data) == 0:
		return None, None

	msg = {}

	if (list(data[0:2]) != pre):
		print('Wrong prefix')

	msg['length'] = data[2] * 256 + data[3]

	if (list(data[5 + msg['length']:7 + msg['length']]) != post):
		print('Wrong postfix')

	msg['chk'] = data[-3]
	msg['data'] = data[4:4 + msg['length']]
	msg['cmd'] = msg['data'][0]

	chk = checksum(msg['data'])[0]
	
	# if (msg['chk'] != chk):
		# print('Wrong checksum ({} != {})'.format(msg['chk'], chk))
	
	return msg, data[7 + msg['length']:]

def handler(client, addr, do_switch):
	init(client)

	g = {}
	g['init_ok'] = 0

	while 1:
		data = client.recv(1024)
		if not data: break
		# print('----------------')
		# print('{} recv: {}'.format(addr, bytes2str(data)))

		msg, rest = unpack(data)

		while msg is not None:
		
			if msg['cmd'] == cmd['init1_reply']:
				# print('  -- init1 reply')
				g['shortmac'] = list(msg['data'][6:9])
				g['id'] = bytes2str(msg['data'][6:9])
				g['trg'] = list(msg['data'][4:6])
				g['init_ok'] = 1

				send(client, 'init2', pack(init2))

			elif msg['cmd'] == cmd['init2_reply']:
				# print('  -- init2 reply')
				mac = list(msg['data'][-6:])
				if mac[3:] == g['shortmac']:
					g['fullmac'] = bytes2str(mac)
				else:
					g['version'] = mac[3:]

			elif msg['cmd'] == cmd['status']:
				# print('  -- status')
				if msg['data'][-1] == 0xff:
					g['status'] = 'on'
				else:
					g['status'] = 'off'
				print('status = {}'.format(g['status']))
				if do_switch == 0:
					return

			elif msg['cmd'] == cmd['heartbeat']:
				# print('  -- heartbeat')
				g['last_seen'] = time.time()
				send(client, 'heartbeat', pack(heartbeat_reply))

			# else:
				#print('!! msg = {}'.format(msg))

			msg, rest = unpack(rest)

		# print('  g = {}'.format(g))

		if do_switch == 1 and g['init_ok'] == 1:
			if new_state == ON:
				switch_on(client, g)
			else:
				switch_off(client, g)
			do_switch = 0
			return


	client.close()

if len(sys.argv) == 2:
	do_switch = 1
	if (sys.argv[1] == ON):
		new_state = ON

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('', port))
s.listen(5)

# print('waiting for connection on port {}'.format(port))
client, addr = s.accept()
# print('connection from: {}'.format(addr))
t = Thread(target=handler, args=(client, addr, do_switch))
t.start()
t.join()
