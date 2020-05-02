# -*- coding: utf-8 -*-

#############################################################################
#                                                                           #
# EIDEAnalog library. facade.py. Wrapper module for EIDEGraphics.           #
#                                                                           #
# Librería EIDEAnalog. facade.py. Módulo de interface para EIDEGraphics.    #
# Ver EIDEAnalog_ASI_SE_HIZO.pdf                                            #
# para más información (https://github.com/Clave-EIDEAnalog/DOCS)           #
#                                                                           #
# Copyright (c) 2020. Clave Ingenieros S.L.;                                #
# vicente.fombellida@claveingenieros.es                                     #
#                                                                           #
#############################################################################



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
head = os.path.split(cwd)[0]
os.chdir(head)
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

mainParser = EIDEParser.EIDEParser("/home/eide/Desktop/EIDE/EIDEGraphics",
    "EIDESystem.txt", systemParameters)
project = mainParser.get('EIDESystem', 'project')

# Add project path to 'sys.path'
projectPath = os.path.join(os.path.join(head, 'PROJECTS_N_EXAMPLES'), project)
sys.path.append(projectPath)

