import serial
import string
import math

WIDTH = 1120
HEIGHT = 720
TITLE = "MODRON-VISION"
x = [0]*100 # list of size 100 initialized to 0
analog = [0, 0, 0, 0, 0]
FIELDS = [Rect(118,118,183,183),Rect(118,419,183,183),Rect(419,118,183,183),Rect(419,419,183,183)]

currentlyTurning = False
masterAngle = 0
turnAngle = 0

sensorValues = []
BLOCK_THRESHOLD = 400

def draw():
    screen.fill((255, 255, 255))

    for field in FIELDS:
        screen.draw.filled_rect(field, (102, 48, 205))
    screen.draw.filled_circle([BOT_X,BOT_Y],50,(200,0,0))
    #screen.draw.line([BOT_X,BOT_Y],[BOT_X + HEAD_X, BOT_Y + HEAD_Y],(0,0,0))

    screen.draw.filled_rect(Rect(720,0,400,720),(0,0,0))
    screen.draw.text(("LIDAR (mm): " + str(analog[0])), (740,10), color = "green", fontsize=20)
    screen.draw.text(("RIGHT PHOTOTRANSISTOR: " + str(analog[1])), (740, 25), color = "green", fontsize=20)
    screen.draw.text(("LEFT PHOTOTRANSISTOR: " + str(analog[2])), (740, 40), color = "green", fontsize=20)
    screen.draw.text(("X: " + str(analog[3])), (740, 55), color = "green", fontsize=20)
    screen.draw.text(("Y: " + str(analog[4])), (740, 70), color = "green", fontsize=20)
    #screen.draw.text(("CURRENT ORIENTATION: " + str(analog[5])), (740, 85), color = "green", fontsize=20)

    if ((analog[1] > BLOCK_THRESHOLD) and (analog[2] < BLOCK_THRESHOLD)):
        screen.draw.text(("RIGHT"), (740, 200), color = "red", fontsize=30)
    elif ((analog[2] > BLOCK_THRESHOLD) and (analog[1] < BLOCK_THRESHOLD)):
        screen.draw.text(("LEFT"), (740, 200), color = "red", fontsize=30)
    elif ((analog[1] > BLOCK_THRESHOLD) and (analog[2] > BLOCK_THRESHOLD)):
        screen.draw.text(("BOTH"), (740, 200), color = "red", fontsize=30)

def update(dt):
    global HEIGHT
    global x, analog
    global masterAngle, turnAngle, currentlyTurning
    global BOT_X,BOT_Y#,HEAD_X,HEAD_Y,BOT_THETA

    while ser.in_waiting:
        line = ser.read_until().strip() #strip() removes the \r\n
        values = line.decode('ascii').split(' ')
        if(values[0] == 'x'):
            x[int(values[1])] = int(values[2])
        if(values[0] == 'a'):
            for idx in range(0,len(analog)):
                #print(idx)
                #print(values[idx+1])
                analog[idx] = float(values[idx+1])

    #BOT_THETA = analog[3]
    BOT_X = 100*analog[3]
    BOT_Y = 100*analog[4]

    #HEAD_X = 50*math.cos(BOT_THETA)
    #HEAD_Y = 50*math.sin(BOT_THETA)


def on_mouse_down(button, pos):
    #print("Mouse button", button, "down at", pos)
    ser.write(b'o')

def on_mouse_up(button, pos):
    #print("Mouse button", button, "up at", pos)
    ser.write(b'p')
    ser.write(b'a')

def on_key_down(key): #key names are saved in CAPS
    if key.name == 'X':
        ser.write(b'x')
        #print("Sent x")
    if key.name == 'C':
        ser.write(b'c')
        #print("Sent c")
    if key.name == 'W':
        ser.write(b'w')
    if key.name == 'S':
        ser.write(b's')
    if key.name == 'A':
        ser.write(b'l')
    if key.name == 'D':
        ser.write(b'r')
    if key.name == 'SPACE':
        ser.write(b'b')
    if key.name == 'O':
        ser.write(b'o')
    if key.name == 'P':
        ser.write(b'p')




ser = serial.Serial('COM10',9600)