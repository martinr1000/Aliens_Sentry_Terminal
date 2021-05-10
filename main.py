from __future__ import division
import pygame, os
from pyscope import pyscope
from resources import resources
from setupPanel import setupPanel
from trackPanel import trackPanel

#initialise required game classes
#setup graphics scope
scope=pyscope()

#initialise resources
resources=resources()
resources.initFonts(scope)

#initialise panels
setupPanelInstance=setupPanel(scope, resources)
setupPanelInstance.renderBackground(True)
trackPanelInstance=trackPanel(scope, resources)
trackPanelInstance.renderBackground(True)

running = True
setupPanel = True
trackPanel = False

clock = pygame.time.Clock()
start_time_critical = pygame.time.get_ticks()
start_time_warning = pygame.time.get_ticks()
while running:

    elapsed_time_critical = pygame.time.get_ticks() - start_time_critical
    elapsed_time_warning = pygame.time.get_ticks() - start_time_warning
    if elapsed_time_critical>=200:
        trackPanelInstance.setCriticalState()
        start_time_critical = pygame.time.get_ticks()
    if elapsed_time_warning>=300:
        trackPanelInstance.playAlert()
        start_time_warning = pygame.time.get_ticks()

    #process pygame events
    ev = "none"
    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
            running = False # Flag that we are done so we exit this loop
            ev = "none"
            pass
        if event.type == pygame.KEYDOWN:
            if event.key==pygame.K_ESCAPE:
                running = False
            if event.key==pygame.K_SPACE:
                if setupPanel:
                    trackPanelInstance.renderBackground(False)
                    setupPanel=False
                    trackPanel=True
                else:
                    setupPanelInstance.renderBackground(False)
                    setupPanel=True
                    trackPanel=False
            if (event.key==pygame.K_f):
                if scope.screen.get_flags() & pygame.FULLSCREEN:
                    scope.toggle_fullscreen("RESIZABLE")
                    pygame.display.set_icon(resources.icon)
                    resources.initFonts(scope)
                    ev = "RESIZE" 
                else:
                    scope.toggle_fullscreen("FULLSCREEN")
                    resources.initFonts(scope)
                    ev = "RESIZE" 
            if event.key==pygame.K_UP:
                ev = event.key
            if event.key==pygame.K_DOWN:
                ev = event.key 
            if event.key==pygame.K_LEFT:
                ev = event.key
            if event.key==pygame.K_RIGHT:
                ev = event.key
            if event.key==pygame.K_RETURN:
                ev = event.key
        if event.type == pygame.MOUSEMOTION:
            ev = "MOUSEMOTION"
        if event.type == pygame.VIDEORESIZE:
            scope.resize(event)
            resources.initFonts(scope)
            ev = "RESIZE"            
                
    #render the screen graphics
    if setupPanel:
        setupPanelInstance.render(ev)
    else:
        trackPanelInstance.render(ev)
                    
    pygame.display.flip()
    clock.tick(30)

pygame.quit()
