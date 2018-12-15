from lib.StupidArtnet import StupidArtnet
import datetime
import time
from MQTT import MQTT_start
from switch import  getRGB
MQTT_start()
target_ip = '192.168.1.230'		# typically in 2.x or 10.x range
packet_size = 512
a = StupidArtnet(target_ip,0,512)
print(a)

# YOU CAN CREATE YOUR OWN BYTE ARRAY OF PACKET_SIZE
packet = bytearray(packet_size)		# create packet for Artnet
for i in range(packet_size):		# fill packet with sequential values
	packet[i] = (i % 256)

# ... AND SET IT TO STUPID ARTNET
a.set(packet)						# only on changes
w, h = 21, 8;

Matrix = [[0 for x in range(w)] for y in range(h)]

t1 = [[0,0,0,0],[0,0,1,0],[0,1,1,0],[1,0,1,0],[0,0,1,0],[0,0,1,0],[0,0,1,0],[0,1,1,1]]
t2 = [[0,0,0,0],[0,1,1,0],[1,0,0,1],[0,0,0,1],[0,0,1,0],[0,1,0,0],[1,0,0,0],[1,1,1,1]]
t3 = [[0,0,0,0],[0,1,1,0],[1,0,0,1],[0,0,0,1],[0,1,1,0],[0,0,0,1],[1,0,0,1],[0,1,1,0]]
t4 = [[0,0,0,0],[1,0,0,1],[1,0,0,1],[1,0,0,1],[1,1,1,1],[0,0,0,1],[0,0,0,1],[0,0,0,1]]
t5 = [[0,0,0,0],[1,1,1,1],[1,0,0,0],[1,1,1,0],[0,0,0,1],[0,0,0,1],[1,0,0,1],[0,1,1,0]]
t6 = [[0,0,0,0],[0,1,1,0],[1,0,0,1],[1,0,0,0],[1,1,1,0],[1,0,0,1],[1,0,0,1],[0,1,1,0]]
t7 = [[0,0,0,0],[1,1,1,1],[0,0,0,1],[0,0,0,1],[0,0,1,0],[0,0,1,0],[0,1,0,0],[0,1,0,0]]
t8 = [[0,0,0,0],[0,1,1,0],[1,0,0,1],[1,0,0,1],[0,1,1,0],[1,0,0,1],[1,0,0,1],[0,1,1,0]]
t9 = [[0,0,0,0],[0,1,1,0],[1,0,0,1],[1,0,0,1],[0,1,1,1],[0,0,0,1],[1,0,0,1],[0,1,1,0]]
t0 = [[0,0,0,0],[0,1,1,0],[1,0,0,1],[1,0,0,1],[1,0,0,1],[1,0,0,1],[1,0,0,1],[0,1,1,0]]

w,h = 8,4;
t = [[0 for x in range(w)] for y in range(h)]
print(Matrix)

Matrix[2][10] = 1
Matrix[5][10] = 1


def numbertomatrix(T):
    global t

    print(T)
    T = str(T)
    if T == '1':
        t = t1
    if T == '2':
        t = t2
    if T == '3':
        t = t3
    if T == '4':
        t = t4
    if T == '5':
        t = t5
    if T == '6':
        t = t6
    if T == '7':
        t = t7
    if T == '8':
        t = t8
    if T == '9':
        t = t9
    if T == '0':
        t = t0
    print(t)

def main(uur,min,R,G,B):
    global Matrix,t,a
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

    print(tijd)
    for K in range(4):
        numbertomatrix(tijd[K])
        print(t)
        for I in range(8):
            if K == 0:
                standoff = 0
            if K == 1:
                standoff = 5
            if K == 2:
                standoff = 12
            if K == 3:
                standoff = 17
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
    MATRIX_out = [[255 for x in range(3)]for x in range(168)]
    for I in range(168):
        if MATRIX_STRING[I] == 1:
            MATRIX_out[I][0] = R
            MATRIX_out[I][1] = G
            MATRIX_out[I][2] = B
        else:
            MATRIX_out[I][0] = 0
            MATRIX_out[I][1] = 0
            MATRIX_out[I][2] = 0
    array = [0 for x in range(512)]
    for I in range(168):
        for J in range(3):
            array[I*3+J] = MATRIX_out[I][J]
    print(array)
    print(MATRIX_out)
    a.set(array)
    a.show()
    time.sleep(1)

minslate = 123
RGBlate = getRGB()
while True:
    now = datetime.datetime.now()
    mins = now.minute
    houre = now.hour
    print(mins)
    print(houre)
    RGB = getRGB()
    STATE = RGB[3]
    if STATE == 1:
        if mins != minslate:
            main(houre,mins,RGB[0],RGB[1],RGB[2])
        if RGB != RGBlate:
            main(houre, mins, RGB[0], RGB[1], RGB[2])
    else:
        a.blackout()

    time.sleep(1)
    minslate = mins
    RGBlate = RGB



