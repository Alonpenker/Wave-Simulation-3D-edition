#---define the modules for the project---#
import pygame
import pygame.freetype
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import math
from random import randint
#---define variables---#
pygame.init()
pygame.font.init()
screenWidth = 1000
screenHeight = 800
display = (1000,800)
win = pygame.display.set_mode(display,DOUBLEBUF|OPENGL)
pygame.display.set_caption("Wave Simulation in 3D")
glOrtho(0,100,-10,10,-10,10)
#gluPerspective(45, display[0]/display[1], 1, 500.0)
glTranslatef(0.0,0.0,0.0)
length = 20
amplitude = 3
type = 1
running = True
mode = "opening screen" #opening screen, explanation screen, simulation, wave game?
pygame.font.init()
font1 = pygame.font.SysFont ('calibri', 20)
font2 = pygame.font.SysFont ('calibri', 30)
font3 = pygame.font.SysFont('calibri', 70)
infoText = ""
infoTime = 1
status: str = "GO"
autoPilot: str = "OFF"
typeText = "Square Wave"
#---define class for the wave---#
class Point():
    def __init__(self, placement, value):
        self.placement = placement #מיקום
        self.value = value  #ערך
    def getPx(self):
        return self.placement
    def getPy(self):
        return int(300-self.value*10)
    def getRGBColor(self):
        if abs(self.value)*20<255:
           return (0,abs(self.value)*20,255)
        else:
            return (0, 255, 255)
    def getGreenColor(self):
        if abs(self.value) * 40 < 255:
            return (abs(self.value) * 40)/255
        else:
            return 1
#---define wave values---#
rightValues = [] #values that goes right
leftValues = [] #values that goes left
wave = [] #crossing of the two lists
for i in range(0, 100+50+50+1, 1):
    rightValues.append(0)
    leftValues.append(0)
for i in range(0, 101, 1):
    wave.append(Point(i,rightValues[i+50]+leftValues[i+50]))
#---defining auxiliary operations---#
def Pulse(length, amplitude, type, direction):
    if type==1: #פולס מרובע
        if direction == 'right' and length!=0:
          for f in range(50,49-length,-1):
            rightValues[f] = amplitude
        if direction == 'left' and length!=0:
          for z in range(100+50,100+51+length,1):
            leftValues[z] = amplitude
    if type==2: #פולס משולש
        num = amplitude
        lol = 0
        if length%2==0:
          if direction == 'right':
            for f in range(50-int(length/2),50,1):
              rightValues[f] = num - lol
              lol+=amplitude/(length*0.5)
            lol = 0
            for f in range(49-int(length/2), 49 - length, -1):
                rightValues[f] = num - lol
                lol += amplitude / (length * 0.5)
          if direction == 'left':
              for f in range(100+50+int(length / 2), 100+50, -1):
                  leftValues[f] = num - lol
                  lol += amplitude / (length * 0.5)
              lol = 0
              for f in range(100+51+int(length / 2),100+50+length, 1):
                  leftValues[f] = num - lol
                  lol += amplitude / (length * 0.5)
        else:
            if direction == 'right':
                for f in range(50 - int((length+1)/ 2), 50, 1):
                    rightValues[f] = num - lol
                    lol += amplitude / (length * 0.5)
                lol = 0
                for f in range(50 - int((length+1) / 2), 49 - length, -1):
                    rightValues[f] = num - lol
                    lol += amplitude / (length * 0.5)
            if direction == 'left':
                for f in range(100 + 50 + int((length+1) / 2), 100 + 50, -1):
                    leftValues[f] = num - lol
                    lol += amplitude / (length * 0.5)
                lol = 0
                for f in range(100 + 50 + int((length+1) / 2), 100 + 51 + length, 1):
                    leftValues[f] = num - lol
                    lol += amplitude / (length * 0.5)
    if type==3: #פולס גל
        par = 0
        if direction == 'right':
          for f in range(50,49-length,-1):
            rightValues[f] = amplitude*math.cos(math.pi*0.5+-par*0.5*math.pi)
            par+=4/length
        if direction == 'left':
          for z in range(100+50,100+51+length,1):
            leftValues[z] = -1*amplitude*math.cos(math.pi*0.5+-par*0.5*math.pi)
            par+=4/length
def updateValues(wave):
    for r in range(100+100,0,-1):
        rightValues[r] = rightValues[r - 1]
    for l in range(0,100+100, 1):
        leftValues[l] = leftValues[l + 1]
    for w in range(0,100+1,1):
        wave[w].value = rightValues[w+50]+leftValues[w+50]
def drawText(xpos, ypos, textString, color, font):
    textSurface = font.render(textString, True, color, (0,0,0,1))
    textData = pygame.image.tostring(textSurface, "RGBA", True)
    glRasterPos2d(xpos,ypos)
    glDrawPixels(textSurface.get_width(), textSurface.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, textData)
def checkValues():
    counter = 0
    for i in range (0,101,1):
        if wave[i].value!=0:
            counter=counter+1
    if counter==0:
        return True
    else:
        return False
