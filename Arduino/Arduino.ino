#include <Servo.h>

#define TILT 6
#define PAN 5
#define MOTOR 3
#define LED 3

#define TILT_START 85
#define PAN_START 90

Servo pan_servo;
Servo tilt_servo;

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
	pinMode(LED, OUTPUT);

	start_serial(9600);
}


void loop()
{
  String x_str = readline();
  String y_str = readline();
  String z_str = readline();
  String offset_y_str = readline();
  String offset_z_str = readline();

  int x = x_str.substring(0, x_str.length() - 2).toInt();
  int y = y_str.substring(0, y_str.length() - 2).toInt();
  int z = z_str.substring(0, z_str.length() - 2).toInt();
  
  int offset_y = offset_y_str.substring(0, offset_y_str.length() - 2).toInt();
  int offset_z = offset_z_str.substring(0, offset_z_str.length() - 2).toInt();

  
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

String readline() {
	// Renvoie la ligne (finit par \n) dispo sur la liaison s�rie
	String data = "";
	char c = ' ';
	while (c != '\n') {
		if (Serial.available() > 0) {
			c = Serial.read();
			data += c;
		}
	}
	return data;
}
