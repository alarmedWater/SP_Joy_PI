#include <wiringPi.h>
#include <stdio.h>
#include <unistd.h>

int main() {
    int button_pin = 25; // GPIO pin 26 (wiringPi pin numbering)
    int buzzer_pin = 1;  // GPIO pin 18 (wiringPi pin numbering)

    if (wiringPiSetup() == -1) {
        printf("wiringPi setup failed.\n");
        return 1;
    }

    pinMode(button_pin, INPUT);
    pullUpDnControl(button_pin, PUD_UP);
    pinMode(buzzer_pin, OUTPUT);

    while (1) {
        if (digitalRead(button_pin) == 1) {
            digitalWrite(buzzer_pin, LOW);  // Buzzer ON
        } else {
            digitalWrite(buzzer_pin, HIGH); // Buzzer OFF
        }
    }

    return 0; // This line is never reached in the infinite loop
}