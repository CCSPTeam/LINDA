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
}

void start_serial(long baudrate) {
	// Initialisation de la liaison série
	Serial.begin(baudrate);
	String data;

	// Procédure de connexion : Reçoit SYN, repond ACK et c'est bon.
	while (data != String("SYN\r\n")) {
		data = readline();
		if (data != String("SYN\r\n")) {
			Serial.println("NACK"); // Si message reçu bizarre, répond NACK
		}
	}
	Serial.println("ACK");
}

String readline() {
	// Renvoie la ligne (finit par \n) dispo sur la liaison série
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