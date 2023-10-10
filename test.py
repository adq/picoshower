import aioble
import asyncio
import cfgsecrets
import mqtt_async
import binascii
import bluetooth
import struct



FAN_MAC = '58:2b:db:00:2e:68'.lower()
FAN_PIN = '09135336'
FAN_MAX_RPM = 2400

SENSOR_MAC = 'A4:C1:38:AA:AF:F3'.lower()

MQTT_STATE_TOPIC = 'homeassistant/sensor/picopower/state'
MQTT_CONFIG_TOPIC = 'homeassistant/sensor/picopower/config'
MQTT_CLIENT_ID = 'picoshower'

SERVICE_FAN_STATUS = bluetooth.UUID("e6834e4b-7b3a-48e6-91e4-f1d005f564d3")
CHARACTERISTIC_PIN_CODE = bluetooth.UUID("4cad343a-209a-40b7-b911-4d9b3df569b2")
CHARACTERISTIC_PIN_CONFIRMATION = bluetooth.UUID("d1ae6b70-ee12-4f6d-b166-d2063dcaffe1")
CHARACTERISTIC_FAN_DESCRIPTION = bluetooth.UUID("b85fa07a-9382-4838-871c-81d045dcc2ff")
CHARACTERISTIC_SENSOR_DATA = bluetooth.UUID("528b80e8-c47a-4c0a-bdf1-916a7748f412")
CHARACTERISTIC_STATUS = bluetooth.UUID("25a824ad-3021-4de9-9f2f-60cf8d17bded")

SERVICE_FAN_SETTINGS = bluetooth.UUID("c119e858-0531-4681-9674-5a11f0e53bb4")
CHARACTERISTIC_AUTOMATIC_CYCLES = bluetooth.UUID("f508408a-508b-41c6-aa57-61d1fd0d5c39")
CHARACTERISTIC_BASIC_VENTILATION = bluetooth.UUID("faa49e09-a79c-4725-b197-bdc57c67dc32")
CHARACTERISTIC_BOOST = bluetooth.UUID("118c949c-28c8-4139-b0b3-36657fd055a9")
CHARACTERISTIC_CLOCK = bluetooth.UUID("6dec478e-ae0b-4186-9d82-13dda03c0682")
CHARACTERISTIC_FACTORY_SETTINGS_CHANGED = bluetooth.UUID("63b04af9-24c0-4e5d-a69c-94eb9c5707b4")
CHARACTERISTIC_LED = bluetooth.UUID("8b850c04-dc18-44d2-9501-7662d65ba36e")
CHARACTERISTIC_LEVEL_OF_FAN_SPEED = bluetooth.UUID("1488a757-35bc-4ec8-9a6b-9ecf1502778e")
CHARACTERISTIC_MODE = bluetooth.UUID("90cabcd1-bcda-4167-85d8-16dcd8ab6a6b")
CHARACTERISTIC_NIGHT_MODE = bluetooth.UUID("b5836b55-57bd-433e-8480-46e4993c5ac0")
CHARACTERISTIC_RESET = bluetooth.UUID("ff5f7c4f-2606-4c69-b360-15aaea58ad5f")
CHARACTERISTIC_SENSITIVITY = bluetooth.UUID("e782e131-6ce1-4191-a8db-f4304d7610f1")
CHARACTERISTIC_TEMP_HEAT_DISTRIBUTOR = bluetooth.UUID("a22eae12-dba8-49f3-9c69-1721dcff1d96")
CHARACTERISTIC_TIME_FUNCTIONS = bluetooth.UUID("49c616de-02b1-4b67-b237-90f66793a6f2")


async def fan():
    while True:
        try:
            print("MOOOO")
            device = aioble.Device(0, FAN_MAC)  # 0 => ADDR_PUBLIC
            connection = await device.connect(0)
            async with connection:
                fan_status_service = await connection.service(SERVICE_FAN_STATUS)
                fan_settings_service = await connection.service(SERVICE_FAN_SETTINGS)
                
                fan_status_service_pin = await fan_status_service.characteristic(CHARACTERISTIC_PIN_CODE)
                await fan_status_service_pin.write(struct.pack("<I", int(FAN_PIN)))

                for service in connection.services():
                    print(service)
                while True:
                    print("FANCONNECTED")

                    await asyncio.sleep(1)
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
