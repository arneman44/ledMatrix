#this code builds a byte array from hex values and sends it UDP to the dmx/ethernet bridge, an ENTTEC OPENDMX

import socket

UDP_IP = "192.168.1.230"  #ip for the dmx/ethernet bridge
UDP_PORT = 6454
test_array = bytearray([0x41,0x72,0x74,0x2d,0x4e,0x65,0x74,0x00,0x00,0x50,0x00,0x0e,0x00,0x01,0x00,0x00,0x02,0x00,0x8])

array_to_send = ''.join([
	"Art-Net\x00",
	"\x00P",
	"\x00", "\x0e",
	"\x00",
	"\x00",
	"\x00", "\x00",
	"\x02", "\x00",
	"\x08", "\xff", "\xff", #channel 1,2,3
	"\x00", "\x00", "\xff", "\x00", "\x00", "\x00","\x00", "\x00", #channels 4-11
	"\x09", "\x00", "\x00", #channel 12,13,14
	"\x09", "\xc5", "\x00", #channle 15,16,17
	"".join(["\x09"] * 495) #writes to remaining channels, 512 total
])

print(''.join(["\x00", "\x00", "\xff", "\x00", "\x00", "\x00","\x00", "\x00"]))
print(array_to_send)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
sock.connect((UDP_IP,UDP_PORT))
array_to_send = array_to_send.encode()
sock.send(array_to_send)
sock.close()