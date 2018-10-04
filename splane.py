# -*- coding: utf-8 -*-
"""
Combination of 
http://scipy-central.org/item/52/1/zplane-function
and
http://www.dsprelated.com/showcode/244.php
with my own modifications
Further modifications were added for didactic purposes
"""

# Copyright (c) 2011 Christopher Felton
# 2018 modified by Andres Di Donato
# 2018 modified by Mario Llamendi Osorio

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


# The following is derived from the slides presented by
# Alexander Kain for CS506/606 "Special Topics: Speech Signal Processing"
# CSLU / OHSU, Spring Term 2011.

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import patches
from collections import defaultdict
from scipy.signal import tf2zpk,tf2sos


def analyze_sys( all_sys, aprox_name, bode_lenght=None, n=100, printW=-1):
    
#    %matplotlib qt5
#    %matplotlib inline
    
#   img_ext = 'none'
#    img_ext = 'png'
    img_ext = 'svg'
    
    cant_sys = len(all_sys)

    ## BODE plots
    fig_id = 1
    axes_hdl = ()
    
    print("\n\n")

    for ii in range(cant_sys):
        fig_id, axes_hdl = bodePlot(all_sys[ii], aprox_name[ii], fig_id, 
                                    axes_hdl, bode_lenght, n, printW)

    axes_hdl[0].legend(aprox_name)

    if img_ext != 'none':
        plt.savefig('-'.join(aprox_name) + '-Bode.' + img_ext, format=img_ext)

    ## PZ Maps
    fig_id = 2
    axes_hdl = ()
    
    for ii in range(cant_sys):
        fig_id, axes_hdl = pzmap(all_sys[ii], aprox_name[ii], fig_id, axes_hdl)

    axes_hdl.legend()

    if img_ext != 'none':
        plt.figure(fig_id)
        plt.savefig('-'.join(aprox_name) + '-PZmap.' + img_ext, format=img_ext)
    
    
    ## Group delay plots
    fig_id = 3
    
    for ii in range(cant_sys):
        fig_id, axes_hdl = grpDelay(all_sys[ii], fig_id, bode_lenght)
    
    axes_hdl.legend(aprox_name)

    axes_hdl.set_ylim(bottom=0)

    if img_ext != 'none':
        plt.savefig('-'.join(aprox_name) + '-GrpDelay.'  + img_ext, format=img_ext)



def pzmap(myFilter, filter_description='none',fig_id='none', axes_hdl='none'):
    """Plot the complex s-plane given zeros and poles.
    Pamams:
     - b: array_like. Numerator polynomial coefficients.
     - a: array_like. Denominator polynomial coefficients.
    
    http://www.ehu.eus/Procesadodesenales/tema6/102.html
    
    """
    

    if fig_id == 'none':
        fig_hdl = plt.figure()
        fig_id = fig_hdl.number
    else:
        if plt.fignum_exists(fig_id):
            fig_hdl = plt.figure(fig_id)
        else:
            fig_hdl = plt.figure()
            fig_id = fig_hdl.number

    axes_hdl = plt.gca()
    
        # Get the poles and zeros
    z, p, k = tf2zpk(myFilter.num, myFilter.den)


    # Add unit circle and zero axes    
    unit_circle = patches.Circle((0,0), radius=1, fill=False,
                                 color='black', ls='solid', alpha=0.1)
    axes_hdl.add_patch(unit_circle)
    plt.axvline(0, color='0.7')
    plt.axhline(0, color='0.7')

    
    #Add circle lines
    
  #        maxRadius = np.abs(10*np.sqrt(p[0]))
    all_radius = np.unique(np.concatenate((np.abs(z), np.abs(p), [1])))
   
    for circleRadius in all_radius:

        circle = patches.Circle((0,0), radius=circleRadius, fill=False,
                                 color='black', ls= (0, (1, 5)), alpha=0.2)
        axes_hdl.add_patch(circle)
        plt.axvline(0, color='0.7')
        plt.axhline(0, color='0.7')
    
    
    # Plot the poles and set marker properties
    poles = plt.plot(p.real, p.imag, 'x', markersize=9, alpha=0.5, 
                     label=filter_description)
    
#    if filter_description != 'none':
#        poles[0].label = filter_description
    
    # Plot the zeros and set marker properties
    zeros = plt.plot(z.real, z.imag,  'o', markersize=9, 
             color='none', alpha=0.5,
             markeredgecolor=poles[0].get_color(), # same color as poles
             markerfacecolor='white'
             )

    
    # Scale axes to fit
    rx = 1.1 * np.amax(np.concatenate((abs(z), abs(p), [1])))
    
    
    auxPMax = p.imag.max() if len(p.imag) > 0 else 0
    auxZMax = z.imag.max() if len(z.imag) > 0 else 0
    
    ry = 1.1* np.amax([auxPMax, auxZMax])
    ry = 1 if ry == 0 else ry
        
    plt.axis([-rx, rx, -ry, ry])
    #plt.axis('scaled')
    #plt.axis([-r, r, -r, r])
