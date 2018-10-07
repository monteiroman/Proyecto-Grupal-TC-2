#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 20 18:30:41 2018

@author: tiago
"""
import numpy as np
import scipy.signal as sig
#import matplotlib as mpl
from splane import analyze_sys


#vectores auxiliares para imprimir los graficos de los sistemas
all_sys = []
filter_names = []

# Constantes del filtro Besselworth
fc = 40

# Constatens del filtro Butterworth y Bessel
order2analyze = 4


#____________Butter____________

z,p,k = sig.buttap(order2analyze)

num, den = sig.zpk2tf(z,p,k)

all_sys.append(sig.TransferFunction(num,den))

filter_names.append('Butter orden '+str(order2analyze))



#____________Bessel____________

z,p,k = sig.besselap(order2analyze, norm='mag')

num, den = sig.zpk2tf(z,p,k)

all_sys.append(sig.TransferFunction(num,den))

filter_names.append('Bessel orden '+str(order2analyze))



#____________Besselworth____________

#Coeficientes de la transferencia obtenida con Tina normalizada con C4 = 10nf (3)
#num = [(2.81*10**(-6))*(fc*2*np.pi), 1]
#den = [(7.21*10**(-16))*((fc*2*np.pi)**4), (9.21*10**(-11))*((fc*2*np.pi)**3),
#       (1.98*10**(-6))*((fc*2*np.pi)**2), (2.47*10**(-3))*(fc*2*np.pi), 1]

#Coeficientes de la transferencia obtenida con Tina normalizada con C4 = 100nf (2)
#num = [(2.81*10**(-6))*(fc*2*np.pi), 1]
#den = [(7.21*10**(-15))*((fc*2*np.pi)**4), (7.54*10**(-10))*((fc*2*np.pi)**3),
#       (2.84*10**(-6))*((fc*2*np.pi)**2), (2.82*10**(-3))*(fc*2*np.pi), 1]

#Coeficientes de la transferencia obtenida con Tina normalizada con C4 = 1uF (1)
num = [(2.81*10**(-6))*(fc*2*np.pi), 1]
den = [(7.21*10**(-14))*((fc*2*np.pi)**4), (7.38*10**(-9))*((fc*2*np.pi)**3), 
       (1.14*10**(-5))*((fc*2*np.pi)**2), (6.33*10**(-3))*(fc*2*np.pi), 1]

tf = sig.TransferFunction(num, den)

 

print ("*Coeficientes de la transferencia Besselworth NORMALIZADA:\n")
print ("\tNumerador:")
for c in tf.num:
    print(f"\t\t{c:.3f}")
print ("\tDenominador:")
for c in tf.den:
    print(f"\t\t{c:.3f}")
print ("\n")

print ("*Polos y ceros de la transferencia Besselworth NORMALIZADA:\n")
print ("\tPolos:")
for c in tf.poles:
    print(f"\t\t{c:.3f}")
print ("\tCeros:")
for c in tf.zeros:
    print(f"\t\t{c:.3f}")


all_sys.append(tf)
filter_names.append("Besselworth orden 4")

#Defino el rango a imprimir y el punto a mostrar
ini = 0.1
end = 10.1
n = 100000
bode_lenght = np.linspace(ini, end, n)
printW = 1
#imprimo todos los Bode
analyze_sys( all_sys, filter_names, bode_lenght, printW=printW)


