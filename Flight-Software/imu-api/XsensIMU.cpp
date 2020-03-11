/*
* ASEN 4028 Senior Projects -- TOMCAT
* I2C Read/Write functions for beaglebone black.
* Requires XsensIMU.h to work
* Author: Srikanth Venkataraman
*
*/
#include"XsensIMU.h"
#include<iostream>
#include <fstream>
#include<sstream>
#include<fcntl.h>
#include<stdio.h>
#include<iomanip>
#include<unistd.h>
#include<sys/ioctl.h>
#include<linux/i2c.h>
#include<linux/i2c-dev.h>
#include <cstdint>
#include <cstring>
#include<string>
using namespace std;




namespace tomcat {


XsensIMU::XsensIMU(unsigned int bus, unsigned int device) {
	this->file=-1;
	this->bus = bus;
	this->device = device;
	this->open();
}


int XsensIMU::open(){
   string name;
  name = I2C_BUS;

   if((this->file=::open(name.c_str(), O_RDWR)) < 0){
      perror("I2C: failed to open the bus\n");
	  return 1;
   }
   if(ioctl(this->file, I2C_SLAVE, this->device) < 0){
      perror("I2C: Failed to connect to the device\n");
	  return 1;
   }
   return 0;
}



int XsensIMU::write(unsigned char value){
   unsigned char buffer[1];
   buffer[0]=value;
   if (::write(this->file, buffer, 1)!=1){
      perror("I2C: Failed to write to the device\n");
      return 1;
   }
   return 0;
}


unsigned char* XsensIMU::read(unsigned int number){
    unsigned char* data = new unsigned char[number];
    if(::read(this->file, data, number)!=(int)number){
       perror("I2C: Failed to read in the full buffer.\n");
     return NULL;
    }
  return data;
}


unsigned char* XsensIMU::readRegisters(unsigned int number, unsigned int fromAddress){
	this->write(fromAddress);
	unsigned char* data = new unsigned char[number];
    if(::read(this->file, data, number)!=(int)number){
       perror("I2C: Failed to read in the full buffer.\n");
	   return NULL;
    }
	return data;
}

float * XsensIMU::getMotionData(unsigned char* measurements ){
  float *motionData = new float[6];
  int indexes[6] = {23,27,31,38,42,46};
  uint8_t tempMeas[4];
  for (int i = 0;i<6;i++){
    
     tempMeas[0] = measurements[indexes[i]];
     tempMeas[1] = measurements[indexes[i]-1];
     tempMeas[2] = measurements[indexes[i]-2];
     tempMeas[3] = measurements[indexes[i]-3];
     memcpy(&motionData[i],&tempMeas,4);


  }
  return motionData;
}
float  XsensIMU::getTemperature(unsigned char* measurements ){
  float temperature ;
  uint8_t tempTemp[4];
  tempTemp[0] = measurements[53];
  tempTemp[1] = measurements[52];
  tempTemp[2] = measurements[51];
  tempTemp[3] = measurements[50];
  memcpy(&temperature,&tempTemp,4);

  return temperature;
}

message  XsensIMU::getTime(unsigned char* measurements ){
  uint8_t tempNano[4];
  uint32_t nanoTime;

  tempNano[0] = measurements[8];
  tempNano[1] = measurements[7];
  tempNano[2] = measurements[6];
  tempNano[3] = measurements[5];
  memcpy(&nanoTime,&tempNano,4);

  // uint8_t tempYear[2];
  // uint16_t year;
  // tempYear[0] = measurements[10];
  // tempYear[1] = measurements[9];
  // memcpy(&year,&tempYear,2);
  //If time gets screwy, fix the bad types on these variables
  //uint16_t month = measurements[11];
  //uint16_t day = measurements[12];
  uint16_t hour = measurements[13];
  uint16_t min = measurements[14];
  uint16_t sec = measurements[15];
  message toSend;
  toSend.hour = hour;
  toSend.min = min;
  toSend.sec = sec;
  toSend.nano = nanoTime;
  return toSend;
}

string XsensIMU::DRDYread(){
   ifstream fs;
   string filepath = "/sys/class/gpio/gpio48/value";
   fs.open((filepath).c_str());
   if (!fs.is_open()){
     perror("Failed to open file. Check if pin 48 is exported ");
    }
   string input;
   getline(fs,input);
   fs.close();
   return input;
}



void XsensIMU::close(){
	::close(this->file);
	this->file = -1;
}



XsensIMU::~XsensIMU() {
	if(file!=-1) this->close();
}

}