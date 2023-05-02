import math
import time
import datetime
from luma.core.interface.serial import i2c, spi, pcf8574
from luma.core.interface.parallel import bitbang_6800
from luma.core.render import canvas
from luma.oled.device import ssd1306, ssd1309, ssd1325, ssd1331, sh1106, sh1107, ws0010
import RPi.GPIO as GPIO
# getting data from app
import boto3

s3 = boto3.client('s3',
                  aws_access_key_id='Aws access key',
                  aws_secret_access_key='aws secret key',
                  region_name='region')

bucket_name = 'smartpills'
object_key = 'userdetails/userdetails.txt'
local_file_path = '/home/rpi/test_code/s3bucket_text.txt'



GPIO.setmode(GPIO.BOARD)
GPIO.setup(10, GPIO.IN)
GPIO.setup(11, GPIO.OUT)
serial = i2c(port=1, address=0x3c)
device = sh1106(serial)



import math
import time
import datetime



# the format of this code is   adi,15:16,4,001
# it should be adi/15:16,15:40,15:55/4/001
# separate this in given variables below
def main():
    excluded_date = datetime.datetime.now().date()
    excluded_time= []
    today_last_time = "Unknown"
    while True:
        s3.download_file(bucket_name, object_key, local_file_path)

        with open(local_file_path, 'r') as f:
            file_contents = f.read()
        print(file_contents)
        
        file = open(local_file_path, 'r')
        current_time = datetime.datetime.now()
        print(current_time)
        if current_time.date() != excluded_date:
            excluded_time = []
            print("UPDATED DATE")
            excluded_date = current_time.date()




        lines = []
        while True:
            line = file.readline()
            if not line:
                break
            line = line[:-1] if line[-1] == '\n' else line
            lines.append(line)
        file.close()

        pill_name = lines[0][6:]
        pill_times =list(filter(lambda val: val is not None,[x if x!= '' else None for x in lines[1][6:].split(",")]))
        pill_id = lines[2][11:]
        no_of_dosages = int(lines[3][8:])


        set_times =[]
        # set_hour, set_minute = set_time.split(':')
        for t in pill_times:

            set_hour, set_minute = tuple(t.split(':'))
            set_hour = int(set_hour)
            # print(set_hour)
            set_minute = int(set_minute)
            # print(set_minute)
            # no_of_dosages = int(pill_dosage)
            settime = datetime.datetime.now().replace(hour=set_hour, minute=set_minute)
            set_times.append(settime)




        for current_set_time in set_times:
            set_h_m =[current_set_time.hour,current_set_time.minute]

            if [current_time.hour, current_time.minute] == set_h_m: # here compare if current time == any element in arr
                if [current_set_time.hour,current_set_time.minute] not in excluded_time:
                    if GPIO.input(10) == False:
                        if(pill_id == '001'):
                            for x in range(no_of_dosages):
                                with open("dispense_pill1.py") as f:
                                    exec(f.read())
                                time.sleep(0.2)

                        if(pill_id == '002'):
                            for x in range(no_of_dosages):
                                with open("dispense_pill2.py") as f:
                                    exec(f.read())
                                time.sleep(0.2)

                        if(pill_id == '003'):
                            for x in range(no_of_dosages):
                                with open("dispense_pill3.py") as f:
                                    exec(f.read())
                                time.sleep(0.2)

                        if(pill_id == '004'):
                            for x in range(no_of_dosages):
                                with open("dispense_pill4.py") as f:
                                    exec(f.read())
                                time.sleep(0.2)

                        excluded_time.append(set_h_m) # this should come in the "if IR SENSOR" block
                        print(f"pill dispensed {excluded_time}") # dont forget to delete this x_x
                    
                    else:
                        with canvas(device) as draw:
                            draw.rectangle(device.bounding_box, outline="white", fill="black")
                            draw.text((10, 40), "Take pill", fill="white")
                            GPIO.output(11, GPIO.HIGH)
                        time.sleep(0.2)
                        
            
            if GPIO.input(10) == True:
                with canvas(device) as draw:
                    draw.rectangle(device.bounding_box, outline="white", fill="black")
                    draw.text((10, 40), "No Dispenser ", fill="white")
                    GPIO.output(11, GPIO.LOW)
                #buzzer.off()
                time.sleep(0.2)
            else:
                with canvas(device) as draw:
                    now = datetime.datetime.now()
                    today_date = now.strftime("%d %b %y")
                    today_time = now.strftime("%H:%M:%S")
                    
                    if today_time != today_last_time:
                        today_last_time = today_time
                        draw.rectangle(device.bounding_box, outline="white", fill="black")
                        draw.text((10, 40), today_date+' '+today_time, fill="white")
                time.sleep(1)
                GPIO.output(11, GPIO.LOW)
                        
if __name__ == "__main__":
    try:
        # device = get_device()
        main()

    except KeyboardInterrupt:
        pass
