/*
 Basic ESP8266 MQTT example

 This sketch demonstrates the capabilities of the pubsub library in combination
 with the ESP8266 board/library.

 It connects to an MQTT server then:
  - publishes "hello world" to the topic "outTopic" every two seconds
  - subscribes to the topic "inTopic", printing out any messages
    it receives. NB - it assumes the received payloads are strings not binary
  - If the first character of the topic "inTopic" is an 1, switch ON the ESP Led,
    else switch it off

 It will reconnect to the server if the connection is lost using a blocking
 reconnect function. See the 'mqtt_reconnect_nonblocking' example for how to
 achieve the same result without blocking the main loop.

 To install the ESP8266 board, (using Arduino 1.6.4+):
  - Add the following 3rd party board manager under "File -> Preferences -> Additional Boards Manager URLs":
       http://arduino.esp8266.com/stable/package_esp8266com_index.json
  - Open the "Tools -> Board -> Board Manager" and click install for the ESP8266"
  - Select your ESP8266 in "Tools -> Board"

*/

#include <ESP8266WiFi.h>
#include <PubSubClient.h>
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


// Update these with values suitable for your network.

const char* ssid = "DanielsNetwork";
const char* password = "DwodBsngl#29teRknor";
const char* mqtt_server = "192.168.1.9";

WiFiClient espClient;
PubSubClient client(espClient);
long lastMsg = 0;
char msg[50];
int value = 0;

void setup_wifi() {

  delay(10);
  // We start by connecting to a WiFi network
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  randomSeed(micros());

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}

void callback(char* topic, byte* payload, unsigned int length) {
 payload[length] = '\0';
 int blue_val = atoi((char *)payload);
 switch_light(blue_val);

}

void reconnect() {
  // Loop until we're reconnected
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    // Create a random client ID
    String clientId = "ESP8266Client-";
    clientId += String(random(0xffff), HEX);
    // Attempt to connect
    if (client.connect(clientId.c_str())) {
      Serial.println("connected");
      // Once connected, publish an announcement...
      client.publish("outTopic", "hello world");
      // ... and resubscribe
      client.subscribe("optoworld/switch");
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      // Wait 5 seconds before retrying
      delay(5000);
    }
  }
}

float get_temperature() {
  sensors.requestTemperatures();
  float temp1 = sensors.getTempCByIndex(0);
  
  return temp1;
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

void switch_light(int blue_val){
  fill_solid(leds, NUM_LEDS, CRGB(0,0,blue_val));
  FastLED.show();
  
}

void setup() {
  pinMode(BUILTIN_LED, OUTPUT);     // Initialize the BUILTIN_LED pin as an output
  Serial.begin(115200);
  setup_wifi();
  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);

    //initialize the lights
    FastLED.addLeds<NEOPIXEL, DATA_PIN>(leds, NUM_LEDS);  // GRB ordering is assumed
  //inititalize the thermometers
    sensors.begin();
  //initialize the pins
    pinMode(buttonPin, INPUT);
  
}

void loop() {
  check_button();

  if (!client.connected()) {
    reconnect();
  }
  client.loop();

  long now = millis();
  if (now - lastMsg > 5000) {
    lastMsg = now;
    ++value;
    float temp = get_temperature();
    client.publish("optoworld/temperature", String(temp).c_str());
  }
}
