#define NUM_KEYS 5
#define DEBUG_LED_PIN 13
#define BAUD_RATE 9600

const int adc_key_val[NUM_KEYS] = {620, 670, 730, 810, 920};
int adc_key_in;
int key = -1;
int oldkey = -1;

void setup()
{
       pinMode(DEBUG_LED_PIN, OUTPUT); // we'll use the debug LED to output a heartbeat
       Serial.begin(BAUD_RATE);        // 9600 bps
}

void loop()
{
       adc_key_in = analogRead(0); // read the value from the sensor
       digitalWrite(DEBUG_LED_PIN, LOW);
       key = get_key(adc_key_in); // convert into key press

       if (key != oldkey) // if keypress is detected
       {
              delay(50);                  // wait for debounce time
              adc_key_in = analogRead(0); // read the value from the sensor
              key = get_key(adc_key_in);  // convert into key press
              if (key != oldkey)
              {
                     oldkey = key;
                     if (key >= 0)
                     {
                            digitalWrite(DEBUG_LED_PIN, HIGH);
                            switch (key)
                            {
                            case 0:
                                   Serial.println("1");
                                   break;
                            case 1:
                                   Serial.println("2");
                                   break;
                            case 2:
                                   Serial.println("3");
                                   break;
                            case 3:
                                   Serial.println("4");
                                   break;
                            case 4:
                                   Serial.println("5");
                                   break;
                            }
                     }
              }
       }
       delay(100);
}
// Convert ADC value to key number
int get_key(unsigned int input)
{
       int k;
       for (k = 0; k < NUM_KEYS; k++)
       {
              if (input < adc_key_val[k])
              {
                     return k;
              }
       }
       if (k >= NUM_KEYS)
              k = -1; // No valid key pressed
       return k;
}
