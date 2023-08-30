#include <wiringPi.h>
#include <stdio.h>
#include <unistd.h>

int main() {
    int buzzer_pin = 1; // GPIO pin 18 (wiringPi pin numbering)
    
    if (wiringPiSetup() == -1) {
        printf("wiringPi setup failed.\n");
        return 1;
    }
    
    pinMode(buzzer_pin, OUTPUT);
    
    digitalWrite(buzzer_pin, HIGH); // Turn on the buzzer
    usleep(500000); // Sleep for 0.5 seconds
    digitalWrite(buzzer_pin, LOW); // Turn off the buzzer
    
    return 0;
}