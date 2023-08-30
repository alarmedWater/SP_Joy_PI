/*
    compile with gcc -o light_sensor light_sensor.c -lwiringPi
    Enable BUS Communication with: sudo raspi-config -> Interfacing Options I2C on
*/

#include <wiringPi.h>
#include <stdio.h>
#include <unistd.h>
#include <stdint.h>
#include <stdlib.h>
#include <fcntl.h>
#include <sys/ioctl.h>
#include <linux/i2c-dev.h>

#define DEVICE 0x5c
#define ONE_TIME_HIGH_RES_MODE_1 0x20

int file;

void setupI2C() {
    if ((file = open("/dev/i2c-1", O_RDWR)) < 0) {
        printf("Failed to open the I2C bus\n");
        exit(1);
    }
    if (ioctl(file, I2C_SLAVE, DEVICE) < 0) {
        printf("Failed to acquire bus access and/or talk to slave\n");
        exit(1);
    }
}

uint16_t convertToNumber(uint8_t data[2]) {
    return (data[1] + (256 * data[0])) / 1.2;
}

uint16_t readLight() {
    uint8_t data[2];
    data[0] = ONE_TIME_HIGH_RES_MODE_1;
    if (write(file, data, 1) != 1) {
        printf("Error writing to I2C slave\n");
        exit(1);
    }
    usleep(200000);
    if (read(file, data, 2) != 2) {
        printf("Error reading from I2C slave\n");
        exit(1);
    }
    return convertToNumber(data);
}

int main() {
    if (wiringPiSetup() == -1) {
        printf("wiringPi setup failed.\n");
        return 1;
    }

    setupI2C();

    while (1) {
        printf("Light Level: %d lx\n", readLight());
        delay(500);
    }

    return 0;
}
