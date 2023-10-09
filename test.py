import aioble
import asyncio
import machine
from machine import I2C
import network
import time
import rp2
import json
from umqtt.simple import MQTTClient
import secrets
import mqtt_async

LIGHT_SENSOR_I2C_ADDRESS = 0x23
LIGHT_SENSOR_PULSE_THRESHOLD = 40
WIFI_SSID = secrets.WIFI_SSID
WIFI_PASSWORD = secrets.WIFI_PASSWORD
MQTT_HOST = secrets.MQTT_HOST
MQTT_STATE_TOPIC = 'homeassistant/sensor/picopower/state'
MQTT_CONFIG_TOPIC = 'homeassistant/sensor/picopower/config'
MQTT_CLIENT_ID = 'picopower'


# _IRQ_SCAN_RESULT = 5


# def bt_irq(event, data):
#     if event == _IRQ_SCAN_RESULT:
#         addr_type, addr, connectable, rssi, adv_data = data
#         address = binascii.hexlify(addr).decode()
#         print(address, binascii.hexlify(adv_data))
#         # devices[address] = rssi

async def yyy():
    device = aioble.Device(0, '')  # 0 => ADDR_PUBLIC
    connection = await device.connect()

    async with connection:
        pass
        # try:
        #     temp_service = await connection.service(_ENV_SENSE_UUID)
        #     temp_characteristic = await temp_service.characteristic(_ENV_SENSE_TEMP_UUID)
        # except asyncio.TimeoutError:
        #     print("Timeout discovering services/characteristics")
        #     return

        # while True:
        #     temp_deg_c = _decode_temperature(await temp_characteristic.read())
        #     print("Temperature: {:.2f}".format(temp_deg_c))
        #     await asyncio.sleep_ms(1000)


async def xxx():
    async with aioble.scan(0) as scanner:
        async for result in scanner:
            print(result, result.name(), result.rssi, list(result.services()))

    print("hi")

# if __name__ == "__main__":
#     ble = bluetooth.BLE()
#     ble.active('active')
#     ble.irq(bt_irq)
#     ble.gaqqp_scan(2000, 100)
#     time.sleep(2)
#     # ble.active('active')
#     # with ble.gap_scan(30000, 50000, 50000) as scanner:
#     #     for adv in scanner:
#     #         print(adv)

async def main():
    config = mqtt_async.config.copy()
    config['ssid'] = WIFI_SSID
    config['wifi_pw'] = WIFI_PASSWORD
    config['server'] = MQTT_HOST

    # Connect to WiFi
    print("Connecting to WIFI")
    rp2.country('GB')
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(WIFI_SSID, WIFI_PASSWORD)
    while not wlan.isconnected():
        print(wlan.status())
        print('Waiting for connection...')
        time.sleep(1)
    print("Connected to WiFi")

    await asyncio.gather(xxx(), yyy())

asyncio.run(main())
print("HING")
