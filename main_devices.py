import asyncio
from read_device import ReadDevice


async def show_information_register(
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
            ReadDevice.decode_registers_to_floats([registers[i], registers[i + 1]])
            for i in range(0, len(registers), 2)
        ]

        print(f"{label}: {floats[float_index]}")

    except Exception as e:
        print(f"Error reading {label}: {e}")


async def main():
    """
    Function to execute multiple asynchronous tasks
    """
    try:
        await asyncio.gather(
            # Connection to Huawei_inverter
            show_information_register(
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
            # Connection to pac3200
            show_information_register(
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
        )
    except Exception as e:
        print(f"Exception: {e}")


if __name__ == "__main__":
    # Executes the asyncio event loop
    asyncio.run(main())
