from __future__ import division
import pygame, os

#define class to describe the setup panel 
class setupPanel():

    scope = None
    resources = None

    def __init__(self, scope, resources):

        #define column and rows
        #column is multi-dimensional. We have column[] == to the justification column and then column[][] representing column
        #width percentages
        self.columns = [[1], [0.24,0.19,0.23,0.34], [0.28,0.34,0.38]]
        self.rows = [0.16,0.12,0.02,0.04,0.04,0.04,0.04,0.06,0.12,0.02,0.04,0.04,0.04,0.22]

        #sort out the defaults for the headings
        self.justificationColumn = 1
        self.selectedColumn = 0
        self.selectedHeaderRow = -1
        self.topHeaderRow = 1
        self.bottomHeaderRow = 8

        #sort out the defaults for the menu items
        self.populatedMenuItemRowsTop=[3,2,4,2]
        self.polulatedMenuItemRowsBot=[3,2,3]
        self.selectedMenuItemRow = -1
        self.topMenuItemStartRow = 3
        self.bottomMenuItemStartRow = 10
        self.scope = scope
        self.resources = resources

        self.lockedItems = []

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

        if (initialiseRowsAndColumns):
            self.selectedHeaderRow = 1
            self.selectedMenuItemRow = 3

    #increment the column selection
    def incrementSelectedColumn(self, incrementMenuColumn):

        currentColumn = self.selectedColumn

        self.selectedColumn = self.selectedColumn+incrementMenuColumn
        if self.selectedColumn>len(self.columns[self.justificationColumn])-1:
            #increment justificationColumn
            self.justificationColumn=self.justificationColumn+1
            if self.justificationColumn>len(self.columns)-1:
                self.justificationColumn = 1
            #reset selectedColumnIndex
            self.selectedColumn = 0
            #reset selectedRowIndex
            if self.justificationColumn==1:
                self.selectedHeaderRow = self.topHeaderRow
            else:
                self.selectedHeaderRow = self.bottomHeaderRow
        if self.selectedColumn<0:
            #decrement justificationColumn
            self.justificationColumn=self.justificationColumn-1
            if self.justificationColumn<1:
                self.justificationColumn = len(self.columns)-1
            #reset selectedColumnIndex
            self.selectedColumn = len(self.columns[self.justificationColumn])-1
            #reset selectedRowIndex
            if self.justificationColumn==1:
                self.selectedHeaderRow = self.topHeaderRow
            else:
                self.selectedHeaderRow = self.bottomHeaderRow

        if currentColumn!=self.selectedColumn:
            #is there already a locked item in this column? if so navigate to it
            for lockedItem in self.lockedItems:
                lockedJustificationColumn = lockedItem[0]
                lockedSelectedColumn = lockedItem[1]
                lockedSelectedMenuItemRow = lockedItem[2]
                if self.justificationColumn==lockedJustificationColumn and self.selectedColumn==lockedSelectedColumn:
                     self.selectedMenuItemRow = lockedSelectedMenuItemRow
                     return
            
            if self.justificationColumn==1:
                self.selectedMenuItemRow = self.topMenuItemStartRow
            else:
                self.selectedMenuItemRow = self.bottomMenuItemStartRow
            

    #increment the row selection
    def incrementSelectedRow(self, incrementMenuRow):

        if self.justificationColumn == 1:
            populatedRows = self.populatedMenuItemRowsTop[self.selectedColumn]
            startRow = self.topMenuItemStartRow
        else:
            populatedRows = self.polulatedMenuItemRowsBot[self.selectedColumn]
            startRow = self.bottomMenuItemStartRow
            
        self.selectedMenuItemRow = self.selectedMenuItemRow+incrementMenuRow
        if self.selectedMenuItemRow==(startRow + populatedRows):
            self.selectedMenuItemRow = startRow
        if self.selectedMenuItemRow<(startRow):
            self.selectedMenuItemRow = startRow + populatedRows-1

    #check if the mouse movement has resulted in a selection having been made in any of the menu item rows
    def checkMouseSelection(self, mouseX, mouseY):
        #print("inhere")
        return
        if self.justificationColumn == 1:
            populatedRows = self.populatedMenuItemRowsTop[self.selectedColumn]
            startRow = self.topMenuItemStartRow
        else:
            populatedRows = self.polulatedMenuItemRowsBot[self.selectedColumn]
            startRow = self.bottomMenuItemStartRow
            
        self.selectedMenuItemRow = self.selectedMenuItemRow+incrementMenuRow
        if self.selectedMenuItemRow==(startRow + populatedRows):
            self.selectedMenuItemRow = startRow
        if self.selectedMenuItemRow<(startRow):
            self.selectedMenuItemRow = startRow + populatedRows-1

    def render(self, event):

        if event=="MOUSEMOTION":
            Mouse_x, Mouse_y = pygame.mouse.get_pos()
            self.checkMouseSelection(Mouse_x, Mouse_y)
        elif event=="RESIZE":
            self.renderBackground(False)
        else:
            incrementMenuColumn = 0
            incrementMenuRow = 0
            if event==pygame.K_UP:
                incrementMenuRow = -1
            if event==pygame.K_DOWN:
                incrementMenuRow = 1
            if event==pygame.K_LEFT:
                incrementMenuColumn = -1
            if event==pygame.K_RIGHT:
                incrementMenuColumn = 1
            if event==pygame.K_RETURN:
                self.lockItems()

            #update user interaction
            self.incrementSelectedColumn(incrementMenuColumn)
            self.incrementSelectedRow(incrementMenuRow)

        #draw the blurred background image
        self.scope.screen.blit(self.blurredImage, (0, 0))

        #draw the menu heading selection boxes
        self.drawSelectedMenuHeading()

        #draw the menu item selection boxes
        self.drawSelectedMenuItem()

        #draw the locked items
        self.drawLockedItems()
        
        #redraw the graphics to account for blur
        self.drawPanel()
    
    #define function to provide y start coordinate of selected row
    def getRowStartHeight(self, rowNum):

        height = 0
        for x in range(rowNum):
            height = height + (self.rows[x]*self.scope.height)

        return height

    #define function to get the the width of a column spanning between column indices
    def getColumnWidth(self, justificationRowNum, columnStart, columnEnd):

        column = self.columns[justificationRowNum]
        width = 0
        for x in range(columnStart, columnEnd):
            width = width + (column[x]*self.scope.width)

        return width

    #define function to provide y start coordinate of selected row
    def getColumnStartWidth(self, rowNum, columnNum):

        column = self.columns[rowNum]       
        width = 0
        for x in range(columnNum):
            width = width + (column[x]*self.scope.width)

        return width

    #define function to provide row thickness
    def getRowHeight(self, rowStart, rowEnd):

        height = 0
        for x in range(rowStart, rowEnd):
            height = height + (self.rows[x]*self.scope.height)

        return height
        
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
   
    def drawTable(self):

        width = self.scope.width
        height = self.scope.height
        row1Height = self.getRowStartHeight(1)
        row2Height = self.getRowStartHeight(2)
        row3Height = self.getRowStartHeight(8)
        row4Height = self.getRowStartHeight(9)

        row2Column1Width = self.getColumnStartWidth(1, 1)
        row2Column2Width = self.getColumnStartWidth(1, 2)
        row2Column3Width = self.getColumnStartWidth(1, 3)
        row3Column1Width = self.getColumnStartWidth(2, 1)
        row3Column2Width = self.getColumnStartWidth(2, 2)
        
        #draw top line
        pygame.draw.rect(self.scope.screen, self.resources.ui_colour, (self.resources.borderOffset, int(row2Height), width-(2*self.resources.borderOffset), self.resources.thinLineWidth), 0)

        #draw bottom lines
        pygame.draw.rect(self.scope.screen, self.resources.ui_colour, (self.resources.borderOffset, int(row3Height), width-(2*self.resources.borderOffset), self.resources.thinLineWidth), 0)
        pygame.draw.rect(self.scope.screen, self.resources.ui_colour, (self.resources.borderOffset, int(row4Height), width-(2*self.resources.borderOffset), self.resources.thinLineWidth), 0)

        #draw the columns - top row column 1
        pygame.draw.rect(self.scope.screen, self.resources.ui_colour, (int(row2Column1Width-0.75*self.resources.thinLineWidth), int(row1Height), self.resources.thinLineWidth, int(self.getRowHeight(1, 8))), 0)
        pygame.draw.rect(self.scope.screen, self.resources.ui_colour, (int(row2Column1Width+0.75*self.resources.thinLineWidth), int(row1Height), self.resources.thinLineWidth, int(self.getRowHeight(1, 8))), 0)

        #draw the columns - top row column 2
        pygame.draw.rect(self.scope.screen, self.resources.ui_colour, (int(row2Column2Width-0.75*self.resources.thinLineWidth), int(row1Height), self.resources.thinLineWidth, int(self.getRowHeight(1, 8))), 0)
        pygame.draw.rect(self.scope.screen, self.resources.ui_colour, (int(row2Column2Width+0.75*self.resources.thinLineWidth), int(row1Height), self.resources.thinLineWidth, int(self.getRowHeight(1, 8))), 0)

        #draw the columns - top row column 3
        pygame.draw.rect(self.scope.screen, self.resources.ui_colour, (int(row2Column3Width-0.75*self.resources.thinLineWidth), int(row1Height), self.resources.thinLineWidth, int(self.getRowHeight(1, 8))), 0)
        pygame.draw.rect(self.scope.screen, self.resources.ui_colour, (int(row2Column3Width+0.75*self.resources.thinLineWidth), int(row1Height), self.resources.thinLineWidth, int(self.getRowHeight(1, 8))), 0)

        #draw the columns - bottom row column 1
        pygame.draw.rect(self.scope.screen, self.resources.ui_colour, (int(row3Column1Width-0.75*self.resources.thinLineWidth), int(row3Height), self.resources.thinLineWidth, int(self.getRowHeight(8, 14))), 0)
        pygame.draw.rect(self.scope.screen, self.resources.ui_colour, (int(row3Column1Width+0.75*self.resources.thinLineWidth), int(row3Height), self.resources.thinLineWidth, int(self.getRowHeight(8, 14))), 0)

        #draw the columns - bottom row column 2
        pygame.draw.rect(self.scope.screen, self.resources.ui_colour, (int(row3Column2Width-0.75*self.resources.thinLineWidth), int(row3Height), self.resources.thinLineWidth, int(self.getRowHeight(8, 14))), 0)
        pygame.draw.rect(self.scope.screen, self.resources.ui_colour, (int(row3Column2Width+0.75*self.resources.thinLineWidth), int(row3Height), self.resources.thinLineWidth, int(self.getRowHeight(8, 14))), 0)

    def drawPanel(self):

        self.drawBorder()
        self.drawHeaderText(self.resources.headerFont, self.resources.bigHeaderFont)
        #draw the panel A subheadings
        self.drawPanelSubHeaderText(self.resources.subHeaderFont)
        #draw the panel A menuitems
        self.drawPanelMenuItems(self.resources.menuItemFont)
        #draw the table lines
        self.drawTable()

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

        width = self.scope.width
        height = self.scope.height
        row2CentreHeight = self.getRowStartHeight(1) + (self.getRowHeight(1, 2)/2) + self.resources.thinLineWidth
        row8CentreHeight = self.getRowStartHeight(8) + (self.getRowHeight(8, 9)/2) + self.resources.thinLineWidth

        antiAlias = False

        #1st row, 1st column
        colour = self.getHeaderTextColour(1, 0, 1)
        text = font.render("SYSTEM" , antiAlias , colour)
        self.scope.screen.blit(text, ((int(70*self.scope.scale_Width))-(text.get_width()/2),(int(row2CentreHeight-(text.get_height()/1.5)-(text.get_height()/2)))))
        text = font.render("MODE" , antiAlias , colour)
        self.scope.screen.blit(text, ((int(70*self.scope.scale_Width))-(text.get_width()/2),(int(row2CentreHeight+(text.get_height()/1.5)-(text.get_height()/2)))))

        #1st row, 2nd column
        colour = self.getHeaderTextColour(1, 1, 1)
        text = font.render("WEAPON" , antiAlias , colour)
        self.scope.screen.blit(text, ((int(210*self.scope.scale_Width))-(text.get_width()/2),(int(row2CentreHeight-(text.get_height()/1.5)-(text.get_height()/2)))))
        text = font.render("STATUS" , antiAlias , colour)
        self.scope.screen.blit(text, ((int(210*self.scope.scale_Width))-(text.get_width()/2),(int(row2CentreHeight+(text.get_height()/1.5)-(text.get_height()/2)))))

        #1st row, 3rd column
        colour = self.getHeaderTextColour(1, 2, 1)
        text = font.render("IFF" , antiAlias , colour)
        self.scope.screen.blit(text, ((int(350*self.scope.scale_Width))-(text.get_width()/2),(int(row2CentreHeight-(text.get_height()/1.5)-(text.get_height()/2)))))
        text = font.render("STATUS" , antiAlias , colour)
        self.scope.screen.blit(text, ((int(350*self.scope.scale_Width))-(text.get_width()/2),(int(row2CentreHeight+(text.get_height()/1.5)-(text.get_height()/2)))))

        #1st row, 4th column
        colour = self.getHeaderTextColour(1, 3, 1)
        text = font.render("TEST" , antiAlias , colour)
        self.scope.screen.blit(text, ((int(500*self.scope.scale_Width))-(text.get_width()/2),(int(row2CentreHeight-(text.get_height()/1.5)-(text.get_height()/2)))))
        text = font.render("ROUTINE" , antiAlias , colour)
        self.scope.screen.blit(text, ((int(500*self.scope.scale_Width))-(text.get_width()/2),(int(row2CentreHeight+(text.get_height()/1.5)-(text.get_height()/2)))))

        #2nd row, 1st column
        colour = self.getHeaderTextColour(2, 0, 8)
        text = font.render("TARGET PROFILE" , antiAlias , colour)
        self.scope.screen.blit(text, ((int(100*self.scope.scale_Width))-(text.get_width()/2),(int(row8CentreHeight-(text.get_height()/2)))))

        #2nd row, 2nd column
        colour = self.getHeaderTextColour(2, 1, 8)
        text = font.render("SPECTRAL PROFILE" , antiAlias , colour)
        self.scope.screen.blit(text, ((int(290*self.scope.scale_Width))-(text.get_width()/2),(int(row8CentreHeight-(text.get_height()/2)))))

        #2nd row, 3rd column
        colour = self.getHeaderTextColour(2, 2, 8)
        text = font.render("TARGET SELECT" , antiAlias , colour)
        self.scope.screen.blit(text, ((int(510*self.scope.scale_Width))-(text.get_width()/2),(int(row8CentreHeight-(text.get_height()/2)))))

    def drawPanelMenuItems(self, font):    

        row3CentreHeight = self.getRowStartHeight(3) + (self.getRowHeight(3, 4)/2) + self.resources.thinLineWidth
        row4CentreHeight = self.getRowStartHeight(4) + (self.getRowHeight(4, 5)/2) + self.resources.thinLineWidth
        row5CentreHeight = self.getRowStartHeight(5) + (self.getRowHeight(5, 6)/2) + self.resources.thinLineWidth
        row6CentreHeight = self.getRowStartHeight(6) + (self.getRowHeight(6, 7)/2) + self.resources.thinLineWidth

        row9CentreHeight = self.getRowStartHeight(10) + (self.getRowHeight(10, 11)/2) + self.resources.thinLineWidth
        row10CentreHeight = self.getRowStartHeight(11) + (self.getRowHeight(11, 12)/2) + self.resources.thinLineWidth
        row11CentreHeight = self.getRowStartHeight(12) + (self.getRowHeight(12, 13)/2) + self.resources.thinLineWidth

        antiAlias = False

        #1st row, 1st column
        colour = self.getMenuItemTextColour(1, 0, 3)
        text = font.render("AUTO-REMOTE" , antiAlias , colour)
        self.scope.screen.blit(text, ((int(85*self.scope.scale_Width))-(text.get_width()/2),(int(row3CentreHeight))-(text.get_height()/2)))
        colour = self.getMenuItemTextColour(1, 0, 4)
        text = font.render("MAN-OVERRIDE" , antiAlias , colour)
        self.scope.screen.blit(text, ((int(85*self.scope.scale_Width))-(text.get_width()/2),(int(row4CentreHeight))-(text.get_height()/2)))
        colour = self.getMenuItemTextColour(1, 0, 5)
        text = font.render("SEMI-AUTO" , antiAlias , colour)
        self.scope.screen.blit(text, ((int(85*self.scope.scale_Width))-(text.get_width()/2),(int(row5CentreHeight))-(text.get_height()/2)))

        #1st row, 2nd column
        colour = self.getMenuItemTextColour(1, 1, 3)
        text = font.render("SAFE" , antiAlias , colour)
        self.scope.screen.blit(text, ((int(210*self.scope.scale_Width))-(text.get_width()/2),(int(row3CentreHeight))-(text.get_height()/2)))
        colour = self.getMenuItemTextColour(1, 1, 4)
        text = font.render("ARMED" , antiAlias , colour)
        self.scope.screen.blit(text, ((int(210*self.scope.scale_Width))-(text.get_width()/2),(int(row4CentreHeight))-(text.get_height()/2)))

        #1st row, 3rd column
        colour = self.getMenuItemTextColour(1, 2, 3)
        text = font.render("SEARCH" , antiAlias , colour)
        self.scope.screen.blit(text, ((int(350*self.scope.scale_Width))-(text.get_width()/2),(int(row3CentreHeight))-(text.get_height()/2)))
        colour = self.getMenuItemTextColour(1, 2, 4)
        text = font.render("TEST" , antiAlias , colour)
        self.scope.screen.blit(text, ((int(350*self.scope.scale_Width))-(text.get_width()/2),(int(row4CentreHeight))-(text.get_height()/2)))
        colour = self.getMenuItemTextColour(1, 2, 5)
        text = font.render("ENGAGED" , antiAlias , colour)
        self.scope.screen.blit(text, ((int(350*self.scope.scale_Width))-(text.get_width()/2),(int(row5CentreHeight))-(text.get_height()/2)))
        colour = self.getMenuItemTextColour(1, 2, 6)
        text = font.render("INTERROGATE" , antiAlias , colour)
        self.scope.screen.blit(text, ((int(350*self.scope.scale_Width))-(text.get_width()/2),(int(row6CentreHeight))-(text.get_height()/2)))

        #1st row, 4th column
        colour = self.getMenuItemTextColour(1, 3, 3)
        text = font.render("AUTO" , antiAlias , colour)
        self.scope.screen.blit(text, ((int(500*self.scope.scale_Width))-(text.get_width()/2),(int(row3CentreHeight))-(text.get_height()/2)))
        colour = self.getMenuItemTextColour(1, 3, 4)
        text = font.render("SELECTIVE" , antiAlias , colour)
        self.scope.screen.blit(text, ((int(500*self.scope.scale_Width))-(text.get_width()/2),(int(row4CentreHeight))-(text.get_height()/2)))

        #2nd row, 1st column
        colour = self.getMenuItemTextColour(2, 0, 10)
        text = font.render("SOFT" , antiAlias , colour)
        self.scope.screen.blit(text, ((int(100*self.scope.scale_Width))-(text.get_width()/2),(int(row9CentreHeight))-(text.get_height()/2)))
        colour = self.getMenuItemTextColour(2, 0, 11)
        text = font.render("SEMIHARD" , antiAlias , colour)
        self.scope.screen.blit(text, ((int(100*self.scope.scale_Width))-(text.get_width()/2),(int(row10CentreHeight))-(text.get_height()/2)))
        colour = self.getMenuItemTextColour(2, 0, 12)
        text = font.render("HARD" , antiAlias , colour)
        self.scope.screen.blit(text, ((int(100*self.scope.scale_Width))-(text.get_width()/2),(int(row11CentreHeight))-(text.get_height()/2)))

        #2nd row, 2nd column
        colour = self.getMenuItemTextColour(2, 1, 10)
        text = font.render("BIO" , antiAlias , colour)
        self.scope.screen.blit(text, ((int(290*self.scope.scale_Width))-(text.get_width()/2),(int(row9CentreHeight))-(text.get_height()/2)))
        colour = self.getMenuItemTextColour(2, 1, 11)
        text = font.render("INERT" , antiAlias , colour)
        self.scope.screen.blit(text, ((int(290*self.scope.scale_Width))-(text.get_width()/2),(int(row10CentreHeight))-(text.get_height()/2)))

        #2nd row, 3rd column
        colour = self.getMenuItemTextColour(2, 2, 10)
        text = font.render("MULTI SPEC" , antiAlias , colour)
        self.scope.screen.blit(text, ((int(510*self.scope.scale_Width))-(text.get_width()/2),(int(row9CentreHeight))-(text.get_height()/2)))
        colour = self.getMenuItemTextColour(2, 2, 11)
        text = font.render("INFRA RED" , antiAlias , colour)
        self.scope.screen.blit(text, ((int(510*self.scope.scale_Width))-(text.get_width()/2),(int(row10CentreHeight))-(text.get_height()/2)))
        colour = self.getMenuItemTextColour(2, 2, 12)
        text = font.render("UV" , antiAlias , colour)
        self.scope.screen.blit(text, ((int(510*self.scope.scale_Width))-(text.get_width()/2),(int(row11CentreHeight))-(text.get_height()/2)))

    #draw the selected menu heading
    def drawSelectedMenuHeading(self):
        rowStart = self.getRowStartHeight(self.selectedHeaderRow)+self.resources.thinLineWidth
        rowHeight = self.getRowHeight(self.selectedHeaderRow, self.selectedHeaderRow+1)
        columnStart = self.getColumnStartWidth(self.justificationColumn, self.selectedColumn)+self.resources.thinLineWidth
        columnWidth = self.getColumnWidth(self.justificationColumn, self.selectedColumn, self.selectedColumn+1)-self.resources.thinLineWidth
        pygame.draw.rect(self.scope.screen, self.resources.ui_colour, (int(columnStart), int(rowStart), int(columnWidth), int(rowHeight)), 0)

    #draw the selected menu heading
    def drawSelectedMenuItem(self):
        rowStart = self.getRowStartHeight(self.selectedMenuItemRow)+self.resources.thinLineWidth
        rowHeight = self.getRowHeight(self.selectedMenuItemRow, self.selectedMenuItemRow+1)
        columnStart = self.getColumnStartWidth(self.justificationColumn, self.selectedColumn)+self.resources.thinLineWidth
        columnWidth = self.getColumnWidth(self.justificationColumn, self.selectedColumn, self.selectedColumn+1)-self.resources.thinLineWidth
        pygame.draw.rect(self.scope.screen, self.resources.ui_colour, (int(columnStart), int(rowStart), int(columnWidth), int(rowHeight)), 0)

        #don't blur an already locked selection
        for lockedItem in self.lockedItems:        
            lockedJustificationColumn = lockedItem[0]
            lockedSelectedColumn = lockedItem[1]
            lockedSelectedMenuItemRow = lockedItem[2]
            if (self.justificationColumn==lockedJustificationColumn and self.selectedColumn==lockedSelectedColumn and self.selectedMenuItemRow==lockedSelectedMenuItemRow):
                return
        
        if self.scope.numberOfBlurLoops!=0:  
            #draw blur
            x = (int(columnStart))
            y = (int(rowStart-self.resources.lineWidth))
            xWid = (int(columnWidth))
            yWid = (int(rowHeight+(2*self.resources.lineWidth)))

            if x<0:
                x=0
            if x+xWid>self.scope.width:
                xWid = self.scope.width-x
            
            surface = self.scope.addBlur(x, y, xWid, yWid)
            self.scope.screen.blit(surface, (x,y))
        #overlay the original image on top of blur
        pygame.draw.rect(self.scope.screen, self.resources.ui_colour, (int(columnStart), int(rowStart), int(columnWidth), int(rowHeight)), 0)

    #get the header text colour
    def getHeaderTextColour(self, justificationColumn, selectedColumn, selectedHeaderRow):
        #colour the locked item text
        for lockedItem in self.lockedItems:        
            lockedJustificationColumn = lockedItem[0]
            lockedSelectedColumn = lockedItem[1]
            lockedSelectedHeaderRow = lockedItem[2]
            if (justificationColumn==lockedJustificationColumn and selectedColumn==lockedSelectedColumn and selectedHeaderRow==lockedSelectedHeaderRow):
                return self.resources.background_colour
        
        if (self.justificationColumn==justificationColumn and self.selectedColumn==selectedColumn and self.selectedHeaderRow==selectedHeaderRow):
            return self.resources.background_colour
        else:
            return self.resources.ui_colour

    def getMenuItemTextColour(self, justificationColumn, selectedColumn, selectedMenuItemRow):

        #colour the locked item text
        for lockedItem in self.lockedItems:        
            lockedJustificationColumn = lockedItem[0]
            lockedSelectedColumn = lockedItem[1]
            lockedSelectedMenuItemRow = lockedItem[2]
            if (justificationColumn==lockedJustificationColumn and selectedColumn==lockedSelectedColumn and selectedMenuItemRow==lockedSelectedMenuItemRow):
                return self.resources.background_colour
        
        if (self.justificationColumn==justificationColumn and self.selectedColumn==selectedColumn and self.selectedMenuItemRow==selectedMenuItemRow):
            return self.resources.background_colour
        else:
            return self.resources.ui_colour

    #lock in selections for rendering
    def lockItems(self):
        #lock in an array containing the following indices
        #[0] selected justification column
        #[1] selected column
        #[2] selected header row
        #[3] selected menu item row
        #is there already a locked item in this column? if so remove it and add the new one
        x = 0
        for lockedItem in (self.lockedItems):
            lockedJustificationColumn = lockedItem[0]
            lockedSelectedColumn = lockedItem[1]
            lockedSelectedMenuItemRow = lockedItem[2]           
            if self.justificationColumn==lockedJustificationColumn and self.selectedColumn==lockedSelectedColumn:
                del self.lockedItems[x]
                break
            #increment x
            x = x+1
            
        self.lockedItems.append([self.justificationColumn, self.selectedColumn, self.selectedMenuItemRow])

        #play the menu select sound
        self.resources.warning.play()

        #increase the column index
        self.incrementSelectedColumn(1)

    #draw the selected menu heading
    def drawLockedItems(self):
        for lockedItem in self.lockedItems:
            justificationColumn = lockedItem[0]
            selectedColumn = lockedItem[1]
            selectedMenuItemRow = lockedItem[2]
            #draw the menu items
            rowStart = self.getRowStartHeight(selectedMenuItemRow)+self.resources.thinLineWidth
            rowHeight = self.getRowHeight(selectedMenuItemRow, selectedMenuItemRow+1)
            columnStart = self.getColumnStartWidth(justificationColumn, selectedColumn)+self.resources.thinLineWidth
            columnWidth = self.getColumnWidth(justificationColumn, selectedColumn, selectedColumn+1)-self.resources.thinLineWidth
            pygame.draw.rect(self.scope.screen, self.resources.ui_colour, (int(columnStart), int(rowStart), int(columnWidth), int(rowHeight)), 0)
            if self.scope.numberOfBlurLoops!=0:
                #draw blur
                x = (int(columnStart))
                y = (int(rowStart-self.resources.lineWidth))
                xWid = (int(columnWidth))
                yWid = (int(rowHeight+(2*self.resources.lineWidth)))

                if x<0:
                    x=0
                if x+xWid>self.scope.width:
                    xWid = self.scope.width-x
            
                surface = self.scope.addBlur(x, y, xWid, yWid)
                self.scope.screen.blit(surface, (x,y))
            #overlay the original image on top of blur
            pygame.draw.rect(self.scope.screen, self.resources.ui_colour, (columnStart, rowStart, columnWidth,rowHeight), 0)

        


        
