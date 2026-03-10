#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 22 12:34:29 2024

@author: gyanlouisin

TIPE project: Serial data acquisition from Arduino and CSV export.

This script reads angular velocity data from an Arduino over a serial port,
plots the result immediately for verification, and optionally saves the raw
series to a CSV file for further processing.

Skills demonstrated:
 - serial communication (pyserial)
 - real-time data collection and filtering
 - plotting with matplotlib
 - saving and organizing experiment data into CSV
 - simple GUI interaction with tkinter

How to adapt for your setup:
 - Update `ser = serial.Serial(...)` to match your Arduino's serial port.
 - Modify the output paths for the CSV file and the experiment counter file
   to a location you prefer (see variables near the bottom of this script).
 - For reproducible workflows, store data in relative paths within the repo.
"""


import numpy as np
import select
import serial
import matplotlib.pyplot as plt
import csv
import tkinter as tk


#définition du port de collecte des données (celui où la carte est branchée)
ser=serial.Serial('/dev/cu.usbmodem101')
#définition de deux tableaux pour stocker les données traitées  
vitesseAngulaire=np.array([])
temps=np.array([])
#définition d'un temps d'attente maximum des données
tmpsmax=5
#la boucle while permet de récuperer en continue les données
while True:
    #cette commande renvoie une liste de données à chaque itération, quand il n'y a plus de données, elle renvoie une liste vide
    lecture,_,_=select.select([ser],[],[],tmpsmax)
    #si la liste est vide, alors le flux de données c'est arreté, on peut quitter la boucle
    if lecture==[]:
        break
    #si la carte transmet des données, on les traitent avant de les stocker
    else:
        #premier traitement des données brutes, on lit les données puis on les stockent dans une liste
        Data=ser.readline().strip().split()
        #Différents cas servant à corriger certains bugs
        if Data[0]== b'Ready':
            continue
        elif Data[0]== b'ours/s':
            continue
        elif Data[1]==b't':
            break
        else:  
            #on remplit les listes au fur et à mesure des itérations
            vitesseAngulaire=np.append(vitesseAngulaire, float(Data[0].decode())/93.465)
            temps=np.append(temps, float(Data[3].decode()))
            #aprés plusieures expérience, on s'est rendu compte d'un bug pour des vitesses de rotation faibles, cette ligne permet de s'assurer une collecte de données 
            if float(Data[0].decode()) <= 0.50:
                break
            
table=[temps ,vitesseAngulaire]
print(len(table[1]),len(table[0] ))
table[1] = np.delete(table[1], 0, axis=0)  # Supprime le premier élément de vitesseAngulaire
table[0] = np.delete(table[0], 0, axis=0)  # Supprime le premier élément de temps
# défintiion d'un temps de réference pour commencer l'echeclle de temps à 0
tempsref=table[0][0]   
table=[table[0],table[1]]
#Traçé des courbes pour observer si il n'y a pas de grosses erreurs de mesure
x=table[0]
y=table[1]
print(len(x),len(y))
plt.plot(x,y,marker='+',color="blue",linestyle= "None", label="Points expérimentaux")
plt.xlabel("temps en s")
plt.ylabel("vitesse angulaire en rad/s")
plt.title("Vitesse Angulaire du volant en rad/s en fonction du temps")
plt.legend()

plt.show()
#Utilisation d'un interface graphique pour valider ou non la série de mesure prise      
root=tk.Tk()
Question=tk.messagebox.askquestion("Conservation de la Courbe", "Conserver les données ?", icon="warning")
#Si les résultats sont convenables, on les enregistres dans un fichier .csv
if Question=="yes":
    
    #Permet de numéroter les série de mesures en écrivant une variable numérique comptant le nombre d'essais
    with open("/Users/gyanlouisin/Desktop/TIPE/Experience n°.txt", 'r')as g:
              old_i= g.readlines()
              index=int(old_i[0])+1
              
    with open("/Users/gyanlouisin/Desktop/TIPE/Experience n°.txt", 'w') as g:
        for line in old_i:
            if line.strip('\n') !=str(index):
              g.write(str(index))
              

    colonnes=[index,table[0],table[1]]    
              
    with open('/Users/gyanlouisin/Desktop/TIPE/TIPE_experience2.csv', 'a', newline='') as f:
        writer=csv.writer(f)
        writer.writerow(colonnes)
        
else: 
    root.destroy()
root.mainloop()
    

    
    

    
        
    
