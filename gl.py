
#Andy Castillo 18040
#SR3: Models
from obj import Obj
import struct

def char(c):
  return struct.pack('=c', c.encode('ascii'))

def word(c):
  return struct.pack('=h', c)

def dword(c):
  return struct.pack('=l', c)

class Render(object):
  def __init__(self):
    self.framebuffer = []

  def glInit(self):
    self.width = 400
    self.height = 400

  def glCreateWindow(self, width, height):
    self.width = width
    self.height= height

  def glViewPort(self, x ,y , width, height):
    self.xVP = x
    self.yVP = y
    self.widthVP = width
    self.heightVP = height

  def glClear(self):
    self.framebuffer = [
      [self.backgroundColor for x in range(self.width+1)]
      for y in range(self.height+1)
    ]
    
  def glClearColor(self, r, g , b):
    self.backgroundColor = bytes([b*255, g*255, r*255])

  def glVertex(self, x , y):
    if x>1:
      x=1
    if y>1:
      y=1
    coordX = round(self.xVP + (self.widthVP/2 * (1+x)))
    coordY = round(self.yVP + (self.heightVP/2 * (1+y)))
    print(coordX, coordY)
    self.framebuffer[coordX][coordY] = self.color

  def point(self, x, y):
     self.framebuffer[x][y] = self.color

  def glColor(self, r, g , b):
    self.color = bytes([int(b*255), int(g*255), int(r*255)])

  def glFinish(self, filename):
    f = open(filename, 'bw')


    #file header
    f.write(char('B'))
    f.write(char('M'))
    f.write(dword(14 + 40 + self.width * self.height * 3))
    f.write(dword(0))
    f.write(dword(14 + 40))

    #image header
    f.write(dword(40))
    f.write(dword(self.width))
    f.write(dword(self.height))
    f.write(word(1))
    f.write(word(24))
    f.write(dword(0))
    f.write(dword(self.width * self.height * 3))
    f.write(dword(0))
    f.write(dword(0))
    f.write(dword(0))
    f.write(dword(0))

    #pixel data

    for x in range(self.width):
      for y in range(self.height):
        f.write(self.framebuffer[y][x])

    f.close()

  def glLoad(self, filename,translate, scale):
    model = Obj(filename)
	  
    c=0
    for face in model.faces:
      if c >8939:
        self.glColor(1,1,1)
      elif c < 8939 and c>6060:
        self.glColor(0,0,1)
      else:
        self.glColor(1,0,0)
      c+=1
      vcount = len(face)
      for j in range(vcount):
        f1 = face[j][0]
        f2 = face[(j + 1) % vcount][0]

        v1 = model.vertices[f1 - 1]
        v2 = model.vertices[f2 - 1]
        
        x1 = round((v1[0] + translate[0]) * scale[0])
        y1 = round((v1[1] + translate[1]) * scale[1])
        x2 = round((v2[0] + translate[0]) * scale[0])
        y2 = round((v2[1] + translate[1]) * scale[1])
        self.glLine(x1, y1, x2, y2)

  def glLine(self, x0, y0, x1, y1):

    dy = abs(y1-y0)
    dx = abs(x1-x0)

    steep = dy > dx
    if steep:
      x0, y0 = y0, x0
      x1, y1 = y1, x1

    if x0 > x1:
      x0, x1 = x1, x0
      y0, y1 = y1, y0

    dy = abs(y1-y0)
    dx = abs(x1-x0)

    offset = 0
    threshold = dx

    y = y0
    x0 = int(x0)
    x1 = int(x1)

    inc = 1 if y1 > y0 else -1
    for x in range(x0, x1 + 1,):
      x = x
      # print(x, y)
      if steep:
        self.point(y, x)
      else:
        self.point(x, y)

      offset += dy * 2
      if offset >= threshold:
        y += inc
        threshold += 2*dx


bitmap = Render()

bitmap.glCreateWindow(1100, 1100)
bitmap.glClearColor(0,0,0)
bitmap.glClear()
bitmap.glViewPort(0,0,1000,1000)
bitmap.glColor(1,0,0)


bitmap.glLoad('./spiderman-scene.obj', (1, 0.25), (500,500))

bitmap.glFinish('out.bmp')