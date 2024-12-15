import asyncio
from read_device import ReadDevice


async def main() -> None:
    try:
        serial_settings = "COM2"
        function = 4
        address = 40035
        quantity = 4
        slave_id = 2
        baudrate = 9600
        bytesize = 8
        parity = "E"
        stopbits = 1
        modbusCliente = ReadDevice(
            serial_settings=serial_settings,
            function=function,
            address=address,
            quantity=quantity,
            slave_id=slave_id,
            baudrate=baudrate,
            bytesize=bytesize,
            parity=parity,
            stopbits=stopbits,
        )

        read_registers = await modbusCliente.run_async_simple_client()
        floats = [
            ReadDevice.decode_registers_to_floats(
                [read_registers[i], read_registers[i + 1]]
            )
            for i in range(0, len(read_registers), 2)
        ]

        print(f"Registerts: {read_registers}")
        print(f"Irradiancia: {floats[0]}")
        print(f"Temperature: {floats[1]}")
    except Exception as e:
        print(f"Exception in main: {e}")


if __name__ == "__main__":
    asyncio.run(main(), debug=False)
