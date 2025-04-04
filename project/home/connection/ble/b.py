from home.connection.ble.ble_uart_peripheral import BLEUART
import bluetooth
import time
# Ana program
def start_b():
    ble = bluetooth.BLE()
    uart = BLEUART(ble, "SaturnBLE")

    def on_rx():
        received = uart.read().decode("utf-8").strip()
        print("Alınan:", received)
        response = f"ESP32: '{received}' aldım\n"
        uart.write(response)
        print("Gönderilen:", response.strip())

    uart.irq(handler=on_rx)
    print("BLE UART Terminal Hazır. Bağlanmayı bekliyor...")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Program sonlandırılıyor...")
        uart._ble.active(False)
