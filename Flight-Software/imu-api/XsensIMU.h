#ifndef I2C_H_
#define I2C_H_
#include <cstdint>
#include<string>
using std::string;
#define I2C_BUS "/dev/i2c-2"

namespace tomcat {

struct message {
    float threeAxisData[6];
    float temperature;
    uint16_t hour;
	uint16_t min;
	uint16_t sec;
	uint32_t nano;
};

class XsensIMU{
private:
	unsigned int bus;
	unsigned int device;
	int file;
	int write(unsigned char value);
	unsigned char* read (unsigned int number);
	int open();
	
public:
	 XsensIMU(unsigned int bus, unsigned int device);
	 float * getMotionData( unsigned char* measurements);
	 float  getTemperature( unsigned char* measurements);
	 message  getTime( unsigned char* measurements);
	 unsigned char* readRegisters(unsigned int number, unsigned int fromAddress=0);
	 string DRDYread();
	 void close();
	 ~XsensIMU();
};

} 
#endif