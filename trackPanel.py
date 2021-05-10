from __future__ import division
import pygame, os, math
import random

#define class to describe the gun tracking panel 
class trackPanel():

    scope = None
    resources = None

    def __init__(self, scope, resources):

        #define column and rows
        #column is multi-dimensional. We have column[] == to the justification column and then column[][] representing column
        #width percentages
        self.columns = [0.09,0.24,0.04,0.03,0.19,0.03,0.05,0.12,0.03,0.12,0.07]
        self.rows = [0.16,0.11,0.21,0.04,0.15,0.23,0.07,0.03]
        self.scope = scope
        self.resources = resources
        self.currentRounds=500
        #set value at which the critical warning appears
        self.criticalValue=60
    
        self.countingDown = False
        self.weaponPauseTimer = None
        self.weaponPauseValue = None
        self.weaponPaused = False
        self.weaponTemp = 0
        self.rpm = 0

        #set the critical state
        self.criticalState = 1

        #get a background image that is not blurred
        self.imageToBlur = None
        #get a background image that is blurred
        self.blurredImage = None

    def renderBackground(self, initialiseRowsAndColumns):

        #fill the background
        self.scope.screen.fill(self.resources.background_colour)
        
        #draw everything once and add blur
        self.drawPanel()

        #get a background image that is not blurred
        width = self.scope.width
        height = self.scope.height
        self.imageToBlurBytes = pygame.image.tostring(self.scope.screen, 'RGBA')
        
        #get a background image that is blurred
        self.blurredImage = self.scope.getBlurredImage(self.imageToBlurBytes).convert()
        
    def render(self, event):

        if event==pygame.K_LEFT:
            if self.countingDown:
                self.countingDown=False
            else:
                self.countingDown=True
        if event==pygame.K_RIGHT:
            if not self.countingDown:
                self.currentRounds=500
        if event=="RESIZE":
            self.renderBackground(False)

        #update the counters
        if self.countingDown:
            self.updateCounters()
        
        #draw the blurred background image
        self.scope.screen.blit(self.blurredImage, (0, 0))

        #draw the animated text and graphs
        self.drawAnimated()

        #redraw the graphics to account for blur
        self.drawPanel()

    #update counters
    def updateCounters(self):

        rateOfChange = 0

        ########ROUNDS####################################################
        #if the weapon is paused, check that if the pause time has elapsed 
        if self.weaponPaused:
            if self.weaponPauseValue<0:
                self.weaponPauseTimer=None
                self.weaponPauseValue=None
                self.weaponPaused=False
            else:
                self.weaponPauseValue=self.weaponPauseValue-self.weaponPauseTimer.get_time()
                self.weaponPauseTimer.tick()
            
        if not self.weaponPaused:
            weaponPauseNumber = random.randint(0,9)
            if weaponPauseNumber==7:
                self.weaponPauseTimer=pygame.time.Clock()
                self.weaponPauseValue=random.randint(500, 1000)
                self.weaponPaused=True

        if not self.weaponPaused:        
            if self.currentRounds>0:
                rateOfChange = random.randint(1, 3)
                self.currentRounds=self.currentRounds-rateOfChange
                if self.currentRounds<0:
                    self.currentRounds=0
                    heatRate = -4
                    self.rpm = 0
            else:
                heatRate = -4
                self.rpm = 0

        ##########TEMP and RPM#############################################
        #introduce heating rates based upon fire rate
        if self.weaponPaused:
            heatRate = -2
            self.rpm = 0
        if rateOfChange==1:
            heatRate = 3
            self.rpm = 50
        if rateOfChange==2:
            heatRate = 6
            self.rpm = 75
        if rateOfChange==3:
            heatRate = 9
            self.rpm = 100

        #if the weapon temp gets above 80% then randomise the value between 80 and 100
        self.weaponTemp = self.weaponTemp+heatRate
        if self.weaponTemp>100:
            self.weaponTemp=100-random.randint(0,5)
        if self.weaponTemp<0:
            self.weaponTemp=0

        #stop the countdown when we get to 0
        if self.weaponTemp==0 and self.currentRounds==0:
            self.countingDown=False
            
    #define function to provide y start coordinate of selected row
    def getRowStartHeight(self, rowNum):
        height = 0
        for x in range(rowNum):
            height = height + (self.rows[x]*self.scope.height)

        return height

    #define function to get the the width of a column spanning between column indices
    def getColumnWidth(self, columnStart, columnEnd):

        width = 0
        for x in range(columnStart, columnEnd):
            width = width + (self.columns[x]*self.scope.width)

        return width

    #define function to provide y start coordinate of selected row
    def getColumnStartWidth(self, columnNum):
   
        width = 0
        for x in range(columnNum):
            width = width + (self.columns[x]*self.scope.width)

        return width

    #define function to provide row thickness
    def getRowHeight(self, rowStart, rowEnd):     

        height = 0
        for x in range(rowStart, rowEnd):
            height = height + (self.rows[x]*self.scope.height)

        return height 

    def drawTable(self):

        width = self.scope.width
        height = self.scope.height
        showgrid = False

        #get rows to show grid
        row1StartHeight = self.getRowStartHeight(0)
        row2StartHeight = self.getRowStartHeight(1)
        row3StartHeight = self.getRowStartHeight(2)
        row4StartHeight = self.getRowStartHeight(3)
        row5StartHeight = self.getRowStartHeight(4)
        row6StartHeight = self.getRowStartHeight(5)
        row7StartHeight = self.getRowStartHeight(6)
        row8StartHeight = self.getRowStartHeight(7)

        #get columns to show grid
        column1StartWidth = self.getColumnStartWidth(0)
        column2StartWidth = self.getColumnStartWidth(1)
        column3StartWidth = self.getColumnStartWidth(2)
        column4StartWidth = self.getColumnStartWidth(3)
        column5StartWidth = self.getColumnStartWidth(4)
        column6StartWidth = self.getColumnStartWidth(5)
        column7StartWidth = self.getColumnStartWidth(6)
        column8StartWidth = self.getColumnStartWidth(7)
        column9StartWidth = self.getColumnStartWidth(8)
        column10StartWidth = self.getColumnStartWidth(9)

        #get column widths
        column5width = self.getColumnWidth(4,5)
        column4to7width = self.getColumnWidth(3,6)

        #get row widths
        row3Torow4height = self.getRowHeight(2,4)
        row6height = self.getRowHeight(5,6)

        #draw box around "Rounds Remaining"
        pygame.draw.rect(self.scope.screen, self.resources.ui_colour, (column5StartWidth, row3StartHeight, column5width, self.resources.thinLineWidth), 0)
        pygame.draw.rect(self.scope.screen, self.resources.ui_colour, (column5StartWidth, row5StartHeight, column5width, self.resources.thinLineWidth), 0)
        pygame.draw.rect(self.scope.screen, self.resources.ui_colour, (column5StartWidth, row3StartHeight, self.resources.thinLineWidth, row3Torow4height), 0)
        pygame.draw.rect(self.scope.screen, self.resources.ui_colour, (column6StartWidth, row3StartHeight, self.resources.thinLineWidth, row3Torow4height+self.resources.thinLineWidth), 0)
        #draw the triangle
        pygame.draw.polygon(self.scope.screen, self.resources.ui_colour, [[column5StartWidth, row3StartHeight+(row3Torow4height/2)], [column5StartWidth-row3Torow4height/4, row3StartHeight+(row3Torow4height/2)+row3Torow4height/8], [column5StartWidth-row3Torow4height/4, row3StartHeight+(row3Torow4height/2)-row3Torow4height/8]], 0)


        #draw box around "Time Remaining"
        pygame.draw.rect(self.scope.screen, self.resources.ui_colour, (int(column4StartWidth), int(row6StartHeight), int(column4to7width), self.resources.thinLineWidth), 0)
        pygame.draw.rect(self.scope.screen, self.resources.ui_colour, (int(column4StartWidth), int(row7StartHeight), int(column4to7width), self.resources.thinLineWidth), 0)
        pygame.draw.rect(self.scope.screen, self.resources.ui_colour, (int(column4StartWidth), int(row6StartHeight), self.resources.thinLineWidth, int(row6height)), 0)
        pygame.draw.rect(self.scope.screen, self.resources.ui_colour, (int(column7StartWidth), int(row6StartHeight), self.resources.thinLineWidth, int(row6height)+self.resources.thinLineWidth), 0)

        #draw bottom line
        pygame.draw.rect(self.scope.screen, self.resources.ui_colour, (self.resources.borderOffset, int(row8StartHeight), width-(2*self.resources.borderOffset), self.resources.thinLineWidth), 0)

        #draw rows to show grid
        if showgrid:
            pygame.draw.rect(self.scope.screen, self.resources.ui_colour, (self.resources.borderOffset, int(row1StartHeight), width-(2*self.resources.borderOffset), self.resources.thinLineWidth), 0)
            pygame.draw.rect(self.scope.screen, self.resources.ui_colour, (self.resources.borderOffset, int(row2StartHeight), width-(2*self.resources.borderOffset), self.resources.thinLineWidth), 0)
            pygame.draw.rect(self.scope.screen, self.resources.ui_colour, (self.resources.borderOffset, int(row3StartHeight), width-(2*self.resources.borderOffset), self.resources.thinLineWidth), 0)
            pygame.draw.rect(self.scope.screen, self.resources.ui_colour, (self.resources.borderOffset, int(row4StartHeight), width-(2*self.resources.borderOffset), self.resources.thinLineWidth), 0)
            pygame.draw.rect(self.scope.screen, self.resources.ui_colour, (self.resources.borderOffset, int(row5StartHeight), width-(2*self.resources.borderOffset), self.resources.thinLineWidth), 0)
            pygame.draw.rect(self.scope.screen, self.resources.ui_colour, (self.resources.borderOffset, int(row6StartHeight), width-(2*self.resources.borderOffset), self.resources.thinLineWidth), 0)
            pygame.draw.rect(self.scope.screen, self.resources.ui_colour, (self.resources.borderOffset, int(row7StartHeight), width-(2*self.resources.borderOffset), self.resources.thinLineWidth), 0)

        #draw columns to show grid
        if showgrid:
            pygame.draw.rect(self.scope.screen, self.resources.ui_colour, (int(column1StartWidth), int(row2StartHeight), self.resources.thinLineWidth, int(self.getRowHeight(1, 7))), 0)
            pygame.draw.rect(self.scope.screen, self.resources.ui_colour, (int(column2StartWidth), int(row2StartHeight), self.resources.thinLineWidth, int(self.getRowHeight(1, 7))), 0)
            pygame.draw.rect(self.scope.screen, self.resources.ui_colour, (int(column3StartWidth), int(row2StartHeight), self.resources.thinLineWidth, int(self.getRowHeight(1, 7))), 0)
            pygame.draw.rect(self.scope.screen, self.resources.ui_colour, (int(column4StartWidth), int(row2StartHeight), self.resources.thinLineWidth, int(self.getRowHeight(1, 7))), 0)
            pygame.draw.rect(self.scope.screen, self.resources.ui_colour, (int(column5StartWidth), int(row2StartHeight), self.resources.thinLineWidth, int(self.getRowHeight(1, 7))), 0)
            pygame.draw.rect(self.scope.screen, self.resources.ui_colour, (int(column6StartWidth), int(row2StartHeight), self.resources.thinLineWidth, int(self.getRowHeight(1, 7))), 0)
            pygame.draw.rect(self.scope.screen, self.resources.ui_colour, (int(column7StartWidth), int(row2StartHeight), self.resources.thinLineWidth, int(self.getRowHeight(1, 7))), 0)
            pygame.draw.rect(self.scope.screen, self.resources.ui_colour, (int(column8StartWidth), int(row2StartHeight), self.resources.thinLineWidth, int(self.getRowHeight(1, 7))), 0)
            pygame.draw.rect(self.scope.screen, self.resources.ui_colour, (int(column9StartWidth), int(row2StartHeight), self.resources.thinLineWidth, int(self.getRowHeight(1, 7))), 0)
            pygame.draw.rect(self.scope.screen, self.resources.ui_colour, (int(column10StartWidth), int(row2StartHeight), self.resources.thinLineWidth, int(self.getRowHeight(1, 7))), 0)
        

    def drawBorder(self):

        width = self.scope.width
        height = self.scope.height
        row1Height = self.getRowStartHeight(1)
        
        #draw outline
        pygame.draw.rect(self.scope.screen, self.resources.ui_colour, (self.resources.borderOffset, self.resources.borderOffset, width-(2*self.resources.borderOffset), self.resources.lineWidth), 0)   
        pygame.draw.rect(self.scope.screen, self.resources.ui_colour, (self.resources.borderOffset, height-(self.resources.borderOffset)-self.resources.lineWidth, width-(2*self.resources.borderOffset), self.resources.lineWidth), 0)
        pygame.draw.rect(self.scope.screen, self.resources.ui_colour, (self.resources.borderOffset, self.resources.borderOffset, self.resources.lineWidth, height-(2*self.resources.borderOffset)), 0)
        pygame.draw.rect(self.scope.screen, self.resources.ui_colour, (width-(self.resources.borderOffset+self.resources.lineWidth),self.resources.borderOffset,self.resources.lineWidth, height-(2*self.resources.borderOffset)), 0)
        #draw top line
        pygame.draw.rect(self.scope.screen, self.resources.ui_colour, (self.resources.borderOffset, int(row1Height), width-(2*self.resources.borderOffset), self.resources.lineWidth), 0)
        #draw top circles
        pygame.draw.circle(self.scope.screen, self.resources.ui_colour, (int(width/2+(width/2.5)+22*self.scope.scale_Width), int(row1Height/2+self.resources.lineWidth/2)), int(28*self.scope.scale_Height), self.resources.thinLineWidth)
        pygame.draw.circle(self.scope.screen, self.resources.ui_colour, (int(width/2-(width/2.5)-22*self.scope.scale_Width), int(row1Height/2+self.resources.lineWidth/2)), int(28*self.scope.scale_Height), self.resources.thinLineWidth)
   

    def drawPanel(self):

        self.drawBorder()
        self.drawHeaderText(self.resources.headerFont, self.resources.bigHeaderFont)
        #draw the panel A subheadings
        self.drawPanelSubHeaderText(self.resources.subHeaderFont)
        #draw the left hand column text
        self.drawLeftColumnText(self.resources.headerFont)
        #draw temperature scale
        self.drawScaleLines(7, -1*(self.getColumnWidth(7, 8)/3.5))
        #draw R(M) scale
        self.drawScaleLines(9, -1*(self.getColumnWidth(7, 8)/6))
        #draw the table lines
        self.drawTable()

    def drawAnimated(self):
        
        #draw the current rounds remaining
        self.drawRoundsRemaining(self.resources.bigHeaderFont)
        x = self.getColumnStartWidth(4)
        y = self.getRowStartHeight(2)
        xWid = int(self.getColumnWidth(4, 5))
        yWid = int(self.getRowHeight(2, 4))
        surface = self.scope.addBlur(x, y, xWid, yWid)
        self.scope.screen.blit(surface, (x,y))
        self.drawRoundsRemaining(self.resources.bigHeaderFont)

        #draw.currentTimeRemaining
        self.drawTimeRemaining(self.resources.bigHeaderFont)
        x = self.getColumnStartWidth(4)
        y = self.getRowStartHeight(5)
        xWid = int(self.getColumnWidth(4, 5))
        yWid = int(self.getRowHeight(5, 6))
        surface = self.scope.addBlur(x, y, xWid, yWid)
        self.scope.screen.blit(surface, (x,y))
        self.drawTimeRemaining(self.resources.bigHeaderFont)
        
        #draw temperature scale
        self.drawScale(7, -1*int((self.getColumnWidth(7, 8)/3.5)), self.weaponTemp)
        columnStartWidth = self.getColumnStartWidth(7)
        columnWidth = (self.getColumnWidth(7, 8)) / 2
        offset = -1*int((self.getColumnWidth(7, 8)/3.5))
        x = (columnStartWidth+1.5*columnWidth+offset-(columnWidth/2))-self.resources.lineWidth
        y = self.getRowStartHeight(2)-self.resources.lineWidth
        xWid = int(columnWidth/2)+int((1.5*self.resources.lineWidth))
        yWid = int(self.getRowHeight(2, 6))+(self.resources.lineWidth)
        surface = self.scope.addBlur(x, y, xWid, yWid)
        self.scope.screen.blit(surface, (x,y))
        self.drawScale(7, -1*int((self.getColumnWidth(7, 8)/3.5)), self.weaponTemp)
        #pygame.draw.rect(self.scope.screen, self.resources.ui_colour, (x, y, xWid, yWid), 0)

        #draw R(M) scale
        self.drawScale(9, -1*int((self.getColumnWidth(7, 8)/6)), self.rpm)
        columnStartWidth = self.getColumnStartWidth(9)
        columnWidth = (self.getColumnWidth(9, 10)) / 2
        offset = -1*int((self.getColumnWidth(7, 8)/6))
        x = (columnStartWidth+columnWidth+offset)-self.resources.lineWidth
        y = self.getRowStartHeight(2)-self.resources.lineWidth
        xWid = int(columnWidth/2)+int((1.5*self.resources.lineWidth))
        yWid = int(self.getRowHeight(2, 6))+(self.resources.lineWidth)       
        surface = self.scope.addBlur(x, y, xWid, yWid)
        self.scope.screen.blit(surface, (x,y))
        self.drawScale(9, -1*int((self.getColumnWidth(7, 8)/6)), self.rpm)
        #pygame.draw.rect(self.scope.screen, self.resources.ui_colour, (x, y, xWid, yWid), 0)
        
        #draw critical
        if self.currentRounds<=self.criticalValue:
            self.drawCritical(self.resources.headerFont)
            x = self.getColumnStartWidth(1) - self.resources.lineWidth
            y = self.getRowStartHeight(3) - self.resources.lineWidth
            xWid = int(self.getColumnWidth(1, 2)+(2*self.resources.lineWidth))
            yWid = int(self.getRowHeight(3, 5)+(2*self.resources.lineWidth))
            surface = self.scope.addBlur(x, y, xWid, yWid)
            self.scope.screen.blit(surface, (x,y))
            self.drawCritical(self.resources.headerFont)

    def drawHeaderText(self, font, bigFont):    

        width = self.scope.width
        height = self.scope.height
        row1Height = self.getRowStartHeight(1)

        antiAlias = False

        text = font.render("^A 571-C" , antiAlias , self.resources.ui_colour)
        lowTextHeight = int((row1Height/2+self.resources.lineWidth/2)-(text.get_height()/2)-(text.get_height()/2))
        self.scope.screen.blit(text, ((width/2)-(text.get_width()/2),lowTextHeight))

        text = font.render("REMOTE SENTRY WEAPON SYSTEM" , antiAlias , self.resources.ui_colour)
        highTextHeight = int((row1Height/2+self.resources.lineWidth)+(text.get_height()/2)-(text.get_height()/2))
        self.scope.screen.blit(text, ((width/2)-(text.get_width()/2),highTextHeight))

        #draw big letters
        centreTextHeight = int((row1Height/2)-(text.get_height()/2)-(0.75*self.resources.lineWidth))
        text = bigFont.render("C" , antiAlias , self.resources.ui_colour)
        self.scope.screen.blit(text, ((width/2-(width/2.5)-int(18*self.scope.scale_Width))-(text.get_width()/2),centreTextHeight))
        text = bigFont.render("C" , antiAlias , self.resources.ui_colour)
        self.scope.screen.blit(text, ((width/2+(width/2.5)+int(26*self.scope.scale_Width))-(text.get_width()/2),centreTextHeight))

    def drawPanelSubHeaderText(self, font):    

        colour = self.resources.ui_colour
        row2CentreHeight = self.getRowStartHeight(1) + (self.getRowHeight(1, 2)/2) + self.resources.thinLineWidth
        row3CentreHeight = self.getRowStartHeight(2) + (self.getRowHeight(2, 3)/2) + self.resources.thinLineWidth
        column8CentreWidth = self.getColumnStartWidth(7) + (self.getColumnWidth(7, 8)/2) + self.resources.thinLineWidth
        column10CentreWidth = self.getColumnStartWidth(9) + (self.getColumnWidth(9, 10)/2) + self.resources.thinLineWidth

        antiAlias = False

        #temp and R(M)
        text = font.render("Temp" , antiAlias , colour)
        self.scope.screen.blit(text, (int((column8CentreWidth)-(text.get_width()/2)),int(row2CentreHeight)-(text.get_height()/2)))
        text = font.render("R(M)" , antiAlias , colour)
        self.scope.screen.blit(text, (int((column10CentreWidth)-(text.get_width()/2)),int(row2CentreHeight)-(text.get_height()/2)))

    def drawLeftColumnText(self, font):

        colour = self.resources.ui_colour
        row3CentreHeight = self.getRowStartHeight(2) + (self.getRowHeight(2, 3)/2) + self.resources.thinLineWidth
        row6CentreHeight = self.getRowStartHeight(5) + (self.getRowHeight(5, 6)/2) + self.resources.thinLineWidth
        column2CentreWidth = self.getColumnStartWidth(1) + (self.getColumnWidth(1, 2)/2) + self.resources.thinLineWidth
        
        antiAlias = False

        #rounds remaining
        text = font.render("Rounds" , antiAlias , colour)
        self.scope.screen.blit(text, (int((column2CentreWidth)-(text.get_width()/2)),(int(row3CentreHeight-(text.get_height()/1.5)-(text.get_height()/2)))))
        text = font.render("Remaining" , antiAlias , colour)
        self.scope.screen.blit(text, (int((column2CentreWidth)-(text.get_width()/2)),(int(row3CentreHeight+(text.get_height()/1.5)-(text.get_height()/2)))))
        #rounds remaining
        text = font.render("TIME AT 100%" , antiAlias , colour)
        self.scope.screen.blit(text, (int((column2CentreWidth)-(text.get_width()/2)),(int(row6CentreHeight-(text.get_height()/1.5)-(text.get_height()/2)))))
        text = font.render("(secs)" , antiAlias , colour)
        self.scope.screen.blit(text, (int((column2CentreWidth)-(text.get_width()/2)),(int(row6CentreHeight+(text.get_height()/1.5)-(text.get_height()/2)))))

    def drawRoundsRemaining(self, font):

        colour = self.resources.ui_colour
        antiAlias = False

        row3CentreHeight = self.getRowStartHeight(2) + (self.getRowHeight(2, 4)/2) + self.resources.thinLineWidth
        column5CentreWidth = self.getColumnStartWidth(4) + (self.getColumnWidth(4, 5)/2) + self.resources.thinLineWidth

        text = font.render(str(self.currentRounds), antiAlias , colour)
        self.scope.screen.blit(text, (int((column5CentreWidth)-(text.get_width()/2)),(int(row3CentreHeight-(text.get_height()/2)))))

    def drawTimeRemaining(self, font):

        #calculate time remaining
        timeRemaining = self.currentRounds/15

        colour = self.resources.ui_colour
        antiAlias = False

        row6CentreHeight = self.getRowStartHeight(5) + (self.getRowHeight(5, 6)/2) + self.resources.thinLineWidth
        column5CentreWidth = self.getColumnStartWidth(4) + (self.getColumnWidth(4, 5)/2) + self.resources.thinLineWidth

        text = font.render('{0:.2f}'.format(timeRemaining) , antiAlias , colour)
        self.scope.screen.blit(text, (int((column5CentreWidth)-(text.get_width()/2)),(int(row6CentreHeight-(text.get_height()/2)))))

    def drawScaleLines(self, column, offset):

        columnStartWidth = self.getColumnStartWidth(column)
        columnEndWidth = self.getColumnStartWidth(column+1) - self.resources.thinLineWidth
        rowStartHeight = self.getRowStartHeight(2)
        rowEndHeight = self.getRowStartHeight(6)
        columnWidth = (self.getColumnWidth(column, column+1)) / 2
        scaleHeight = int(self.getRowHeight(2, 6))
        #vertical scale bar
        pygame.draw.rect(self.scope.screen, self.resources.ui_colour, (columnEndWidth+offset,rowStartHeight,self.resources.thinLineWidth, scaleHeight), 0)
        #bottom scale bar
        pygame.draw.rect(self.scope.screen, self.resources.ui_colour, (columnStartWidth+columnWidth+offset,rowEndHeight,columnWidth, self.resources.thinLineWidth), 0)
        #draw the large scale graduations
        for x in range(0, 6):
            graduationStartHeight = rowStartHeight+(int((scaleHeight/6)*x))
            pygame.draw.rect(self.scope.screen, self.resources.ui_colour, (columnStartWidth+1.75*columnWidth+offset-self.resources.thinLineWidth,graduationStartHeight,columnWidth/4+self.resources.thinLineWidth, self.resources.thinLineWidth), 0)
        #draw the small scale graduations
        for x in range(0, 6):
            graduationStartHeight = rowStartHeight+(int((scaleHeight/6)*x))
            pygame.draw.rect(self.scope.screen, self.resources.ui_colour, (columnStartWidth+1.875*columnWidth+offset-self.resources.thinLineWidth,graduationStartHeight+scaleHeight/12,columnWidth/8+self.resources.thinLineWidth, self.resources.thinLineWidth), 0)
        #draw the middle graduation mark
        graduationStartHeight = rowStartHeight+(int((scaleHeight/6)*3))
        pygame.draw.rect(self.scope.screen, self.resources.ui_colour, (columnStartWidth+1.5*columnWidth+offset,graduationStartHeight,columnWidth/2, self.resources.thinLineWidth), 0)

    def drawScale(self, column, offset, graphPercentageValue):

        columnStartWidth = self.getColumnStartWidth(column)
        rowEndHeight = self.getRowStartHeight(6)
        columnWidth = (self.getColumnWidth(column, column+1)) / 2
        scaleHeight = int(self.getRowHeight(2, 6))
        percentageHeight = (scaleHeight/100)*graphPercentageValue  

        #bottom bar graph
        pygame.draw.rect(self.scope.screen, self.resources.ui_colour, (columnStartWidth+columnWidth+offset,rowEndHeight-percentageHeight,columnWidth/2, percentageHeight), 0)

    def drawCritical(self, font):

        antiAlias = False

        columnStartWidth = self.getColumnStartWidth(1)
        rowStartHeight = self.getRowStartHeight(3)
        columnWidth = self.getColumnWidth(1, 2)
        rowHeight = self.getRowHeight(3,5)

        rowCentreHeight = self.getRowStartHeight(3) + (self.getRowHeight(3, 5)/2) + self.resources.thinLineWidth
        columnCentreWidth = self.getColumnStartWidth(1) + (self.getColumnWidth(1, 2)/2) + self.resources.thinLineWidth

        if self.criticalState==0 or self.criticalState==2:
            #outside bar
            pygame.draw.rect(self.scope.screen, self.resources.ui_colour, (columnStartWidth,rowStartHeight,columnWidth, 2*self.resources.lineWidth), 0)
            pygame.draw.rect(self.scope.screen, self.resources.ui_colour, (columnStartWidth,rowStartHeight+rowHeight-2*self.resources.lineWidth,columnWidth, 2*self.resources.lineWidth), 0)
            pygame.draw.rect(self.scope.screen, self.resources.ui_colour, (columnStartWidth,rowStartHeight, 2*self.resources.lineWidth,rowHeight), 0)
            pygame.draw.rect(self.scope.screen, self.resources.ui_colour, (columnStartWidth+columnWidth-2*self.resources.lineWidth,rowStartHeight,2*self.resources.lineWidth,rowHeight), 0)
            #innermost bar
            pygame.draw.rect(self.scope.screen, self.resources.ui_colour, (columnStartWidth+(4*self.resources.lineWidth),rowStartHeight+(4*self.resources.lineWidth),columnWidth-(8*self.resources.lineWidth), rowHeight-(8*self.resources.lineWidth)), 0)
            colour = self.resources.background_colour
        else:
            #inside bar
            pygame.draw.rect(self.scope.screen, self.resources.ui_colour, (columnStartWidth+2*self.resources.lineWidth,rowStartHeight+2*self.resources.lineWidth,columnWidth-(4*self.resources.lineWidth), 2*self.resources.lineWidth), 0)
            pygame.draw.rect(self.scope.screen, self.resources.ui_colour, (columnStartWidth+2*self.resources.lineWidth,rowStartHeight+rowHeight-(4*self.resources.lineWidth),columnWidth-(4*self.resources.lineWidth), 2*self.resources.lineWidth), 0)
            pygame.draw.rect(self.scope.screen, self.resources.ui_colour, (columnStartWidth+2*self.resources.lineWidth,rowStartHeight+(2*self.resources.lineWidth), 2*self.resources.lineWidth,rowHeight-(4*self.resources.lineWidth)), 0)
            pygame.draw.rect(self.scope.screen, self.resources.ui_colour, (columnStartWidth+columnWidth-(4*self.resources.lineWidth),rowStartHeight+(2*self.resources.lineWidth), 2*self.resources.lineWidth,rowHeight-(4*self.resources.lineWidth)), 0)
            colour = self.resources.ui_colour

        text = font.render("CRITICAL" , antiAlias , colour)
        self.scope.screen.blit(text, (int((columnCentreWidth)-(text.get_width()/2)),(int(rowCentreHeight-(text.get_height()/2)))))

        #when we get to 0 play the sound overlapping at every game loop
        if self.currentRounds==0:
            self.resources.end.play()

    #set the critical state. This is controlled by timer from main
    def setCriticalState(self):
        if self.currentRounds==0:
            self.criticalState=2
        else:
            if self.criticalState==0:
                self.criticalState=1
            else:
                self.criticalState=0

    #play the alert sound
    def playAlert(self):
        if self.currentRounds<=self.criticalValue and self.currentRounds>0:
            self.resources.warning.play()
 
