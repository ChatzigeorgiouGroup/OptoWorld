

/*
 OptoWorld Microcrontroller code

 This code does the following: 
 
 It connects to an MQTT server then:
  - Measures Temperature with a ds18b20 onewire thermometer
  - Measures light intensity in lux using a bh1750 module
  - Publishes the values to MQTT topic optoworld/status
  - subscribes to the topic "optoworld/switch". 
    Callback on incoming messages for this topic sets the neopixels to the intensity value specified
    in the message.
 The code will attempt reconnecting to the server if the connection is lost using a blocking
 reconnect function. 

 Replace the placeholders for ssid, password and broker ip with your real values.

*/

#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include <FastLED.h>
#include <DallasTemperature.h>
#include <OneWire.h>
#include <BH1750.h>

BH1750 lightSensor;


//number of leds we are running
#define NUM_LEDS 300
#define DATA_PIN D6

// Define the array of leds
CRGB leds[NUM_LEDS];

//setup the thermometer
#define ONE_WIRE_BUS D5 
OneWire oneWire(ONE_WIRE_BUS);
DallasTemperature sensors(&oneWire);

// variables
const int reportLed = D4;
int blue_val;

// Update these with values suitable for your network.

const char* ssid = "<my_ssid";
const char* password = "<my_password>";
const char* mqtt_server = "<my_mqtt_broker_ip";

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
 blue_val = atoi((char *)payload);
 switch_light(blue_val);

}

void reconnect() {
  // Loop until we're reconnected
  while (!client.connected()) {
    digitalWrite(BUILTIN_LED, 1);
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
      digitalWrite(BUILTIN_LED, 0);
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      // Wait 5 seconds before retrying
      delay(5000);
    }
  }
}


void switch_light(int blue_val){
  fill_solid(leds, NUM_LEDS, CRGB(0,0,blue_val));
  FastLED.show();
  
}

float get_temperature() {
  sensors.requestTemperatures();
  float temp1 = sensors.getTempCByIndex(0);
  
  return temp1;
}

void setup() {
  pinMode(BUILTIN_LED, OUTPUT);     // Initialize the BUILTIN_LED pin as an output
  digitalWrite(BUILTIN_LED, 1);

  Wire.begin(D2, D1);
  lightSensor.begin();
  
  Serial.begin(115200);
  setup_wifi();
  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);

    //initialize the lights
    FastLED.addLeds<NEOPIXEL, DATA_PIN>(leds, NUM_LEDS);  // GRB ordering is assumed
  //inititalize the thermometers

  
}

void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();
  
  long now = millis();
  if (now - lastMsg > 1000) {
    lastMsg = now;
    ++value;
    float temp = get_temperature();
    float lux = lightSensor.readLightLevel();
//    client.publish("optoworld/light_level", String(lux).c_str());
//    client.publish("optoworld/temperature", String(temp).c_str());
//    client.publish("optoworld/blue_val", String(blue_val).c_str());
    String message = String(temp)+"_"+String(blue_val)+"_"+String(lux);
    client.publish("optoworld/status", message.c_str());
  }
}
