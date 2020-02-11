#include <DallasTemperature.h>
#include <OneWire.h>
#include <FastLED.h>

//number of leds we are running
#define NUM_LEDS 300
#define DATA_PIN D1

// Define the array of leds
CRGB leds[NUM_LEDS];


//setup the thermometer
#define ONE_WIRE_BUS D2
OneWire oneWire(ONE_WIRE_BUS);
DallasTemperature sensors(&oneWire);


// Variables we need to detect and debounce button presses.
int ledState = 0;
int buttonState = 0;
int lastButtonState = 0;

unsigned long lastDebounceTime = 0;
unsigned long debounceDelay = 50;

//define some pin names
const int buttonPin = D7;
const int reportLed = D4;



void setup() { 
  //start serial
    Serial.begin(9600);
  //initialize the lights
    FastLED.addLeds<NEOPIXEL, DATA_PIN>(leds, NUM_LEDS);  // GRB ordering is assumed
  //inititalize the thermometers
    sensors.begin();
  //initialize the pins
    pinMode(buttonPin, INPUT);
    pinMode(reportLed, OUTPUT);
  //switch off the lights
    switch_light(ledState);

}

void loop() {
  check_button();

  if ( millis() % 1000 == 0 ) {
  float temp = get_temperature();
  Serial.println(temp);
  }
    
  
}

float get_temperature() {
  sensors.requestTemperatures();
  float temp = sensors.getTempCByIndex(0);
  
  return temp;
}

void check_button() { 

  //read the button pin
  int reading = digitalRead(buttonPin);

  //if the reading is different from the last button state
  //we update the lastDebounceTime
  if(reading != lastButtonState){
    lastDebounceTime = millis();
  }

  //if the reading has been changed for longer than the delay
  //we will take it as the actual new value
  if((millis() - lastDebounceTime) > debounceDelay){
    //if the reading is different from the current state, update
    if(reading != buttonState){
      buttonState  = reading;
      //if the button is actually pressed, change ledState
      if(buttonState == HIGH){
        ledState = !ledState;
        switch_light(ledState);
      }
    }
  }
  lastButtonState = reading;
}

void switch_light(bool light_status){
  if(light_status == HIGH){
    fill_solid(leds, NUM_LEDS, CRGB(0,0,255));
    FastLED.show();
    digitalWrite(reportLed, LOW);
  }
  else{
    FastLED.clear();
    FastLED.show();
    digitalWrite(reportLed, HIGH);
  }
}
