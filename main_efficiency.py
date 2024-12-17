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
    decode_floats=True,
):
    """
    Reads Modbus registers from a specific device and decodes them.
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

        if decode_floats:
            values = [
                ReadDevice.decode_registers_to_floats([registers[i], registers[i + 1]])
                for i in range(0, len(registers), 2)
            ]
        else:
            values = registers  # Directly use raw registers if no decoding is needed

        print(f"{label}: {values[float_index]}")

    except (ConnectionError, asyncio.TimeoutError) as e:
        print(f"Error reading {label}: {e}")
    except Exception as e:
        print(f"Unexpected error reading {label}: {e}")


async def join_process() -> None:
    """
    Executes three asynchronous functions in parallel, checking every second.

    This function gathers tasks for reading and decoding registers from multiple devices
    and processes them asynchronously.
    """
    while True:
        # Define tasks to run asynchronously
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
            # Connection to monitoring station
            show_information_register(
                serial_port="COM6",
                function=4,
                address=40035,
                quantity=4,
                slave_id=2,
                baudrate=9600,
                bytesize=8,
                parity="E",
                stopbits=1,
                label="Irradiance",
                float_index=0,
                decode_floats=False,  # Example where decoding is not needed
            ),
        )

        # Execute all tasks concurrently

        # Print a dot to indicate that tasks are running every second
        for _ in range(4):
            print(".")
            await asyncio.sleep(1)

        # Wait for 1 second before re-running
        await asyncio.sleep(1)


async def main():
    """
    Main function to execute tasks repeatedly in an asynchronous loop.
    """
    await join_process()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nPrograma terminado por el usuario.")
