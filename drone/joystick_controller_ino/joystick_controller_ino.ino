

int gas_vertical = 0;     // potentiometer wiper (middle terminal) connected to analog pin 3
int pos_vertical = 1;     // potentiometer wiper (middle terminal) connected to analog pin 3
int gas_horizont = 2;     // potentiometer wiper (middle terminal) connected to analog pin 3
int pos_horizont = 3;     // potentiometer wiper (middle terminal) connected to analog pin 3
                         
char teapotPacket[10] = { '$', 0x02, 0, 0, 0, 0, 0x00, 0x00,'\r', '\n' };

void setup()
{
  Serial.begin(115200);              //  setup serial
}

void loop()
{

  teapotPacket[2] = (uint8_t)(analogRead(gas_vertical)/3.0);     // read the input pin
  teapotPacket[3] = (uint8_t)(analogRead(pos_vertical)/3.0);     // read the input pin
  teapotPacket[4] = (uint8_t)(analogRead(gas_horizont)/3.0);     // read the input pin
  teapotPacket[5] = (uint8_t)(analogRead(pos_horizont)/3.0);     // read the input pin
  Serial.write((const uint8_t*)teapotPacket, 10); 
  teapotPacket[7]++;

#ifdef DEBUG
  Serial.println(analogRead(gas_vertical));
  Serial.println(analogRead(pos_vertical));
  Serial.println(analogRead(gas_horizont));
  Serial.println(analogRead(pos_horizont));
#endif
}
