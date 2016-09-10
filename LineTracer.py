#!/usr/bin/python

import RPi.GPIO as GPIO
import time
import sys
import os

import signal
 
def signal_handler( signal, frame ):
	print 'You pressed CTRL+C'
	time.sleep( 1.0 )
	end()
	sys.exit( 0 )

signal.signal( signal.SIGINT, signal_handler )



class Motor:
	""" Motor class """
	def __init__(self, port1, port2, Hz ):
		self._port1 = port1
		self._port2 = port2
		self._pwm1 = self.__initMotorPWM(port1, Hz)
		self._pwm2 = self.__initMotorPWM(port2, Hz)

		self.__ready(self._pwm1, port1, Hz)
		self.__ready(self._pwm2, port2, Hz)

	def __initMotorPWM(self, port, Hz):
		GPIO.setup( port, GPIO.OUT )
		GPIO.output( port, False )
		pwm = GPIO.PWM( port, Hz )

		return pwm

	def __ready(self, pwm, port, Hz):
		time.sleep(.5)
		pwm.start(100)
		pwm.ChangeFrequency(Hz)
		pwm.ChangeDutyCycle(0)
		GPIO.output( port, True )

	def ccw(self, duty):
		self._pwm1.ChangeDutyCycle(duty)
		self._pwm2.ChangeDutyCycle(0)
		
	def cw(self, duty):
		self._pwm1.ChangeDutyCycle(0)
		self._pwm2.ChangeDutyCycle(duty)
		
	def brake(self):
		self._pwm1.ChangeDutyCycle(100)
		self._pwm2.ChangeDutyCycle(100)
		
	def coast(self):
		self._pwm1.ChangeDutyCycle(0)
		self._pwm2.ChangeDutyCycle(0)


IRLM393_1A_05 = 5   #gpio_port 5
IRLM393_1A_06 = 6   #gpio_port 6
IRLM393_1A_13 = 13	#gpio_port 13

MOTOR_BIN_1 = 17
MOTOR_BIN_2 = 18
MOTOR_AIN_1 = 22
MOTOR_AIN_2 = 23
FREQ=800

def init():
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(IRLM393_1A_05, GPIO.IN)
	GPIO.setup(IRLM393_1A_06, GPIO.IN)
	GPIO.setup(IRLM393_1A_13, GPIO.IN)

	motor1 = Motor( MOTOR_AIN_1, MOTOR_AIN_2, FREQ )
	motor2 = Motor( MOTOR_BIN_1, MOTOR_BIN_2, FREQ )

	return (motor1, motor2)

       
def end():
	GPIO.cleanup()
 
def readSensor():
	s1 = GPIO.input(IRLM393_1A_05)
	s2 = GPIO.input(IRLM393_1A_06)
	s3 = GPIO.input(IRLM393_1A_13)

	return (s1, s2, s3)

def run():
	motors = init()

	try:
		while True:

			status = readSensor()
			print status

			if status[0]==1 and status[1]==0:
				motors[0].ccw( 99 )	
			elif status[0]==1 and status[1]==1:
				motors[0].cw( 99 )	
			elif status[0]==0:
				motors[0].brake()

			if status[2]==1 and status[1]==0:
				motors[1].ccw( 99 )	
			elif status[2]==1 and status[1]==1:
				motors[1].cw( 99 )	
			elif status[2]==0:
				motors[1].brake()

			time.sleep(1.0)

	except KeyboardInterrupt:
		end()
	
if __name__=='__main__':        # if script
    run()

