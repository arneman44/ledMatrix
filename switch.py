def switchmessage(message,topic):
    if 'LEDMATRIX/RGB' in topic:
        change(message)
    if 'LEDMATRIX/ONOFF' in topic:
        state(message)

R = 255
G = 255
B = 255
STATE = 1

def change(value):
    global R,G,B
    value = value.split(',')
    R = int(value[0])
    G = int(value[1])
    B = int(value[2])


    print(str(R) + str(G) + str(B) + 'color' )

def state(value):
    global STATE
    if value == 'ON':
        STATE = 1
    else:
        STATE = 0

def getRGB():
    return R,G,B,STATE