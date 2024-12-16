import asyncio
from read_device import ReadDevice


async def read_and_decode_register_floats(
    serial_port,
    function,
    address,
    quantity,
    slave_id,
    baudrate,
    bytesize,
    parity,
    stopbits,
    label,
    float_index,
):
    """
    Generic function that reads and decodes Modbus registers
    from a specific device, converting the registers into float values.
    """
    try:
        device = ReadDevice(
            serial_settings=serial_port,
            function=function,
            address=address,
            quantity=quantity,
            slave_id=slave_id,
            baudrate=baudrate,
            bytesize=bytesize,
            parity=parity,
            stopbits=stopbits,
        )

        registers = await device.run_async_simple_client()
        floats = [
            ReadDevice.decode_registers_to_floats(
                [registers[i], registers[i + 1]])
            for i in range(0, len(registers), 2)
        ]

        print(f"{label}: {floats[float_index]}")

    except Exception as e:
        print(f"Error reading {label}: {e}")


async def read_and_decode_register_integers() -> None:
    """
    Function that reads Modbus registers
    from a specific device.
    """
    try:
        serial_settings = "COM6"
        function = 4
        address = 40035
        quantity = 4
        slave_id = 2
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

        print(f"Irradiance: {floats[0]}")
    except Exception as e:
        print(f"Exception: {e}")


async def join_process() -> None:
    """
    Function to execute three asynchronous functions
    in parallel at 5-second intervals, printing one
    point every second while the functions are not executed.
    """
    while True:
        await asyncio.gather(
            read_and_decode_register_floats(
                serial_port="COM4",
                function=4,
                address=30000,
                quantity=4,
                slave_id=3,
                baudrate=9600,
                bytesize=8,
                parity="E",
                stopbits=1,
                label="Generation_Accum",
                float_index=0,
            ),
            read_and_decode_register_floats(
                serial_port="COM2",
                function=4,
                address=1,
                quantity=8,
                slave_id=1,
                baudrate=9600,
                bytesize=8,
                parity="E",
                stopbits=1,
                label="Active_Power",
                float_index=1,
            ),
            read_and_decode_register_integers(),
        )
        for _ in range(4):
            print(".")
            await asyncio.sleep(1)

        await asyncio.sleep(1)


async def main():
    """
    Function to execute tasks repeatedly
    """
    await join_process()


if __name__ == "__main__":
    # Executes the asyncio event loop
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nPrograma terminado por el usuario.")
