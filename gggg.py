from machine import Pin, ADC
import time

def list_relays():
    
    number_of_relays = int(input("Number of relays: "))
    relay_name = input("Relay Name: ")
    relays = []
    
    for i in range(1 , number_of_relays + 1):
        relays.append(f"{relay_name}{i}")
        
        print(relays)
        return(relays)

def list_sensors():

    number_of_sensors = int(input("Number of sensors: "))
    sensor_name = input("Sensor Name: ")
    sensors = []

    for i in range(1, number_of_sensors + 1):
        sensors.append(f"{sensor_name}{i}")

    print(sensors)
    return sensors

def list_ADC_pins():

    ADC_pin_min = int(input("What is the min pin number?: "))
    ADC_pin_max = int(input("What is the max pin number?: "))

    ADC_pins = [i for i in range(ADC_pin_min, ADC_pin_max + 1)]

    print(ADC_pins)
    return ADC_pins

def sensor_pin_assignment(sensors, ADC_pins):

    sensor_pin = {}

    if len(sensors) > len(ADC_pins):
        
        number_pin_missing = len(sensors) - len(ADC_pins)
        print(f"{number_pin_missing} pins missing")

    elif len(sensors) < len(ADC_pins):

        print(f"Pins remaining: {len(ADC_pins) - len(sensors)} ({ADC_pins})")

        for i in range(len(sensors)):
    
            sensor_pin[sensors[i]] = ADC_pins[i]
               
        print(sensor_pin)
        return sensor_pin

def moisture_reading(sensor_pin):

    adc_objects = {}

    
    for sensor, pin_number in sensor_pin.items():
        adc = ADC(Pin(pin_number))  
        adc.atten(ADC.ATTN_11DB)
        adc.width(ADC.WIDTH_12BIT)
        adc_objects[sensor] = adc

    while True:
        raw_value = 0
        for sensor, adc in adc_objects.items():
            raw_value += adc.read()
        average_moisture = raw_value / len(sensor_pin)
        moisture_percentage = abs((average_moisture - 2750) * 100 / (1000 - 2750))
            
        yield(moisture_percentage)
        
        
def monitor_moisture(sensor_pin):
    
    moisture_high = 80
    moisture_low = 50
    relay_state = True
    
    for moisture_percentage in moisture_reading(sensor_pin):  
        if moisture_percentage < moisture_low:
            relay_state = False  
            print(f"Relay activated: {moisture_percentage:.2f}% moisture")
        
        elif moisture_percentage >= moisture_high:
            relay_state = True  
            print(f"Relay deactivated: {moisture_percentage:.2f}% moisture")
        
        else:
            state = "activated" if not relay_state else "deactivated"
            print(f"Relay remains {state}: {moisture_percentage:.2f}% moisture")
        
        time.sleep(1)  
        
relays = list_relays()        
sensors = list_sensors()
ADC_pins = list_ADC_pins()
sensor_pin = sensor_pin_assignment(sensors, ADC_pins)
monitor_moisture(sensor_pin)








