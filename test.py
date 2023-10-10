import aioble
import asyncio
import cfgsecrets
import mqtt_async
import binascii


FAN_MAC = '58:2b:db:00:2e:68'
FAN_PIN = '09135336'
FAN_MAX_RPM = 2400

SENSOR_MAC = 'A4:C1:38:AA:AF:F3'

MQTT_STATE_TOPIC = 'homeassistant/sensor/picopower/state'
MQTT_CONFIG_TOPIC = 'homeassistant/sensor/picopower/config'
MQTT_CLIENT_ID = 'picoshower'


# _IRQ_SCAN_RESULT = 5


# def bt_irq(event, data):
#     if event == _IRQ_SCAN_RESULT:
#         addr_type, addr, connectable, rssi, adv_data = data
#         address = binascii.hexlify(addr).decode()
#         print(address, binascii.hexlify(adv_data))
#         # devices[address] = rssi

async def fan():
    while True:
        try:
            print("MOOOO")
            device = aioble.Device(0, FAN_MAC)  # 0 => ADDR_PUBLIC
            connection = await device.connect(0)
            async with connection:
                print("FAN")
        except Exception as ex:
            print("FANFAIL")
            print(type(ex))
            print(ex)
            await asyncio.sleep(5)

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


async def sensor():
    while True:
        try:
            print("SCANNER")
            async with aioble.scan(0) as scanner:
                async for result in scanner:
                    print("HEY", binascii.hexlify(result.device.addr, ':'))
                    if result.device.addr == SENSOR_MAC:
                        print("SENSOR", result, result.name(), result.rssi, list(result.services()))
            await asyncio.sleep(1)
        except Exception as ex:
            print("SENSORFAIL")
            print(ex)
            await asyncio.sleep(5)


def msg_callback(topic, msg, retained, qos):
    pass


async def conn_callback(client):
    pass
    # await client.subscribe(TOPIC, 1)


async def mqtt():
    mqtt_async.config['ssid'] = cfgsecrets.WIFI_SSID
    mqtt_async.config['wifi_pw'] = cfgsecrets.WIFI_PASSWORD
    mqtt_async.config['server'] = cfgsecrets.MQTT_HOST
    mqtt_async.config['subs_cb'] = msg_callback
    mqtt_async.config['connect_coro'] = conn_callback

    mqc = mqtt_async.MQTTClient(mqtt_async.config)
    await mqc.connect()
    while True:
        print("HELLO")
        # print('publish', n)
        # await client.publish(TOPIC, 'Hello World #{}!'.format(n), qos=1)
        await asyncio.sleep(5)
    # await mqc.subscribe(topic, qos)


# if __name__ == "__main__":
#     ble = bluetooth.BLE()
#     ble.active('active')
#     ble.irq(bt_irq)
#     ble.gaqqp_scan(2000, 100)
#     time.sleep(2)
#     # ble.active('active')
#     # with ble.gap_scan(30000, 50000, 50000) as scanner:
#     #     for adv in scanner:cd de
#     #         print(adv)

async def main():

    # # Connect to WiFi
    # print("Connecting to WIFI")
    # rp2.country('GB')
    # wlan = network.WLAN(network.STA_IF)
    # wlan.active(True)
    # wlan.connect(WIFI_SSID, WIFI_PASSWORD)
    # while not wlan.isconnected():
    #     print(wlan.status())
    #     print('Waiting for connection...')
    #     time.sleep(1)
    # print("Connected to WiFi")

    await asyncio.gather(
        # fan(),mlknm;,
                         sensor(),
                        #  mqtt()
                         )

asyncio.run(main())
print("HING")
