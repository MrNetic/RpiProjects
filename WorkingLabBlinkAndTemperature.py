#!/usr/bin/env python
import RPi.GPIO as GPIO
import time,math

LedPin = 12    # pin11
a_pin = 18
b_pin = 16

def setup():
	GPIO.setmode(GPIO.BOARD)       # Numbers GPIOs by physical location
	GPIO.setup(LedPin, GPIO.OUT)   # Set LedPin's mode is output
	GPIO.output(LedPin, GPIO.LOW) # Set LedPin high(+3.3V) to off led
	


# Try to keep this value near 1 but adjust it until
# the temperature readings match a known thermometer
adjustment_value = 0.01
# Create a function to take an analog reading of the
# time taken to charge a capacitor after first discharging it
# Perform the procedure 100 times and take an average
# in order to minimize errors and then convert this
# reading to a resistance
def resistance_reading():
    total = 0
    for i in range(1, 100):
        # Discharge the 330nf capacitor
        GPIO.setup(a_pin, GPIO.IN)
        GPIO.setup(b_pin, GPIO.OUT)
        GPIO.output(b_pin, False)
        time.sleep(0.01)
        # Charge the capacitor until our GPIO pin
        # reads HIGH or approximately 1.65 volts
        GPIO.setup(b_pin, GPIO.IN)
        GPIO.setup(a_pin, GPIO.OUT)
        GPIO.output(a_pin, True)
        t1 = time.time()
        while not GPIO.input(b_pin):
            pass
        t2 = time.time()
        # Record the time taken and add to our total for
        # an eventual average calculation
        total = total + (t2 - t1) * 1000000
    # Average our time readings
    reading = total / 100
    # Convert our average time reading to a resistance
    resistance = reading * 6.05 - 939
    return resistance

# Create a function to convert a resistance reading from our
# thermistor to a temperature in Celsius which we convert to
# Fahrenheit and return to our main loop
def temperature_reading(R):
    B = 3977.0 # Thermistor constant from thermistor datasheet
    R0 = 10000.0 # Resistance of the thermistor being used
    t0 = 273.15 # 0 deg C in K
    t25 = t0 + 25.0 # 25 deg C in K
    # Steinhart-Hart equation
    inv_T = 1/t25 + 1/B * math.log(R/R0)
    T = (1/inv_T - t0) * adjustment_value
    return T * 9.0 / 5.0 + 32.0 # Convert C to F
 

def loop():
	while True:
		#just have in celciues
        	t = temperature_reading(resistance_reading())
 		
		#t=resistance_reading()
        	# Print temperature values in real time
        	print(t)

		print "...led on"
		GPIO.output(LedPin, GPIO.LOW)  # led on
		time.sleep(0.5)
		print "led off..."
		GPIO.output(LedPin, GPIO.HIGH) # led off
		print "A Lili e a maior"
		time.sleep(0.5)
		

def destroy():
	GPIO.output(LedPin, GPIO.HIGH)     # led off
	GPIO.cleanup()                     # Release resource

if __name__ == '__main__':     # Program start from here
	setup()
	try:
		loop()
	except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
		destroy()
