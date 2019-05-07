import serial
import string

WIDTH = 500
HEIGHT = 250
TITLE = "Fading Green!"
c = 0
x = [0]*100 # list of size 100 initialized to 0
analog = 0

def draw():
    screen.fill((0, c, 0))
    plot(x,10,HEIGHT/2,0,0,255) # data, xpos, ypos, red, green, blue
    screen.draw.text(str(analog), (250, 20), color="orange", fontsize=80) # top left to bottom right, ypos is inverted

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
        #print(values)
        if(values[0] == 'x'):
            x[int(values[1])] = int(values[2])
            #print(x)
        if(values[0] == 'a'):
            analog = int(values[1])

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
    if key.name == 'B':
        ser.write(b'b')
    if key.name == 'O':
        ser.write(b'o')
    if key.name == 'P':
        ser.write(b'p')


ser = serial.Serial('COM5',9600)