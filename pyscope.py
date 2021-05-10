from __future__ import division
import os, pygame
import ctypes
from PIL import Image, ImageFilter
ctypes.windll.user32.SetProcessDPIAware()

#Define display class
class pyscope :
    
    screen = None
    #pySurface = None
    
    def __init__(self):

        os.environ['SDL_VIDEO_CENTERED'] = '1' # You have to call this before pygame.init()

        pygame.init()
        pygame.font.init()

        info = pygame.display.Info() # You have to call this before pygame.display.set_mode()
        self.max_screen_width = info.current_w
        self.max_screen_height = info.current_h

        self.resized_screen_width = int(self.max_screen_width-(self.max_screen_width/2))
        self.resized_screen_height = int(self.max_screen_height-(self.max_screen_height/2))

        self.screen_width = self.max_screen_width
        self.screen_height = self.max_screen_height

        self.originalWidth = 640
        self.originalHeight = 400

        #setup the display and initialise fonts
        flags = (pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.HWACCEL)

        #initialise the screen variables
        self.initVars()
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height), flags)

        #how many blur loops do we need? more == more blur but higher degredation of performance
        self.numberOfBlurLoops=1

    #window has been resized. Re-initialise variables to new size
    def resize(self, ev):
        self.screen_width = ev.w
        self.screen_height = ev.h
        self.resized_screen_width = self.screen_width
        self.resized_screen_height = self.screen_height      
        self.initVars()

    #initialise the variables for the window
    def initVars(self):
        self.scale_Width = float(self.screen_width / self.originalWidth)
        self.scale_Height = float(self.screen_height / self.originalHeight)
        self.width = int(self.scale_Width * self.originalWidth)
        self.height = int(self.scale_Height * self.originalHeight)       

        #get the blur radius
        self.blurRadius = self.width / 300
        

    #define method to get image befor blurring
    def getBlurredImage(self, imageToBlur):

        width = self.width
        height = self.height

        if self.numberOfBlurLoops==0:
            pil_blurred = Image.frombytes("RGBA", (width, height), imageToBlur).filter(ImageFilter.GaussianBlur(radius=0))
            blurredSurface = pygame.image.fromstring(pil_blurred.tobytes('raw', 'RGBA'), (width, height), 'RGBA')
            return blurredSurface

        tempImageToBlur = imageToBlur
    
        #apply blur to the original image. The original image will be overlaid on top of the blurred image
        for x in range(self.numberOfBlurLoops):
            #get the current surface so we can apply blur to it. Subsequent iterations will increase the blur effect
            pil_blurred = Image.frombytes("RGBA", (width, height), tempImageToBlur).filter(ImageFilter.GaussianBlur(radius=self.blurRadius))
            blurredSurface = pygame.image.fromstring(pil_blurred.tobytes('raw', 'RGBA'), (width, height), 'RGBA')
            #first blit the blurred surface
            self.screen.blit(blurredSurface, (0, 0))
            tempImageToBlur = pygame.image.tostring(self.screen, 'RGBA')

        return blurredSurface

    #define method to blur the contents of a surface image
    def addBlur(self, x, y, xWid, yWid):

        #create a small blurred sub-panel and blur it
        rect = pygame.Rect(x, y, xWid, yWid)
        sub = self.screen.subsurface(rect)
        data = pygame.image.tostring(sub, 'RGBA')
        image = Image.frombytes('RGBA', (xWid,yWid), data)

        #return a non blurred image
        if self.numberOfBlurLoops==0:
            pil_blurred = image.filter(ImageFilter.GaussianBlur(radius=0))
            blurredSurface = pygame.image.fromstring(pil_blurred.tobytes('raw', 'RGBA'), (xWid, yWid), 'RGBA')
            return blurredSurface
    
        #apply blur to the original image. The original image will be overlaid on top of the blurred image
        for x in range(self.numberOfBlurLoops):
            #get the current surface so we can apply blur to it. Subsequent iterations will increase the blur effect
            pil_blurred = image.filter(ImageFilter.GaussianBlur(radius=self.blurRadius))
            blurredSurface = pygame.image.fromstring(pil_blurred.tobytes('raw', 'RGBA'), (xWid, yWid), 'RGBA')
            #first blit the blurred surface
            sub.blit(blurredSurface, (x, y))
            data = pygame.image.tostring(sub, 'RGBA')
            image = Image.frombytes('RGBA', (xWid,yWid), data)

        return blurredSurface

    #toggle fullscreen mode
    def toggle_fullscreen(self, option):
        pygame.display.quit()
        pygame.display.init()
        pygame.font.init()
        if (option=="FULLSCREEN"):
            self.screen_width = self.max_screen_width
            self.screen_height = self.max_screen_height
            self.initVars()
            flags = (pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.HWACCEL | pygame.FULLSCREEN)
        else:
            self.screen_width = self.resized_screen_width
            self.screen_height = self.resized_screen_height
            self.initVars()
            flags = (pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.HWACCEL | pygame.RESIZABLE)

        pygame.display.set_caption('Sentry Terminal')
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height), flags)
 

 
    def __del__(self):
        "Destructor to make sure pygame shuts down, etc."
