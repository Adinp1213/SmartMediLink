import math
import time
import datetime
from luma.core.interface.serial import i2c, spi, pcf8574
from luma.core.interface.parallel import bitbang_6800
from luma.core.render import canvas
from luma.oled.device import ssd1306, ssd1309, ssd1325, ssd1331, sh1106, sh1107, ws0010

# getting data from app
import boto3

s3 = boto3.client('s3',
                  aws_access_key_id='put access key id',
                  aws_secret_access_key=' put secret access key',
                  region_name='region')

bucket_name = 'smartpills'
object_key = 'userdetails/userdetails.txt'

local_file_path = '/home/rpi/test_code/s3bucket_text.txt'


with open(local_file_path, 'r') as f:
    file_contents = f.read()

print(file_contents)


GPIO.setmode(GPIO.BOARD)
GPIO.setup(10, GPIO.IN)
GPIO.setup(11, GPIO.OUT)
serial = i2c(port=1, address=0x3c)
device = sh1106(serial)




def main():
    today_last_time = "Unknown"
    flag = 0
    while True:
        s3.download_file(bucket_name, object_key, local_file_path)
        with open(local_file_path, 'r') as f:
            file_contents = f.read()
        PatientName, set_time, no_of_dosages, PillId = file_contents.split(',')
        set_hour, set_minute = set_time.split(':')
        set_hour = int(set_hour)
        set_minute = int(set_minute)
        no_of_dosages = int(no_of_dosages)
        current_time = datetime.datetime.now()
        print(current_time)
        time.sleep(0.5)
        if current_time.hour == set_hour and current_time.minute == set_minute:
            if GPIO.input(10) == False:
                if (flag == 0):
                    for x in range(no_of_dosages):
                        with open("servotest.py") as f:
                            exec(f.read())
                    flag = 1
            elif flag == 0 and GPIO.input(10) == True:
                with canvas(device) as draw:
                    draw.rectangle(device.bounding_box, outline="white", fill="black")
                    draw.text((10, 40), "Take pill", fill="white")
                    GPIO.output(11, GPIO.HIGH)
                time.sleep(0.2)

        if current_time.minute == set_minute + 1:
            flag = 0

        if GPIO.input(10) == True:
            with canvas(device) as draw:
                draw.rectangle(device.bounding_box, outline="white", fill="black")
                draw.text((10, 40), "No Dispenser ", fill="white")
                GPIO.output(11, GPIO.LOW)
            time.sleep(0.2)
        else:
            with canvas(device) as draw:
                now = datetime.datetime.now()
                today_date = now.strftime("%d %b %y")
                today_time = now.strftime("%H:%M:%S")
                if today_time != today_last_time:
                    today_last_time = today_time
                    draw.rectangle(device.bounding_box, outline="white", fill="black")
                    draw.text((10, 40), today_date + ' ' + today_time, fill="white")
            time.sleep(1)
            GPIO.output(11, GPIO.LOW)


if name == "main":
    try:
        # device = get_device()
        main()
    except KeyboardInterrupt:
        pass
