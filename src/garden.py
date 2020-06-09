from miflora.miflora_poller import MiFloraPoller
from btlewrap.gatttool import GatttoolBackend
import time
from datetime import datetime

poller = MiFloraPoller('80:EA:CA:89:28:33', GatttoolBackend)

start_round = time.time()

now_utc = datetime.utcnow()
now = datetime.now()

# poller.battery_level() #  – gibt den Batteristatus zurück.
# poller.firmware_version() # – liefert die aktuelle Firmware Version als Text.
sensor = {
    'mac': '80:EA:CA:89:28:33', 
    'temperature': None, 
    'light': None, 
    'moisture': None, 
    'conductivity': None, 
    'battery': None,
    'ts_utc': int(now.strftime("%s")), 
    'date_utc': now_utc,
    'date': now,
    'firmware': None
    }


sensor['firmware']=poller.firmware_version()
start=time.time()
# liefert den Temperaturwert (in Grad Celsius)
sensor['temperature']=poller.parameter_value("temperature")
print("temperature")
stop=time.time()
print("Diff: %f" % (stop-start))

start=time.time()
# gibt den Lichtwert zurück (umso größer – umso heller).
sensor['light']=poller.parameter_value("light")
print("light")
stop=time.time()
print("Diff: %f" % (stop-start))

start=time.time()
# gibt die Feuchtigkeit an
sensor['moisture']=poller.parameter_value("moisture")
print("moisture")
stop=time.time()
print("Diff: %f" % (stop-start))

start=time.time()
# gibt die Leitfähigkeit des Bodens an.
sensor['conductivity']=poller.parameter_value("conductivity")
print("conductivity")
stop=time.time()
print("Diff: %f" % (stop-start))

start=time.time()
# gibt den Batteristatus an.
sensor['battery']=poller.parameter_value("battery")
print("battery")
stop=time.time()
print("Diff: %f" % (stop-start))


print("Total Run Time: %f" % (start-start_round))

print(sensor)

