import pymodbus.client, pymodbus.framer, pymodbus.exceptions, pymodbus.pdu
import struct
from decimal import Decimal, ROUND_DOWN


class ReadDevice:

    def __init__(
        self,
        serial_settings: str,
        function: int,
        address: int,
        quantity: int,
        slave_id: int,
        baudrate: int,
        bytesize: int,
        parity: str,
        stopbits: int,
    ) -> None:
        self._serial_settings = serial_settings
        self._function = function
        self._address = address
        self._quantity = quantity
        self._slave_id = slave_id
        self._baudrate = baudrate
        self._bytesize = bytesize
        self._parity = parity
        self._stopbits = stopbits

    async def __start_connection(
        self, framer=pymodbus.framer.ModbusRtuFramer
    ) -> pymodbus.client:
        try:
            client = pymodbus.client.AsyncModbusSerialClient(
                port=self._serial_settings,
                framer=framer,
                timeout=1,
                retries=3,
                baudrate=self._baudrate,
                bytesize=self._bytesize,
                parity=self._parity,
                stopbits=self._stopbits,
            )
            await client.connect()

            if client.connected:
                return client
            else:
                print("Failed to connect to the Modbus server")
                return None
        except Exception as e:
            print(f"Exception in start_connection: {e}")
            return None

    async def run_async_simple_client(self) -> list:

        client = await self.__start_connection()
        if client is None:
            return


        try:
            if self._function == 3:
                rr = await client.read_holding_registers(
                    address=self._address, count=self._quantity, slave=self._slave_id
                )
            else:
                rr = await client.read_input_registers(
                    address=self._address, count=self._quantity, slave=self._slave_id
                )
            if rr.isError():
                print(f"Exception reading registers: {rr}")
                return None
            if isinstance(rr, pymodbus.pdu.ExceptionResponse):
                print(f"Exception in instance of Modbus library: {rr}")
                return None
            return rr.registers if rr else None

        except pymodbus.exceptions.ModbusException as e:
            print(f"Modbus library exception: {e}")
            return None
        finally:
            self.__close_connection(client=client)

    def __close_connection(self, client: pymodbus.client) -> None:
        try:
            if client is not None:
                client.close()
        except Exception as e:
            print(f"Exception in close_connection: {e}")

    @staticmethod
    def decode_registers_to_floats(registers) -> float:

        # The two 16-bit registers are joined together to form a 32-bit value
        # and the order of the registers is reversed.
        combined = (registers[0] << 16) + registers[1]

        # The 32-bit value is converted to a float using struct
        value_float = struct.unpack("!f", struct.pack("!I", combined))[0]
        # number rounded
        float_rounded = Decimal(value_float).quantize(
            Decimal("0.001"), rounding=ROUND_DOWN
        )
        return float_rounded


# It is a good practice to include getters and setters
# to ensure controlled access to the attributes of a class. However,
# since in this case the attributes will not be accessed or modified during
# the execution of the application,
# I have decided to comment them out.

# # Getters
# @property
# def serial_settings(self):
#     return self._serial_settings

# @property
# def function(self):
#     return self._function

# @property
# def address(self):
#     return self._address

# @property
# def quantity(self):
#     return self._quantity

# @property
# def slave_id(self):
#     return self._slave_id

# @property
# def baudrate(self):
#     return self._baudrate

# @property
# def bytesize(self):
#     return self._bytesize

# @property
# def parity(self):
#     return self._parity

# @property
# def stopbits(self):
#     return self._stopbits

# # Setters
# @serial_settings.setter
# def serial_settings(self, value):
#     self._serial_settings = value

# @function.setter
# def function(self, value):
#     self._function = value

# @address.setter
# def address(self, value):
#     self._address = value

# @quantity.setter
# def quantity(self, value):
#     self._quantity = value

# @slave_id.setter
# def slave_id(self, value):
#     self._slave_id = value

# @baudrate.setter
# def baudrate(self, value):
#     self._baudrate = value

# @bytesize.setter
# def bytesize(self, value):
#     self._bytesize = value

# @parity.setter
# def parity(self, value):
#     self._parity = value

# @stopbits.setter
# def stopbits(self, value):
#     self._stopbits = value
