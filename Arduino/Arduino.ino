#include <Servo.h>
#include <math.h>

#define TILT 6
#define PAN 5
#define MOTOR 2
#define LED_RED 3
#define LED_GREEN 4
#define BTN_PLUS 10
#define BTN_MOINS 11
#define BTN 12

#define TILT_START 85
#define PAN_START 90

Servo pan_servo;
Servo tilt_servo;

short state = 0;
int tilt = TILT_START;
int pan = PAN_START;

void setup()
{
	// Attach pin to servo
  pan_servo.attach(PAN);
	tilt_servo.attach(TILT);
	
	// Set start position
  pan_servo.write(PAN_START);    
  tilt_servo.write(TILT_START);
	
	// Set pin Mode for motor and 
  pinMode(MOTOR, OUTPUT);
	pinMode(LED_GREEN, OUTPUT);
  pinMode(LED_RED, OUTPUT);

  pinMode(BTN_PLUS, INPUT_PULLUP);
  pinMode(BTN_MOINS, INPUT_PULLUP);
  pinMode(BTN, INPUT_PULLUP);
  
  start_serial(9600);

  digitalWrite(LED_RED, HIGH);
  delay(100);
  digitalWrite(LED_RED, LOW);
  delay(100);
  digitalWrite(LED_RED, HIGH);
  delay(100);
  digitalWrite(LED_RED, LOW);
  delay(100);
  digitalWrite(LED_RED, HIGH);
  delay(100);
  digitalWrite(LED_RED, LOW);
  delay(100);

  
}

int offset_y = 0;
int offset_z = 0;
float XYZ[] = {0, 0,0};
String command;
int index, previous;

String readline() {
  // Renvoie la ligne (finit par \n) dispo sur la liaison s�rie
  String data = "";
  char c = ' ';
  while (c != '\n'){
    if (Serial.available() > 0) {
      c = Serial.read();
      data += c;
    }
  }
  return data;
}

void start_serial(long baudrate) {
  // Initialisation de la liaison s�rie
  Serial.begin(baudrate);
  String data;

  // Proc�dure de connexion : Re�oit SYN, repond ACK et c'est bon.
  while (data != String("SYN\r\n")) {
    data = readline();
    if (data != String("SYN\r\n")) {
      Serial.println("NACK"); // Si message re�u bizarre, r�pond NACK
    }
  }
  Serial.println("ACK");
}

void loop()
{
  switch(state){
    case 0:
      // Init des actionneurs
      digitalWrite(LED_RED, LOW);
      digitalWrite(LED_GREEN, LOW);
      digitalWrite(MOTOR, LOW);
      
      pan_servo.write(pan);
      tilt_servo.write(tilt);

      state = 1;
      break;

    case 1:
      // Réglage Delta x et Delta z
      digitalWrite(LED_RED, HIGH);
      // Placer la mire au centre de la camera et le laser juste en dessous de la mire
      // Distance : 1mm

      // Puis modifier tilt pour placer le laser sur la mire 
      if (digitalRead(BTN_PLUS) == LOW){
        tilt = tilt + 10;
      }
      else if (digitalRead(BTN_MOINS) == LOW){
        tilt = tilt - 10;
      }
      else if (digitalRead(BTN) == LOW){
        state = 2;
      }
      tilt_servo.write(tilt);
      delay(200); // Bounce Filter
      break;
      
    case 2:
      // Réglage Delta y
      digitalWrite(LED_RED, LOW);
      digitalWrite(LED_GREEN, HIGH);

      // Placer la mire à 50cm du centre, sur l'axe central horizontal

      // Puis modifier PAN pour placer le laser sur la mire
      if (digitalRead(BTN_PLUS) == LOW){
        pan = pan + 10;
      }
      else if (digitalRead(BTN_MOINS) == LOW){
        pan = pan - 10;
      }
      else if (digitalRead(BTN) == LOW){
        state = 3;
      }
      pan_servo.write(pan);
      delay(200); // Bounce Filter
      break;

    case 3:
      // Calcul des offset
      offset_z = 50 / tan((float) pan*3.1415/180) - 100; // Unit : cm
      offset_y = (100 + offset_z) * tan((float) tilt*3.1415/180);
      state = 4;
      digitalWrite(LED_GREEN, LOW);
      break;

    case 4:
      // Attente de consigne
      command = readline(); //"X,Y,Z\r\n" avec une précision de 10^-2
      index = 0;
      previous = 0;
      for (int i=0; i<command.length(); i++){
        if (command[i] == ',' || command[i] == '\r') {
          XYZ[index] = command.substring(previous, i).toFloat();
          index++;
          previous = i + 1;
        }
      }
      state = 5;
      break;
      
    case 5:
      // Applique la consigne
      float x = XYZ[0];
      float y = XYZ[1] + offset_y;
      float z = XYZ[2] + offset_z;
      
      pan = PAN_START + atan(x/z);
      tilt = TILT_START + atan(y/sqrt(x*x+z*z));
      Serial.print(tilt);
      Serial.print(",");
      Serial.println(pan);
      tilt_servo.write(tilt);
      pan_servo.write(pan);
      state = 4;
  }
}
