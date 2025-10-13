#include <Wire.h>

#define ADS7830_ADDRESS 0x48  // Default I2C address for ADS7830

void setup() {
  Wire.begin();
  Serial.begin(9600);
  Serial.println("Adafruit ADS7830 Example");
}

void loop() {
  for (int channel = 0; channel < 8; channel++) {
    uint8_t value = readADS7830(channel);
    Serial.print("Channel ");
    Serial.print(channel);
    Serial.print(": ");
    Serial.println(value);
  }
  Serial.println("----");
  delay(500);
}

uint8_t readADS7830(uint8_t channel) {
  // Control byte format:
  //  [SGL/DIF][ODD/SIGN][C2][C1][C0][PD1][PD0]
  // For single-ended mode, PD bits = 11 (power up A/D and reference)
  
  uint8_t control = 0x84 | (channel << 4); // 1000 0100 | (channel << 4)
  
  Wire.beginTransmission(ADS7830_ADDRESS);
  Wire.write(control);
  Wire.endTransmission();
  
  Wire.requestFrom(ADS7830_ADDRESS, 1);
  if (Wire.available()) {
    return Wire.read();
  } else {
    return 0;
  }
}