#    ticks = [-1, -.5, .5, 1]
#    plt.xticks(ticks)
#    plt.yticks(ticks)

    """
    If there are multiple poles or zeros at the same point, put a 
    superscript next to them.
    TODO: can this be made to self-update when zoomed?
    """
    # Finding duplicates by same pixel coordinates (hacky for now):
    poles_xy = axes_hdl.transData.transform(np.vstack(poles[0].get_data()).T)
    zeros_xy = axes_hdl.transData.transform(np.vstack(zeros[0].get_data()).T)    

    # dict keys should be ints for matching, but coords should be floats for 
    # keeping location of text accurate while zooming

    

    d = defaultdict(int)
    coords = defaultdict(tuple)
    for xy in poles_xy:
        key = tuple(np.rint(xy).astype('int'))
        d[key] += 1
        coords[key] = xy
    for key, value in d.items():
        if value > 1:
            x, y = axes_hdl.transData.inverted().transform(coords[key])
            plt.text(x, y, 
                        r' ${}^{' + str(value) + '}$',
                        fontsize=13,
                        )

    d = defaultdict(int)
    coords = defaultdict(tuple)
    for xy in zeros_xy:
        key = tuple(np.rint(xy).astype('int'))
        d[key] += 1
        coords[key] = xy
    for key, value in d.items():
        if value > 1:
            x, y = axes_hdl.transData.inverted().transform(coords[key])
            plt.text(x, y, 
                        r' ${}^{' + str(value) + '}$',
                        fontsize=13,
                        )

    

    plt.xlabel(r'$\sigma$')
    plt.ylabel('j'+r'$\omega$')

    plt.grid(True, color='0.9', linestyle='-', which='both', axis='both')

    fig_hdl.suptitle('Poles and Zeros map')
   
    return fig_id, axes_hdl
    

def grpDelay(myFilter, fig_id='none', w=None, n=100):

    w,_,phase = myFilter.bode(w, n)

    phaseRad = phase * np.pi / 180.0
    groupDelay = -np.diff(phaseRad)/np.diff(w)

    if fig_id == 'none':
        fig_hdl = plt.figure()
        fig_id = fig_hdl.number
    else:
        if plt.fignum_exists(fig_id):
            fig_hdl = plt.figure(fig_id)
        else:
            fig_hdl = plt.figure()
            fig_id = fig_hdl.number

    plt.semilogx(w[1::], groupDelay)    # Bode phase plot
    plt.grid(True)
    plt.xlabel('Angular frequency [rad/sec]')
    plt.ylabel('Group Delay [sec]')
    plt.title('Group delay')

    axes_hdl = plt.gca()

    return fig_id, axes_hdl

def bodePlot(myFilter, aprox_name, fig_id='none', axes_hdl='none', w=None, 
             n=100, printW=-1):
    
    w, mag, phase = myFilter.bode(w, n)
    
    if printW>=0:
        aux = 0
        for i in range(len(w)):
            if abs(w[i]-printW) <= abs(w[aux]-printW):
                aux = i
        s = mag[aux]
        s2 = w[aux]
        print(f"*El valor obtenido en el Bode en w={s2:.3f}" + " para un " + 
              aprox_name + f" es: {s:.3f}dB\n")
        

    if fig_id == 'none':
        fig_hdl, axes_hdl = plt.subplots(2, 1, sharex='col')
        fig_id = fig_hdl.number
    else:
        if plt.fignum_exists(fig_id):
            fig_hdl = plt.figure(fig_id)
            axes_hdl = fig_hdl.get_axes()
        else:
            fig_hdl, axes_hdl = plt.subplots(2, 1, sharex='col')
            fig_id = fig_hdl.number

    (mag_ax_hdl, phase_ax_hdl) = axes_hdl
    
    plt.sca(mag_ax_hdl)
    plt.semilogx(w, mag)    # Bode magnitude plot
    plt.grid(True)
    plt.xlabel('Angular frequency [rad/sec]')
    plt.ylabel('Magnitude response [dB]')
    plt.title('Frequency response')
    
    plt.sca(phase_ax_hdl)
    plt.semilogx(w, phase)    # Bode phase plot
    plt.grid(True)
    plt.xlabel('Angular frequency [rad/sec]')
    plt.ylabel('Phase response [deg]')
    plt.title('Frequency response')
    
    return fig_id, axes_hdl
    
def convert2SOS(myFilter):
    
    SOSarray = tf2sos(myFilter.num, myFilter.den)
    
    SOSnumber,_ = SOSarray.shape
    
    SOSoutput = np.empty(shape=(SOSnumber,3))
    
    for index in range(SOSnumber):
        SOSoutput[index][:] = SOSarray[index][3::]
        
        if SOSoutput[index][2]==0:
            SOSoutput[index] = np.roll(SOSoutput[index],1)
        
    return SOSoutput