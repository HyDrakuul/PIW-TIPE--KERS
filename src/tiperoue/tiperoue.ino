/*
Created on Wed Feb  7 15:31:12 2024

@author: gyanlouisin

TIPE project: Arduino sketch for measuring flywheel rotation speed.

This sketch reads two sensor coils (or hall-effect sensors) to detect the
passage of a magnet and computes rotational speed in tours/second.
The value is printed over Serial and displayed on an LCD.

Skills demonstrated:
 - embedded system data acquisition with interrupts
 - basic signal debouncing and timing with micros()
 - serial communication with Python scripts for logging/plotting

How to adapt for your setup:
 - Update `pinBobineVitesse` and `pinBobineDetection` to match your wiring.
 - Adjust the scaling factor in the speed calculation if your flywheel geometry
   changes (currently uses a fixed circumference factor 74.96).
 - Ensure the Arduino is connected to the host and the correct serial port is
   used in the Python scripts.
*/

#include <LiquidCrystal.h>
//definition de pi
#define PI 3.1415926535897932384626433832795
//initialisation des ports 
const int pinBobineVitesse=A0;
const int pinBobineDetection=A1;
//paramétrage de l'écran
LiquidCrystal lcd(7, 8, 9, 10, 11, 12);
// definition des variables de debut et de fin de tour
volatile unsigned long debut =0;
volatile unsigned long fin=0;
//defintion d'une variable drapeau
volatile bool flag=false;
void setup() { 
  // inilitialisation de l'écran
  lcd.begin(16, 2);
  lcd.print("V. de Rotation:");
  //Ports de bobine en INPUT
  pinMode(pinBobineVitesse,INPUT);
  pinMode(pinBobineDetection,INPUT);
  //defintion d'un port quelconque qui servira de condition de sortie de la boucle 
  pinMode(2,OUTPUT);
  Serial.begin(9600);
  //definition d'une interruption logique (on active la fonction detectionAimant): on interrompt la boucle si le port 2 passe d'un niveau LOW à HIGH 
  attachInterrupt(digitalPinToInterrupt(2),detectionAimant,RISING); 
  Serial.println("Ready"); 
  }

void loop() {
  // si une tension est detectée par la première bobine, on sort de la boucle pour entrer dans la fonction detection aimant (passage de LOW à HIGH)
  if (analogRead(pinBobineVitesse) != 0){
    digitalWrite(2,HIGH);
  }
//si le drapeau est levé, on considère que l'aimant a fait un tour (il est dejà passé une fois)
 if (flag==true){  
  fin=micros();
  //calcul de la vitesse à l'aide des variables mises à jour
  float vitesse=(2*PI*74.96)/((fin-debut)*pow(10,-3));
  // impression des données dans le buffer
  Serial.print(vitesse);Serial.print(" tours/s ; ");Serial.print(fin*pow(10,-6));Serial.println(" secondes");
  // mise à jour de l'écran
  lcd.setCursor(2, 1);
  lcd.print(vitesse);
  lcd.setCursor(7, 1);
  lcd.print("tours/s");
  // on baisse le drapeau et on réinitialise les variables à la fin du tour
  flag=false;
  fin=0;
  debut=0;

     
  }
  
 }
 
void detectionAimant(){
  // si l'aimant n'est pas déjà passé devant la bobine avant detection, on demarre le compteur 
  if (debut == 0){
    debut=micros();
    //tant que l'aimant ne passe pas devant la 2nde bobine, on attend afin d'éviter les erreurs de mesures 
     while (analogRead(pinBobineDetection)==0){
      delayMicroseconds(1);
      }
      //le drapeau reste baissé car l'aimant commence son tour
    flag=false;
  }
  // si l'aimant passe pour la 2nde fois, on lève le drapeau, ce qui permet de continuer la boucle principale
  else{

    flag=true;
  }
  digitalWrite(2,LOW);
}
