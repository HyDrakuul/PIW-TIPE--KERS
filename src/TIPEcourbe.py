#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  7 15:31:12 2024

@author: gyanlouisin

TIPE project: Minimal serial acquisition and plotting helper.

This script provides a simple acquisition loop that reads angular velocity
and timestamp data from an Arduino and plots the resulting curve.

Skills demonstrated:
 - polling serial devices with `select`
 - basic data cleaning and plotting
 - building small reusable functions for acquisition/processing

How to adapt for your setup:
 - Change the serial port in `ser = serial.Serial(...)` to match your system.
 - Replace the internal list handling with file-based input/output if you
   want to store curves persistently.
"""
import select
import serial
import matplotlib.pyplot as plt
import tkinter as tk 

vitesse=[]
temps=[]

ser=serial.Serial('/dev/cu.usbmodem101')

def acquisition():
    tempsmax=5
    while True:
        lecture,_,_=select.select([ser],[],[],tempsmax)
        
        if lecture==[]:
            break
        else:
            Data=ser.readline().strip().split()
     
            
            if Data[0]== b'Ready' :
                continue
        
            else:  
                vitesse.append(float(Data[0].decode()))
                temps.append(float(Data[3].decode()))
    print(temps,vitesse)
            
    return [temps, vitesse]
        
def traitement(table):
    table[1].pop(0)
    table[0].pop(0)
    tempsref=table[0][0]
    for i in range(len(table[0])):
        table[0][i]=table[0][i]-tempsref
        
    return [table[0],table[1]]

def courbe(table):
    x=traitement(table)[0]
    y=traitement(table)[1]
    plt.plot(x,y,"ob")
    plt.xlabel("temps en s")
    plt.ylabel("vitesse de rotation en m/s")
    plt.title("Vitesse de Rotation du volant en m/s en fonction du temps")
    return plt.show()
    

    
    
    

    
        
    
    

