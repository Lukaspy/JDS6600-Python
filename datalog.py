#JDS6600 frequency counter datalogger
from jds6600 import jds6600
from time import time, strftime, sleep
import glob
import RPi.GPIO as GPIO

def write_freq_temp(freq):
    with open(output, "a") as log:
        log.write("{0},{1},{2}\n".format(strftime("%Y-%m-%d %H:%M:%S"),str(freq),read_temp()))

def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines
    
def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        return temp_f
    
def regulate_temperature():
    if int(desired_temp) < read_temp():
        GPIO.output(13, False)
    else:
        GPIO.output(13, True)

GPIO.setmode(GPIO.BOARD)
GPIO.setup(13, GPIO.OUT)
port = input("What is the tty number?: ")
output = input("type path and filename: ")
j = jds6600("/dev/tty"+port)
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'
desired_temp = input("What is the desired temperature?: ")

j.measure_setcoupling("DC")
j.measure_setgate(5)
j.measure_setmode("FREQ")

while True:
    measured = j.measure_getfreq_f()
    try:
        write_freq_temp(measured)
        regulate_temperature()
    except:
        print("temp probe disconnected")
    sleep(5)

