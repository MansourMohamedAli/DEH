from pymodbus.client.tcp import AsyncModbusTcpClient
from pymodbus.exceptions import ModbusIOException
import asyncio
import logging

"""Logging Setup"""
logging.basicConfig()
_logger = logging.getLogger(__file__)
_logger.setLevel("DEBUG")

"""Setup Defaults"""
default_ip = '127.0.0.1'

default_port = 502

def setup_async_client(ip: str = default_ip, port: int = default_port):
    return AsyncModbusTcpClient(ip, port=port, id=1)


async def run_async_client(client, modbus_calls=None):
    """Run sync client."""
    # _logger.info("### Client starting")
    # await client.connect()
    # print(client.connected)
    if client.connected is True:
        # _logger.info("### Client starting read")
        if modbus_calls:
            return await modbus_calls(client)
    else:
        _logger.info("### Attempting to connect...")
        await client.connect()
        # client.close()
        # _logger.info("### End of Program")
        if client.connected is True:
            _logger.info("### program successfully connected")
            return 0
        return -1

async def read_coil(c):
    """Test connection works."""
    try:
        rr = await c.read_coils(0, 7, slave=1)
        # print(rr.bits)
        # assert len(rr.bits) == 8
    except ModbusIOException:
        client.close()
        _logger.info("### End of Program")
        return 0
    else:
        """If try is successful"""
        return rr.bits


async def read_input_register(c):
    """Test connection works."""
    try:
        print("Reading...")
        rr = await c.read_input_registers(0, 100, slave=1)
        print(rr.registers[0:100])
        print("Done Reading")
    except ModbusIOException as e:
        _logger.error(e)
        return 0
    else:
        """If try is successful"""
        return rr.registers[0]


async def read_holding_register(c):
    """Test connection works."""
    try:
        # print("Reading...")
        rr = await c.read_holding_registers(0, 1, slave=1)
        # print(rr.registers[0:1])
        # print("Done Reading")
    except ModbusIOException as e:
        _logger.error(e)
        return 0
    else:
        """If try is successful"""
        return rr.registers[0]


async def write_regs(c):
    """Test connection works."""
    try:
        print("Starting Write...")
        await c.write_registers(0, 80, slave=1)
    except ModbusIOException as e:
        _logger.error(e)
        return 0
    else:
        """If try is successful"""
        pass


async def read_from_server(setup_client=setup_async_client(), call=None):
    """Combine setup and run."""
    # return await run_async_client(setup_client, modbus_calls=call)
    return await run_async_client(setup_client, modbus_calls=call)


"""Assigning function object to operation and passing entire function
This will give flexibility when wanting to do a different type of operation
such as write from client"""
client = setup_async_client('127.0.0.1', 502)
operation = write_regs

if __name__ == "__main__":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(read_from_server(client, operation), debug=True)  # pragma: no cover
    # asyncio.run(read_from_server(), debug=True)  # pragma: no cover
