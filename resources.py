from __future__ import division
import pygame, sys, os

from pathlib import Path

#load resources for the tracker
class resources:

    bigHeaderFont = None
    headerFont = None
    subHeaderFont = None
    menuItemFont = None

    borderOffset = None
    lineWidth = None
    thinLineWidth = None

    def resource_path(self, relative_path):
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        path = str(base_path) + str(relative_path)
        print(path)
        #path = os.path.join(base_path, relative_path)
        return path

    def __init__(self):

        #define project wide constant values
        # define the ui colour
        self.ui_colour = ('#A79916')
        self.background_colour = (0,0,0)

        #Load the audio files
        self.warning=pygame.mixer.Sound(self.resource_path("\\resources\warning.ogg"))
        self.end=pygame.mixer.Sound(self.resource_path("\\resources\end.ogg"))

        #load the icon
        self.icon=pygame.image.load(self.resource_path('\\resources\\USCM.ico'))

    def initFonts(self,scope):

        scale_Height = scope.scale_Height
        scale_Width = scope.scale_Width

        #default sizes for 3840x2160
        args = [42, 23, 14, 12, 0, 4, 1.5]

        if scope.width<=800 and scope.height<=600:
            args = [38, 17, 14, 12, 0, 4, 3]
        if scope.width<=1024 and scope.height<=768:
            args = [38, 17, 14, 12, 0, 4, 1.5]
        if scope.width<=1152 and scope.height<=864:
            args = [38, 17, 14, 12, 0, 4, 1.5]
        if scope.width<=1176 and scope.height<=664:
            args = [42, 22, 14, 12, 0, 4, 1.5]
        if scope.width<=1280 and scope.height<=720:
            args = [42, 22, 14, 12, 0, 4, 1.5]
        if scope.width<=1280 and scope.height<=768:
            args = [36, 20, 14, 12, 0, 4, 1.5]
        if scope.width<=1280 and scope.height<=800:
            args = [36, 20, 14, 12, 0, 4, 1.5]
        if scope.width<=1280 and scope.height<=960:
            args = [32, 16, 14, 12, 0, 4, 1.5]
        if scope.width<=1280 and scope.height<=1024:
            args = [32, 16, 14, 12, 0, 4, 1.5]
        if scope.width<=1360 and scope.height<=768:
            args = [38, 23, 14, 12, 0, 4, 1.5]
        if scope.width<=1366 and scope.height<=768:
            args = [38, 23, 14, 12, 0, 4, 1.5]
        if scope.width<=1440 and scope.height<=900:
            args = [38, 20, 14, 12, 0, 4, 1.5]
        if scope.width<=1600 and scope.height<=900:
            args = [38, 22, 14, 12, 0, 4, 1.5]
        if scope.width<=1600 and scope.height<=1024:
            args = [38, 20, 14, 12, 0, 4, 1.5]
        if scope.width<=1600 and scope.height<=1200:
            args = [38, 17, 14, 12, 0, 4, 1.5]
        if scope.width<=1680 and scope.height<=1050:
            args = [38, 20, 14, 12, 0, 4, 1.5]
        if scope.width<=1920 and scope.height<=1080:
            args = [38, 22, 14, 12, 0, 4, 1.5]
        if scope.width<=1920 and scope.height<=1200:
            args = [38, 20, 14, 12, 0, 4, 1.5]
        if scope.width<=1920 and scope.height<=1440:
            args = [38, 17, 14, 12, 0, 4, 1.5]
        if scope.width<=2048 and scope.height<=1536:
            args = [38, 17, 14, 12, 0, 4, 1.5]
        if scope.width<=2560 and scope.height<=1440:
            args = [42, 23, 14, 12, 0, 4, 1.5]
        if scope.width<=2560 and scope.height<=1600:
            args = [42, 20, 14, 12, 0, 4, 1.5]
        
            
        #load the fonts
        fontPath = self.resource_path("\\resources\sentryTerminal.ttf")
        self.bigHeaderFont = pygame.font.Font(fontPath,int(args[0]*scale_Height))
        self.headerFont = pygame.font.Font(fontPath,int(args[1]*scale_Height))
        self.subHeaderFont = pygame.font.Font(fontPath,int(args[2]*scale_Height))
        self.menuItemFont = pygame.font.Font(fontPath,int(args[3]*scale_Height))

        #define default line widths
        self.borderOffset = int(args[4]*scale_Width)
        self.lineWidth = int(args[5]*scale_Width)
        self.thinLineWidth = int(args[6]*scale_Width)
