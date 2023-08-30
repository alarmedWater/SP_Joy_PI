#include <wiringPi.h>
#include <stdio.h>
#include <unistd.h>

int main() {
    int vibration_pin = 2; // GPIO pin 13 (wiringPi pin numbering)

    if (wiringPiSetup() == -1) {
        printf("wiringPi setup failed.\n");
        return 1;
    }

    pinMode(vibration_pin, OUTPUT);

    digitalWrite(vibration_pin, HIGH); // Turn on vibration
    sleep(1); // Sleep for 1 second
    digitalWrite(vibration_pin, LOW);  // Turn off vibration

    return 0;
}
