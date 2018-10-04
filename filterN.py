#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 27 12:32:00 2018

@author: tiago
"""

# SOLO IMPORTAR LO SIGUIENTE SI SE CORRE EN PYTHON 2.X
from __future__ import division
#-----------------------------------------------------
import numpy as np


def filterN_Ep ( am, aM, wsN, chevOrBut):
    # Butter -> chevOrBut=0     Chevy-> chevOrBut=1
    epep = 10**(aM/10)-1
    epsilon = np.sqrt(epep)
    
    if chevOrBut == 0:
        n = np.ceil(np.log(np.sqrt((10**(am/10)-1)/(10**(aM/10)-1))) / np.log(wsN))
    elif chevOrBut == 1:
        n = np.ceil(np.arccosh(np.sqrt((10**(am/10)-1)/(10**(aM/10)-1))) / np.arccosh(wsN))
    else:
        print("El tipo que se ingreso en filterN no es valido.")

    return epsilon, epep, n