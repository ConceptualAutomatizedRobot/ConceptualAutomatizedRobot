#!/usr/bin/env python
#coding: utf-8
import motor as m
import car_dir as cd
import time

class Motor:
    def __init__(self):
        m.setup() #Have to be done
    ############################################
    # Permet de stoper le vehicule
    ############################################
    def stop(self):
        m.ctrl(0)
    ############################################
    # Change la vitesse du moteur
    # speed : la vitesse
    ############################################
    def set_speed(self, speed):
        m.setSpeed(speed)
    ############################################
    # Permet d'avancer
    # speed_percent : le pourcentage de vitesse
    # sec : Temps en sec à avancer la voiture
    ############################################
    def forward(self, speed_percent, sec=0):
        #ctrl(stasus(1 : on,0 : off), direction (1 : devant de base,-1 : derriere))
        m.ctrl(1) 
        m.setSpeed(speed_percent)
        time.sleep(sec)
        if sec != 0:
            m.ctrl(0)
    ############################################
    # Permet de reculer
    # speed_percent : le pourcentage de vitesse
    # sec : Temps en sec à avancer la voiture
    ############################################
    def backward(self, speed_percent, sec=0):
        m.ctrl(1,-1)
        m.setSpeed(speed_percent)
        time.sleep(sec)
        if sec != 0:
            m.ctrl(0)
    ############################################
    # Permet de mettre les roues droite
    ############################################
    def straigth_wheel(self):
        cd.setup()
        cd.home()
    ############################################
    # Permet de tourner a gauche
    ############################################
    def left(self):
        cd.turn_left()
    ############################################
    # Permet de tourner a droite
    ############################################
    def right(self):
        cd.turn_right()
    ############################################
    # Test les directions des roues
    ############################################
    def test_rigth_left(self):
        self.straigth_wheel()
        time.sleep(2)
        self.right()
        time.sleep(2)
        self.left()
        time.sleep(2)
        self.straigth_wheel()
    ############################################
    # Test l'avance et le recul du vehicule
    ############################################
    def test_forward_backward(self):
        self.forward(50,2)
        self.backward(50,2)
    ############################################
    # Test l'avance et le recul du vehicule
    ############################################
    def test_circuit(self):
        self.forward(50)
        self.rigt()
        time.sleep(2)
        self.straigth_wheel()
        time.sleep(2)
        self.stop()
def main():
    motor = Motor()
    #motor.test_rigth_left()
    #motor.test_forward_backward()
    motor.test_circuit()

if __name__ == '__main__':
    main()