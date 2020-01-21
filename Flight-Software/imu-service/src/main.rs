use kubos_service::Config;
use std::thread;
use std::time::Duration;

// Get the configuration options for the service out of the `config.toml` file
let config = Config::new("my-payload-service").unwrap();

// Get the watchdog timeout value
let timeout = config
    .get("watchdog-timeout")
    .and_then(|val| val.as_integer())
    .expect("Unable to get timeout value");

// Start a thread which will kick the watchdog at the given interval
thread::spawn(move || loop {
    kick_watchdog();
    thread::sleep(Duration::from_secs(timeout as u64));
});

// Get the I2C information
let device = config.get("device").unwrap();
let bus = device["bus"].as_str().expect("Unable to get I2C bus");
let addr = device["addr"].as_integer().expect("Unable to get I2C address");

// Set up the bus connection
let i2c = rust_i2c::Connection::from_path(&bus, addr as u16);

// Send a command to the device
let command = rust_i2c::Command {
    cmd: 0x70,
    data: vec![],
};
i2c.write(command);
