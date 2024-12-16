import asyncio
from read_device import ReadDevice


async def main_pac3200() -> None:
    try:
        serial_settings = "COM2"
        function = 4
        address = 1
        quantity = 8
        slave_id = 1
        baudrate = 9600
        bytesize = 8
        parity = "E"
        stopbits = 1
        pac3200 = ReadDevice(
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

        read_registers = await pac3200.run_async_simple_client()
        floats = [
            ReadDevice.decode_registers_to_floats(
                [read_registers[i], read_registers[i + 1]]
            )
            for i in range(0, len(read_registers), 2)
        ]

        print(f"Active_Power: {floats[1]}")

    except Exception as e:
        print(f"Exception in main: {e}")


async def main_huawei_inverter() -> None:
    try:
        serial_settings = "COM4"
        function = 4
        address = 30000
        quantity = 4
        slave_id = 3
        baudrate = 9600
        bytesize = 8
        parity = "E"
        stopbits = 1
        huawei_inverter = ReadDevice(
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

        read_registers = await huawei_inverter.run_async_simple_client()
        floats = [
            ReadDevice.decode_registers_to_floats(
                [read_registers[i], read_registers[i + 1]]
            )
            for i in range(0, len(read_registers), 2)
        ]

        print(f"Generation_Accum: {floats[0]}")

    except Exception as e:
        print(f"Exception in main: {e}")


async def main():

    await asyncio.gather(main_huawei_inverter(), main_pac3200())


if __name__ == "__main__":
    asyncio.run(main())
