# -*- coding: utf-8 -*-

#############################################################################
#                                                                           #
# facade.py                                                                 #
#                                                                           #
#############################################################################

"""

Wrapper for "EIDEGraphics" so the "client" module just has to import
this code and instance EIDE.EIDEGraphics class to operate.

"""


import os
import os.path
import sys
import time
import pygame
pygame.init()



#############
# INIT CODE #
#############

# Catch working directory ('../EIDEGraphics') and append it to
# 'sys.path'
cwd = os.getcwd()
print ("facade.cwd1", os.getcwd())
head = os.path.split(cwd)[0]
os.chdir(head)
print ("facade2.cwd1", os.getcwd())
sys.path.append("/home/eide/Desktop/EIDE/EIDEGraphics")

import EIDE

import EIDEParser

# Get project to test.
# EIDE general parameters
systemParameters = (
# Platform: windows, linux, MAC
('Platform', 4),
# Text font and 'normal' size.
('font', 4),
('textStandardSize', 1),
# Significative figures
('sigFigures', 1),
# Language
('language', 4),
# Project
('project', 4),
)


##dirActual = os.getcwd()
##os.chdir("/home/eide/Desktop/EIDE/EIDEGraphics")
mainParser = EIDEParser.EIDEParser("/home/eide/Desktop/EIDE/EIDEGraphics",
    "EIDESystem.txt", systemParameters)
##print ("facade.parserSections", mainParser.sections())
##print ("facade.os.getcwd()", os.getcwd())
project = mainParser.get('EIDESystem', 'project')

# Add project path to 'sys.path'
projectPath = os.path.join(os.path.join(head, 'PROJECTS_N_EXAMPLES'), project)
sys.path.append(projectPath)
##import example              # User program code mock.
##os.chdir(dirActual)

