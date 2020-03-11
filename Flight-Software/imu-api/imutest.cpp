/*
* ASEN 4028 Senior Projects -- TOMCAT
* Script for interfacing with an Xsens MTI-3 IMU.
* Requires XsensIMU.h/cpp to work
* Author: Srikanth Venkataraman
*
*/

#include <iostream>
#include <fstream>
#include "XsensIMU.h"
#include <unistd.h>
#include <pthread.h>
#include <cstdint>
#include <cstring>
#include<string>
#include <sys/socket.h>
#include <arpa/inet.h>

using namespace std;
using namespace tomcat;
#define PORT 5007

int main() {

	ofstream dataLog;
	//!!!!CHANGE BEFORE FLIGHT!!!!
	// dataLog.open("telem.txt",ios::app);
	dataLog.open("telem.txt");
	//Initialize new IMU object
	XsensIMU imu(2,0x6b);

	int sock = 0;
    struct sockaddr_in serv_addr;

    if ((sock = socket(AF_INET, SOCK_DGRAM, 0)) < 0)
    {
        cout<<"Socket creation error \n";
        return -1;
    }

    serv_addr.sin_family = AF_INET;
    serv_addr.sin_port = htons(PORT);

    if(inet_pton(AF_INET, "127.0.0.1", &serv_addr.sin_addr)<=0)
    {
        cout<<"binary conversion failed \n";
        return -1;
    }

    if (connect(sock, (struct sockaddr *)&serv_addr, sizeof(serv_addr)) < 0)
    {
        cout<<"connection failed \n";
        return -1;
    }


	//Buffer to store data from I2C bus
	int k = 0;
	while(k<1){
		string drdy = imu.DRDYread();
		string one = "1"; //I hate cstrings
		if(drdy == one){
			unsigned char* status_buffer ;
			//Get the status of the notification and measurement pipes
			status_buffer = imu.readRegisters((uint8_t)4,0x04);

			//Extract size of message waiting in each pipe
			uint16_t notificationSize;
			uint16_t measurementSize;

			notificationSize = (uint16_t)status_buffer[0] | ((uint16_t)status_buffer[1]<<8);
			measurementSize = (uint16_t)status_buffer[2] | ((uint16_t)status_buffer[3]<<8);
			// cout<<"Notification size: "<<hex<<notificationSize<<"\n";
			// cout<<"Measurement size: "<<hex<<measurementSize<<"\n";

			//Buffer to store measurements
			uint8_t* measurements;
			uint8_t* notifications;


			//Read from mmeasurement pipe
			if(notificationSize>0){
				notifications = imu.readRegisters(notificationSize,0x05);
			}
			if(measurementSize>0){
				measurements = imu.readRegisters(measurementSize,0x06);


				//Print for debugging
				// for(int i = 0; i < measurementSize; ++i){
				// 		cout<<i<<": "<<hex<<(int)(measurements[i])<<"\n";
				// 	}

				//Extract acceleration and rotation data
				float *motionData;
				motionData = imu.getMotionData(measurements);
				message toSend = imu.getTime(measurements);

				float temperature = imu.getTemperature(measurements);

				toSend.temperature = temperature;
				for(int i = 0; i<6;i++){
				toSend.threeAxisData[i] = motionData[i];
			}

				// cout<<"Time: "<<hour<<":"<<min<<":"<<sec<<"."<<nanoTime<<"\n";
				// cout<<"Acc x: "<<motionData[0]<<" m/s^2"<<"\n";
				// cout<<"Acc y: "<<motionData[1]<<" m/s^2"<<"\n";
				// cout<<"Acc z: "<<motionData[2]<<" m/s^2"<<"\n";
				// cout<<"Rot x: "<<motionData[3]<<" m/s"<<"\n";
				// cout<<"Rot y: "<<motionData[4]<<" m/s"<<"\n";
				// cout<<"Rot z: "<<motionData[5]<<" m/s"<<"\n";
				// cout<<"Temperature: "<<temperature<<" degrees C\n";
				//write to file
				dataLog << toSend.hour<<","<< toSend.min<<","<< toSend.sec<<","<<toSend.nano<<","<< motionData[0]<<","<< motionData[1]<<","<< motionData[2]<<","<< motionData[3]<<","<< motionData[4]<<","<< motionData[5]<<","<<temperature<<"\n";
				send(sock , &toSend , sizeof(struct message) , 0 );
				delete motionData;
				delete measurements;
				k++;
			}

		 delete status_buffer;

		}
}

	return 0;
}
