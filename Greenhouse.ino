
int sensorPin1 = 32;
int sensorPin2 = 33;
int LOW_INPUT = 3000;
int HIGH_INPUT = 1000;
int NUMBEROFSENSORS = 2;
int relayPin = 26;
int moistureThresholdLow = 50;
int moistureThresholdHigh = 80;
int greenLedPin = 15;

int calculateAverage(int pin1, int pin2) {
  int reading1 = analogRead(pin1);
  int reading2 = analogRead(pin2);
  return (reading1 + reading2) / NUMBEROFSENSORS;
}

int mapToPercentage(int value) {
  return map(value, LOW_INPUT, HIGH_INPUT, 0, 100);
}

void setup() {
  pinMode(sensorPin1, INPUT);
  pinMode(sensorPin2, INPUT);
  pinMode(greenLedPin, OUTPUT);
  pinMode(relayPin, OUTPUT);
  Serial.begin(115200);
}


void loop() {
  int averageValue = calculateAverage(sensorPin1, sensorPin2);

  int moisturePercentage = mapToPercentage(averageValue);

  if (moisturePercentage < moistureThresholdLow) {
    digitalWrite(relayPin, LOW);
    digitalWrite(greenLedPin, HIGH);
    delay(250);
    digitalWrite(greenLedPin, LOW);
    delay(250);
    Serial.print("Watering Plants ");
  } else if (moisturePercentage >= moistureThresholdHigh) {
    digitalWrite(relayPin, HIGH);
    digitalWrite(greenLedPin, LOW);
  } else {
    digitalWrite(greenLedPin, HIGH);
    Serial.print("Plants are watered ");
  }

  Serial.print(" / Average moisture percentage is ");
  Serial.println(moisturePercentage);
  delay(1000);
}
