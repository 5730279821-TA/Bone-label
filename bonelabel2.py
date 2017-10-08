import win32api
import pygame
import time
import datetime
import numpy
import os,errno
from PIL import ImageGrab
import xlwt
from tkinter import *
from operator import itemgetter
import shutil

class settitlename(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()

def scale():
    root = Tk()
    root.configure(background='#BFAEFF')
    root.resizable(width=False, height=False)
    app = settitlename(master=root)
    app.master.title("Level of cancer")
    v = IntVar()
    v.set(0)
    Label(root,
          text="""Please scale damage level:""",
          bg="#BFAEFF",
          font=("Tahoma", 14),
          justify = LEFT,
          padx = 20).pack()
    Radiobutton(root,
                text="Level 1",
                bg="#BFAEFF",
                padx = 20,
                pady=10,
                variable=v,
                font=("Tahoma", 14),
                value=1).pack()
    Radiobutton(root,
                text="Level 2",
                bg="#BFAEFF",
                padx = 20,
                pady=10,
                variable=v,
                font=("Tahoma", 14),
                value=2).pack()
    Radiobutton(root,
                text="Level 3",
                bg="#BFAEFF",
                padx = 20,
                pady=10,
                variable=v,
                font=("Tahoma", 14),
                value=3).pack()
    Radiobutton(root,
                text="Level 4",
                bg="#BFAEFF",
                padx = 20,
                pady=10,
                variable=v,
                font=("Tahoma", 14),
                value=4).pack()
    Radiobutton(root,
                text="Level 5",
                bg="#BFAEFF",
                padx = 20,
                pady=10,
                variable=v,
                font=("Tahoma", 14),
                value=5).pack()
    Radiobutton(root,
                text="Unknown",
                bg="#BFAEFF",
                padx = 20,
                pady=10,
                variable=v,
                font=("Tahoma", 14),
                value=0).pack()
    root.mainloop()
    return v.get()

screen = pygame.display.set_mode((1,1),pygame.NOFRAME)
print("Bone scintigraphy label Tool")
print("1) Press \"X\" to capture the screen")
print("2) Drag mouse on cancer area for localization")
print("3) Segment the cancer point by click mouse")
print("4) Press \"S\" to save to segmentation point in .csv file")
print("   Press \"E\" to erase draw in the image")
print("   Press \"R\" to resize the image")
print("Log transaction\n")
start =(-1,-1)
end =(-1,-1)
color = (255,0,0)
capture = False

screenres = (win32api.GetSystemMetrics(0),win32api.GetSystemMetrics(1))
dest = (0,0)
filename =""
draw = False
resize = False
topleft =(-1,-1)
topleftget =False
bottomright =(-1,-1)
bottomrightget =False
resizeready =False
ccount=0
data = []
drawpair = set([])
line = set([])
wb = xlwt.Workbook()
ws = wb.add_sheet("Sheet1")


def createbbox(line):
    max_x = max(line, key=itemgetter(0))[0]
    min_x = min(line, key=itemgetter(0))[0]
    max_y = max(line, key=itemgetter(1))[1]
    min_y = min(line, key=itemgetter(1))[1]
    topleftbox = (min_x,min_y)
    bottomrightbox = (max_x,max_y)
    return topleftbox,bottomrightbox

def saveDataToNewFile(st,level,line,tlp,brp):
    r = 4
    c = 0
    wb = xlwt.Workbook()
    ws = wb.add_sheet("Sheet1")
    ws.write(0, c, level)
    ws.write(1, 0, "Bounding Box Position")
    ws.write(2, 0, tlp[0])
    ws.write(2, 1, tlp[1])
    ws.write(2, 2, brp[0])
    ws.write(2, 3, brp[1])
    print("BoundingBox is "+"("+str(tlp[0])+","+str(tlp[1])+")"+"("+str(brp[0])+","+str(brp[1])+")")
    ws.write(3, 0, "X")
    ws.write(3, 1, "Y")
    for p in line:
        ws.write(r, c, p[0])
        ws.write(r, c+1, p[1])
        r += 1
    wb.save("data/"+st+"/image_"+str(ccount)+"/"+"image_"+str(ccount)+".csv")

while True:
    if (capture):
        ccount=0
        st = datetime.datetime.fromtimestamp(time.time()).strftime('%Y%m%d_%H%M%S')
        im=ImageGrab.grab()
        try:
            os.makedirs("data/"+st)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
        filename=st+".jpeg"
        im.save("data/" + st + "/0riginal_"+"image_"+str(ccount)+".jpeg")
        im.save("data/" + st + "/" + filename)
        screen = pygame.display.set_mode(screenres, pygame.FULLSCREEN,32)
        image = pygame.image.load("data/"+st+"/"+"image_"+str(ccount)+".jpeg")
        screen.blit(image,image.get_rect())
        line.clear()
        capture = False
    a = win32api.GetKeyState(0x01)
    if (draw):
        if a < 0:
            end=win32api.GetCursorPos()
            if (drawrect.collidepoint(end)):
                if start == (-1,-1):
                    start = end
                pygame.draw.line(screen,color,start,end,2)
                drawpair.add((start,end))
                start=end
                size = numpy.subtract(bottomright, topleft)
                x = size[0]
                y = size[1]
                inipos = (int((screenres[0] - x) / 2), int((screenres[1] - y) / 2))
                line.add((end[0]-inipos[0],end[1]-inipos[1]))
        else:
            start =(-1,-1)
    elif (topleftget):
        topleft =win32api.GetCursorPos()
        topleftget=False
    elif(bottomrightget):
        bottomright =win32api.GetCursorPos()
        bottomrightget =False
        resizeready =True
    elif (resizeready):
        size =numpy.subtract(bottomright,topleft)
        x = size[0]
        y = size[1]
        if x!=y:
            rect = pygame.Rect(0,0,x, y)
            rect.topleft = topleft
            rect.bottomright =bottomright
            sub = screen.subsurface(rect)
            try:
                os.makedirs("data/"+st+"/image_"+str(ccount))
            except OSError as e:
                if e.errno != errno.EEXIST:
                    raise
            pygame.image.save(sub, "data/"+st+"/image_"+str(ccount)+"/"+"r_"+str(ccount)+".jpeg")
            screen = pygame.display.set_mode(screenres, pygame.FULLSCREEN,32)
            screen.fill((0,0,0))
            image = pygame.image.load("data/"+st+"/image_"+str(ccount)+"/"+"r_"+str(ccount)+".jpeg")
            inipos = (int((screenres[0]-x)/2),int((screenres[1]-y)/2))
            drawrect =screen.blit(image,inipos)
            subscreen = screen.subsurface(drawrect)
            resizeready =False
            resize =False
            draw =True
        else:
            print("Please resize the image again (Drag from top-left to bottom-right)")
            resizeready=False
#x = screen capture -> resize the screen
#r = resizing again
#e = erase all draw point
#s = save without closing the program
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_x:
                if (not draw):
                    capture = True
                    resize =True
            elif event.key == pygame.K_s:
                if len(line)!=0:
                    tlp,brp = createbbox(line)
                    pygame.image.save(subscreen, "data/"+st+"/image_"+str(ccount)+"/"+"s_"+str(ccount)+".jpeg")
                    pygame.draw.rect(subscreen, (0, 0, 255),(tlp[0], tlp[1], (brp[0] - tlp[0]) + 2, (brp[1] - tlp[1]) + 2), 1)
                    pygame.image.save(subscreen, "data/"+st+"/image_"+str(ccount)+"/"+ "b_"+str(ccount)+".jpeg")
                    draw=False
                    screen = pygame.display.set_mode((1,1),pygame.NOFRAME)
                    pygame.display.flip()
                    level = scale()
                    saveDataToNewFile(st, level, line,tlp,brp)
                    ccount = ccount + 1
                    print("Level of image" + filename + " is " + str(level))
                    screen = pygame.display.set_mode(screenres, pygame.FULLSCREEN, 32)
                    image = pygame.image.load("data/" + st + "/" + filename)
                    screen.blit(image, image.get_rect())
                    line.clear()
                    for point in drawpair:
                        pygame.draw.line(screen, color, (point[0][0]-(inipos[0]-topleft[0]),point[0][1]-(inipos[1]-topleft[1])),(point[1][0]-(inipos[0]-topleft[0]),point[1][1]-(inipos[1]-topleft[1])), 2)
                    pygame.image.save(screen, "data/" + st + "/" + filename)
                    drawpair.clear()
                    resize = True
                else:
                    print("Please draw in the image")
            elif event.key == pygame.K_r:
                line.clear()
                os.remove("data/"+st+"/image_"+str(ccount)+"/"+"r_"+str(ccount)+".jpeg")
                shutil.rmtree("data/"+st+"/image_"+str(ccount))
                resize =True
                draw =False
                capture = True
                screen = pygame.display.set_mode((1,1),pygame.NOFRAME)
            elif event.key == pygame.K_e:
                line.clear()
                screen = pygame.display.set_mode(screenres, pygame.FULLSCREEN, 32)
                screen.fill((0, 0, 0))
                image = pygame.image.load("data/"+st+"/image_"+str(ccount)+"/"+"r_"+str(ccount))
                inipos = (int((screenres[0] - x) / 2), int((screenres[1] - y) / 2))
                drawrect = screen.blit(image, inipos)
                subscreen = screen.subsurface(drawrect)
                resizeready = False
                resize = False
                draw = True
            elif event.key == pygame.K_KP_ENTER:
                if(draw==False and resize==True):
                    screen = pygame.display.set_mode((1, 1), pygame.NOFRAME)
        elif event.type == pygame.MOUSEBUTTONUP:
            if (resize and not bottomrightget):
                bottomrightget =True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if (resize and not topleftget):
                topleftget =True
    pygame.display.update()

