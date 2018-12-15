import socket
from lib.StupidArtnet import StupidArtnet

UDP_IP = "192.168.1.230"  #ip for the dmx/ethernet bridge
UDP_PORT = 6454

w, h = 21, 8;
Matrix = [[0 for x in range(w)] for y in range(h)]

t1 = [[0,0,0,0],[1,1,1,0],[1,1,1,0],[0,1,1,0],[0,1,1,0],[0,1,1,0],[1,1,1,1],[0,0,0,0]]
t2 = [[0,0,0,0],[0,1,1,0],[1,0,0,1],[0,0,1,0],[0,1,0,0],[1,0,0,0],[1,1,1,1],[0,0,0,0]]
t3 = [[0,0,0,0],[1,1,1,0],[0,0,0,1],[0,1,1,1],[0,1,1,1],[0,0,0,1],[1,1,1,0],[0,0,0,0]]
t4 = [[0,0,0,0],[1,0,0,0],[1,0,1,0],[1,0,1,0],[1,1,1,1],[0,0,1,0],[0,0,1,0],[0,0,0,0]]
t5 = [[0,0,0,0],[1,1,1,1],[1,0,0,0],[1,1,1,0],[0,0,0,1],[0,0,0,1],[1,1,1,0],[0,0,0,0]]
t6 = [[0,0,0,0],[0,1,1,0],[1,0,0,0],[1,1,1,0],[1,0,0,1],[1,0,0,1],[0,1,1,0],[0,0,0,0]]
t7 = [[0,0,0,0],[1,1,1,1],[0,0,0,1],[0,0,1,0],[0,0,1,0],[0,1,0,0],[0,1,0,0],[0,0,0,0]]
t8 = [[0,0,0,0],[0,1,1,0],[1,0,0,1],[1,0,0,1],[0,1,1,0],[1,0,0,1],[0,1,1,0],[0,0,0,0]]
t9 = [[0,0,0,0],[0,1,1,0],[1,0,0,1],[1,0,0,1],[0,1,1,1],[0,0,0,1],[0,1,1,1],[0,0,0,0]]
t0 = [[0,0,0,0],[0,1,1,0],[1,0,0,1],[1,0,0,1],[1,0,0,1],[1,0,0,1],[0,1,1,0],[0,0,0,0]]

w,h = 8,4;
t = [[0 for x in range(w)] for y in range(h)]
print(Matrix)

Matrix[2][10] = 1
Matrix[5][10] = 1

R = "\xff"
G = "\xff"
B = "\xff"

def numbertomatrix(T):
    global t
    print(T)
    if T == "1":
        t = t1
    if T == "2":
        t = t2
    if T == "3":
        t = t3
    if T == "4":
        t = t4
    if T == "5":
        t = t5
    if T == "6":
        t = t6
    if T == "7":
        t = t7
    if T == "8":
        t = t8
    if T == "9":
        t = t9
    if T == "0":
        t = t0

def main(uur,min):
    global Matrix,t
    tijd = [0 for x in range(4)]
    if uur < 10:
        tijd[0] = 0
        tijd[1] = uur
    else:
        uurarray = list(str(uur))
        tijd[0] = uurarray[0]
        tijd[1] = uurarray[1]
    if min < 10:
        tijd[2] = 0
        tijd[3] = min
    else:
        minarray = list(str(min))
        tijd[2] = minarray[0]
        tijd[3] = minarray[1]

    for K in range(4):
        numbertomatrix(tijd[K])
        print(t)
        for I in range(8):
            if K is 0:
                standoff = 0
            if K is 1:
                standoff = 5
            if K is 2:
                standoff = 12
            if K is 3:
                standoff = 17
            print(I)
            Matrix[I][standoff] = t[I][0]
            Matrix[I][standoff + 1] = t[I][1]
            Matrix[I][standoff + 2] = t[I][2]
            Matrix[I][standoff + 3] = t[I][3]
    print(Matrix)
    MATRIX_STRING = [0 for x in range(168)]

    for I in range(21):
         MATRIX_STRING[I] = Matrix[7][20-I]

    for I in range(21):
        MATRIX_STRING[I + 21] =Matrix[6][I]

    for I in range(21):
        MATRIX_STRING[I + 21 + 21] = Matrix[5][20-I]

    for I in range(21):
        MATRIX_STRING[I + 21 + 21 + 21] = Matrix[4][I]

    for I in range(21):
        MATRIX_STRING[I + 21 + 21 + 21 + 21] = Matrix[3][20-I]

    for I in range(21):
        MATRIX_STRING[I + 21 + 21 + 21 + 21 + 21] = Matrix[2][I]

    for I in range(21):
        MATRIX_STRING[I + 21 + 21 + 21 + 21 + 21 + 21] = Matrix[1][20-I]

    for I in range(21):
        MATRIX_STRING[I + 21 + 21 + 21 + 21 + 21 + 21 + 21] = Matrix[0][I]
    print(Matrix)
    print(MATRIX_STRING)
    MATRIX_out = [["\x09" for x in range(3)]for x in range(168)]
    for I in range(168):
        if MATRIX_STRING[I] == 1:
            MATRIX_out[I][0] = R
            MATRIX_out[I][1] = G
            MATRIX_out[I][2] = B
        else:
            MATRIX_out[I][0] = "\x01"
            MATRIX_out[I][1] = "\x01"
            MATRIX_out[I][2] = "\x01"
    array = ['\x01' for x in range(512)]
    for I in range(168):
        for J in range(3):
            array[I + J] = MATRIX_out[I][J]

    array = ["Art-Net\x00",
	"\x00P",
	"\x00", "\x0e",
	"\x00",
	"\x00",
	"\x00", "\x00",
	"\x02", "\x00"] + array

    print(array)
    boi = "".join(array)
    data = boi.encode()
    print(boi)
    print("UDP target IP:", UDP_IP)
    print("UDP target port:", UDP_PORT)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
    sock.connect((UDP_IP, UDP_PORT))
    sock.send(data)
    sock.close()




main(12,45)