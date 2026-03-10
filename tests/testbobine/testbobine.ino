/*
  Test sketch for validating hand-made sensor coils (bobines).

  This sketch reads an analog input (A0) and prints the voltage to Serial.
  Use the Arduino Serial Plotter to observe the signal in real time.

  Validation method:
  - When the magnet passes in front of the coil, the voltage should spike.
  - A clear peak in the Serial Plotter indicates the coil is responding.
*/

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  Serial.println("Ready");
}

void loop() {
  
  int val2=analogRead(A0);
  
  float tension2=val2*(float)5/1024;
  // put your main code here, to run repeatedly:
  Serial.print("Tension 1:"); Serial.println(tension2); 
  delay(1);

}
