import sys  # sys нужен для передачи argv в QApplication
from PyQt5 import QtWidgets
from PyQt5.QtCore import QThread, QObject, pyqtSlot, pyqtSignal, QTimer 
import design  # Это наш конвертированный файл дизайна
from random import choice, randint
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import paho.mqtt.subscribe as subscribe
import json
from DHE import DH_Endpoint
import time


class myThread(QThread):
    signal1 = pyqtSignal(str)
    signal2 = pyqtSignal(str)
    def __init__(self):
        pass





class ExampleApp(QtWidgets.QMainWindow, design.Ui_MainWindow):
    
    def __init__(self):
        super().__init__()
        self.setupUi(self)                                              
        self.pushButton.clicked.connect(self.send_message)
        self.pushButton_2.clicked.connect(self.subscribe_topic)
        self.pushButton_3.clicked.connect(self.generate_pub_key)
        self.pushButton_4.clicked.connect(self.generate_pvt_key)
        self.pushButton_5.clicked.connect(self.generate_topic)
        self.pushButton_6.clicked.connect(self.key_exchange)
        
        self.public_key1 = None
        self.public_key2 = None
        self.private_key = None
        self.partial_key = None
        self.partial_key_r = None


        self.topic = None
        self.message_to_send = ''
        self.message = None
        self.decoded_message = None

        self.broker = 'broker.hivemq.com'
        self.port = 1883
        self.client_id = f'python-mqtt-{randint(0, 1000)}'

        self.client = mqtt.Client(self.client_id)
        self.client.on_message = self.on_message
        self.client.on_subscribe = self.on_subscribe

        self.connect_mqtt()


        self.timer = QTimer()
        self.timer.stop()
        self.timer.setInterval(20)
        self.timer.start() 
        self.timer.timeout.connect(self.update)
        
        self.DHE = None
    def update(self):
        if self.message:
            self.textBrowser_2.append(self.message)
            self.message = None
        if self.decoded_message:
            self.textBrowser.append(self.decoded_message)
            self.decoded_message = None


    def on_subscribe(self,client, userdata, mid, granted_qos):
        print(client, userdata, mid, granted_qos)

    def connect_mqtt(self):
        try:
            self.client.connect_async(self.broker, self.port)
        except Exception as e:
            print('1333', e)
        self.client.loop_start()
    
    def on_message(self,client,userdata,msg):
        try:
            topic = msg.topic
            payload = str(msg.payload.decode())
            self.message = payload
            if ('key1: ' in payload) and (not self.public_key1):
                self.public_key1 = int(payload.split()[1])
                self.key_exchange()
            elif ('key2: ' in payload) and (not self.public_key2):
                self.public_key2 = int(payload.split()[1])
                self.key_exchange()
            elif ('partial key1: ' in payload) and (not self.partial_key):
                self.partial_key_r = int(payload.split()[2])
                self.private_key = int(self.lineEdit_3.text())    
                self.DHE = DH_Endpoint(self.public_key1,self.public_key2, self.private_key)
                self.partial_key = self.DHE.generate_partial_key()
                self.client.publish(self.topic, f'partial key2: {self.partial_key}')  
                self.DHE.generate_full_key(self.partial_key_r)
            elif ('partial key2: ' in payload) and (not self.partial_key_r):
                self.partial_key_r = int(payload.split()[2])
                self.DHE.generate_full_key(self.partial_key_r)
            elif self.DHE and self.DHE.full_key:
                dcd = self.DHE.decrypt_message(payload)
                self.decoded_message = dcd
        except Exception as e:
            print('123',e)
   #============= 
    
    def isPrime(self, k):
        if k==2 or k==3: return True
        if k%2==0 or k<2: return False
        for i in range(3, int(k**0.5)+1, 2):
            if k%i==0:
                return False
        return True


    def generate_topic(self):
        topic = '/example/of/topic'
        topic += f'/{randint(0,10000)}'
        self.lineEdit_4.setText(topic)


    def generate_pub_key(self):
        primes = [i for i in range(1,100000) if self.isPrime(i)]
        
        key = str(choice(primes))

        self.lineEdit_2.setText(key)

        
    def generate_pvt_key(self):
        primes = [i for i in range(1,100000) if self.isPrime(i)]
        
        key = str(choice(primes))

        self.lineEdit_3.setText(key)


    def subscribe_topic(self):
        self.topic = self.lineEdit_4.text()
        self.client.subscribe(self.topic,qos=0) 
        


    def key_exchange(self):



        if not self.public_key1:
            self.public_key1 = int(self.lineEdit_2.text())
            self.client.publish(self.topic, f'key1: {self.public_key1}')
            return
        elif not self.public_key2: 
            self.public_key2 = int(self.lineEdit_2.text())
            self.client.publish(self.topic, f'key2: {self.public_key2}')
            return

        elif not self.partial_key:
            self.private_key = int(self.lineEdit_3.text())    
            self.DHE = DH_Endpoint(self.public_key1,self.public_key2, self.private_key)
            self.partial_key = self.DHE.generate_partial_key()
            self.client.publish(self.topic, f'partial key1: {self.partial_key}')           
            return

 

        

    def send_message(self):
        try:
            txt = self.textEdit.toPlainText()
            self.message_to_send = self.DHE.encrypt_message(txt)
            self.client.publish(self.topic,self.message_to_send)
        except Exception as e:
            print(e)



def main():
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = ExampleApp()  # Создаём объект класса ExampleApp
    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение

if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    try:
        main()
    except Exception as e:
        print('222', e)
