from kubos_service.config import Config
import i2c
import threading

# Get the configuration options for the service out of the `config.toml` file
config = Config("imu-service")

# Get the watchdog timeout value
timeout = config.raw['watchdog-timeout']

# Start a thread which will kick the watchdog at the given interval
threading.Thread(target=watchdog_kick, args=(timeout,)).start()

# Get the I2C information
bus = config.raw['device']['bus']
addr = config.raw['device']['addr']

# Set up the bus connection (actually only needs the bus number, which is the last character)
i2c = i2c.I2C(bus[:-1])

# Send a command to the device
i2c.write(addr, [0x70])
