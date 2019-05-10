import serial
import string

WIDTH = 500
HEIGHT = 250
TITLE = "Fading Green!"
c = 0
x = [0]*100 # list of size 100 initialized to 0
analog = [0, 0, 0]

sensorValues = []


def draw():
    screen.fill((0, c, 0))
    plot(x,10,HEIGHT/2,0,0,255) # data, xpos, ypos, red, green, blue
    # top left to bottom right, ypos is inverted
    screen.draw.text(("LIDAR (mm): " + str(analog[0])), (20,10), color = "black", fontsize=15)
    screen.draw.text(("RIGHT PHOTOTRANSISTOR: " + str(analog[1])), (20, 20), color = "black", fontsize=15)
    screen.draw.text(("LEFT PHOTOTRANSISTOR: " + str(analog[2])), (20, 30), color = "black", fontsize=15)


def plot(data,xpos,ypos,r,g,b):
    ypos = HEIGHT - ypos # flip the y axis
    for i in range(1, len(data)):
        screen.draw.line((xpos+i,ypos),(xpos+i,ypos-x[i]),(r,g,b))

def update(dt):
    global c, HEIGHT
    global x, analog


    c = (c + 1) % 256
    while ser.in_waiting:
        line = ser.read_until().strip() #strip() removes the \r\n
        values = line.decode('ascii').split(' ')
        if(values[0] == 'x'):
            x[int(values[1])] = int(values[2])
            #print(x)
        if(values[0] == 'a'):
            for idx in range(0,len(analog)):
                analog[idx] = int(values[idx+1])
        print(analog)
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
    if key.name == 'SPACE':
        ser.write(b'b')
    if key.name == 'O':
        ser.write(b'o')
    if key.name == 'P':
        ser.write(b'p')
    if key.name == 'R':
        ser.write(b'r')

ser = serial.Serial('/dev/cu.ARNIE-ESP32SPP',9600)