def checkType(number):
    if number==1:
        return "Square Wave"
    if number==2:
        return "Triangular Wave"
    if number==3:
        return "Sine Wave"
def resetValues():
    rightValues.clear()
    leftValues.clear()
    for i in range(0, 100 + 50 + 50 + 1, 1):
        rightValues.append(0)
        leftValues.append(0)
    for i in range(0, 101, 1):
        wave[i].value == 0
#print(pygame.font.get_fonts())
#---main loop---#
while running:
    if mode=="opening screen":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    mode = "explanation screen"
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        drawText(19, 4, "Wave Simulation in 3D", (255,255,255,1), font3)
        drawText(36, 3, "made by Alon Penker", (255, 255, 255, 1), font2)
        drawText(28, -9, "press SPACE to begin the simulation.", (255, 255, 255, 1), font2)
        pygame.display.flip()
        pygame.time.delay(10)
    if mode=="explanation screen":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    mode = "simulation"
                    glRotatef(20, 1, 0, 0)
                    infoTime = 0
                if event.key == pygame.K_t:
                    if status == 'GO':
                        status = 'STOP'
                        infoText = "Wave simulation stopped"
                        infoTime = 1
                    else:
                        status = 'GO'
                        infoText = "Wave simulation continues"
                        infoTime = 1
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        if checkValues()==True:
          if rightValues[49] == 0:
              l1 = randint(4,49)
              a1 = randint(-5,5)
              while a1==0:
                  a1 = randint(-5, 5)
              t1 = randint(1,3)
              t1Text = checkType(t1)
              Pulse(l1, a1, t1, 'right')
          if leftValues[100 + 49] == 0:
              l2 = randint(4, 49)
              a2 = randint(-5, 5)
              while a2 == 0:
                  a2 = randint(-5, 5)
              t2 = randint(1, 3)
              t2Text = checkType(t2)
              Pulse(l2, a2, t2, 'left')
        if status == "GO":
            updateValues(wave)
        if infoTime>0:
            infoTime=infoTime-0.01
        for m in range(49, 100 + 100 - 1, 1):
                glBegin(GL_LINES)
                glColor3f(1, 0, 0)
                glVertex3fv((m - 50, rightValues[m], 0))
                glVertex3fv((m - 50 + 1, rightValues[m + 1], 0))
                glEnd()
        for n in range(49, 100 + 100 - 1, 1):
                glBegin(GL_LINES)
                glColor3f(0, 0, 1)
                glVertex3fv((n - 50, leftValues[n], 0))
                glVertex3fv((n - 50 + 1, leftValues[n + 1], 0))
                glEnd()
        for i in range(0, len(wave) - 1, 1):
            glBegin(GL_LINES)
            glColor3f(1, 1, 1.0)
            glVertex3fv((i, wave[i].value, 0))
            glVertex3fv((i + 1, wave[i + 1].value, 0))
            glEnd()
        drawText(3, -6, 'Right wave:', (255, 0, 0, 1), font1)
        drawText(3, -7, 'Length: ' + str(l1), (255, 0, 0, 1), font1)
        drawText(3, -8, 'Amplitude: ' + str(a1), (255, 0, 0, 1), font1)
        drawText(3, -9, 'Wave type: ' + t1Text, (255, 0, 0, 1), font1)
        drawText(75, -6, 'Left wave:', (0, 0, 255, 1), font1)
        drawText(75, -7, 'Length: ' + str(l2), (0, 0, 255, 1), font1)
        drawText(75, -8, 'Amplitude: ' + str(a2), (0, 0, 255, 1), font1)
        drawText(75, -9, 'Wave type: ' + t2Text, (0, 0, 255, 1), font1)
        drawText(37, -10, infoText, (255*infoTime, 255*infoTime, 255*infoTime, 1), font1)
        drawText(3, 9, 'This project is based on the principle of super-position: When two or more waves cross at a point, the displacement', (255, 255, 255, 1), font1)
        drawText(3, 8,'at that point is equal to the sum of the displacements of the individual waves. In the following example, the',(255, 255, 255, 1), font1)
        drawText(3, 7,'displacement at each point on the white wave is the sum of the displacements of the red and blue waves at that point.',(255, 255, 255, 1), font1)
        drawText(3,6,"press T to stop and play the example, press SPACE to continue.",(255,255,255,1),font1)
        pygame.display.flip()
        pygame.time.delay(35)
        if mode=="simulation":
            resetValues()
    if mode=="simulation":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    if amplitude < 5:
                        amplitude += 1
                        infoText = "The amplitude increased by 1."
                        infoTime = 1
                    else:
                        infoText = "5 is the maximum amplitude possible"
                        infoTime = 1
                if event.key == pygame.K_s:
                    if amplitude > -5:
                        amplitude -= 1
                        infoText = "The amplitude decreased by 1."
                        infoTime = 1
                    else:
                        infoText = "-5 is the minimum amplitude possible"
                        infoTime = 1
                if event.key == pygame.K_a:
                    if length > 1:
                        length -= 1
                        infoText = "The length decreased by 1."
                        infoTime = 1
                    else:
                        infoText = "The length cannot be equal or less than zero"
                        infoTime = 1
                if event.key == pygame.K_d:
                    if length < 49:
                        length += 1
                        infoText = "The length increased by 1."
                        infoTime = 1
                    else:
                        infoText = "49 is the maximum length possible"
                        infoTime = 1
                if event.key == pygame.K_1:
                    type = 1
                    typeText = "Square Wave"
                    infoText = "The wave type changed to Square Wave"
                    infoTime = 1
                if event.key == pygame.K_2:
                    type = 2
                    typeText = "Triangular Wave"
                    infoText = "The wave type changed to Triangular Wave"
                    infoTime = 1
                if event.key == pygame.K_3:
                    type = 3
                    typeText = "Sine Wave"
                    infoText = "The wave type changed to Sine Wave"
                    infoTime = 1
                if event.key == pygame.K_p and status=="GO":
                    if rightValues[50] == 0:
                        Pulse(length, amplitude, type, 'right')
                    if leftValues[100 + 50] == 0:
                        Pulse(length, -amplitude, type, 'left')
                if event.key == pygame.K_t:
                    if status == 'GO':
                        status = 'STOP'
                        infoText = "Wave simulation stopped"
                        infoTime = 1
                    else:
                        status = 'GO'
                        infoText = "Wave simulation continues"
                        infoTime = 1
                if event.key == pygame.K_e:
                    if autoPilot == 'ON':
                        autoPilot = 'OFF'
                    else:
                        autoPilot = 'ON'
        keys = pygame.key.get_pressed()
        if keys[pygame.K_q]:
            if rightValues[49] == 0:
                Pulse(length, amplitude, type, 'right')
            if leftValues[100 + 51] == 0:
                Pulse(length, -amplitude, type, 'left')
        if keys[pygame.K_r]:
            if rightValues[49] == 0:
                Pulse(randint(1, 49), randint(-5, 5), randint(1, 3), 'right')
            if leftValues[100 + 49] == 0:
                Pulse(randint(1, 49), randint(-5, 5), randint(1, 3), 'left')
        if checkValues()==True and autoPilot=="ON":
          if rightValues[49] == 0:
              l1 = randint(4,49)
              a1 = randint(-5,5)
              while a1==0:
                  a1 = randint(-5, 5)
              t1 = randint(1,3)
              t1Text = checkType(t1)
              Pulse(l1, a1, t1, 'right')
          if leftValues[100 + 49] == 0:
              l2 = randint(4, 49)
              a2 = randint(-5, 5)
              while a2 == 0:
                  a2 = randint(-5, 5)
              t2 = randint(1, 3)
              t2Text = checkType(t2)
              Pulse(l2, a2, t2, 'left')
        if status == "GO":
            updateValues(wave)
        if infoTime>0:
            infoTime=infoTime-0.01
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        drawText(3,10,"To increase the ampiltude, press W.",(255,255,255,1),font1)
        drawText(3, 9, "To decrease the ampiltude, press S.", (255, 255, 255, 1), font1)
        drawText(3, 8, "To increase the length, press D.", (255, 255, 255, 1), font1)
        drawText(3, 7, "To decrease the length, press A.", (255, 255, 255, 1), font1)
        drawText(3, 6, "To create continuous waves, hold Q.", (255, 255, 255, 1), font1)
        drawText(3, 5, "To create continuous random waves, hold R.", (255, 255, 255, 1), font1)
        drawText(50,10, "To change the type to square wave, press 1.", (255, 255, 255, 1), font1)
        drawText(50, 9, "To change the type to triangular wave, press 2.", (255, 255, 255, 1), font1)
        drawText(50,8, "To change the type to sine wave, press 3.", (255, 255, 255, 1), font1)
        drawText(50, 7, "To stop and play the simulation, press T.", (255, 255, 255, 1), font1)
        drawText(50, 6, "To create wave, press P.", (255, 255, 255, 1), font1)
        drawText(50, 5, "To watch and enjoy, press E.", (255, 255, 255, 1), font1)
        drawText(3, -7, 'Length: ' + str(length), (255 , 255 , 255 , 1), font1)
        drawText(3, -8, 'Amplitude: ' + str(amplitude), (255, 255, 255, 1), font1)
        drawText(3, -9, 'Wave type: ' + typeText, (255, 255, 255, 1), font1)
        drawText(3, -10, 'Information: ', (255, 255, 255, 1), font1)
        drawText(13.5, -10, infoText, (255*infoTime, 255*infoTime, 255*infoTime, 1), font1)
        for q in range(-6, 6, 1):
            for i in range(0, len(wave) - 1, 1):
                glBegin(GL_LINE_STRIP)
                glColor3f(0, wave[i].getGreenColor(), 1.0)
                glVertex3fv((i, wave[i].value, q))
                glVertex3fv((i + 1, wave[i + 1].value, q))
                glEnd()
        pygame.display.flip()
        pygame.time.delay(10)
pygame.quit()