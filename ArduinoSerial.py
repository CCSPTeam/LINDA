import serial
import serial.serialutil
import time
from serial.tools.list_ports import comports

# pip install pyserial


class ArduinoSerial:
    """Gestion de la connexion
        - connect(port) : Lance la connexion série entre l'arduino et le programme Python en utilisant le port en paramètres
                            Pour savoir les ports de sa machine : [e.device for e in comports()]
        - send(x,y,z) : Envoie les coordonnées sur la liaison série et tire. les nombres sont des flottants"""

    def __init__(self):
        self.link = None  # Connexion série
        self.port = None  # Port de connexion COM

        self.status = "offline"  # Statut de la connexion

    def connect(self, port='COM3'):
        """Initialise la liasion entre le logiciel et le banc d'essai,
        :param : port= port COM du banc"""
        self.port = port
        if not self.link:  # Une connexion ne peut pas être établie si il est déjà connecté
            try:
                self.link = serial.Serial(port=self.port, baudrate=9600, timeout=5, writeTimeout=1)
                time.sleep(3)  # Timer pour laisser le temps à la liaison de s'établir
                self.link.write(b'SYN\r\n')
                received = self.link.readline()

                if b'ACK\r\n' in received:
                    print("Connexion Established")
                    self.status = "connected"
                elif received == b'':
                    print("Error : no response on " + port)
                    print("Use on of following : ", [e.device for e in comports()])
                    self.link = None
                else:
                    print("Error : Port return " + str(received))  # Si la liaison est occupée
                    self.link = None
            except serial.serialutil.SerialException as e:
                print("Use on of following : ", [e.device for e in comports()])
                print("Error : Access Denied")
                print(e)
                self.link = None
        else:
            print("Already connected !")

    def send(self, x,y,z):
        assert type(x) == float
        assert type(y) == float
        assert type(z) == float

        s = str(round(x,2)) + "," + str(round(y,2)) + "," + str(round(z,2)) + "\r\n"
        print(s)
        if self.link:
            self.link.write(str.encode(s))
        else:
            print("Not connected")

    def disconnect(self):
        if self.status != 'offline':
            self.link.close()
            print("Disconnected")
            self.link = None
            self.status = "offline"


if __name__ == '__main__':
    l = ArduinoSerial()
    l.connect("COM4")
    input("ready : ")
    print("send")
    l.send(40., 0., 100.)
    time.sleep(1)
    print(l.link.readline())