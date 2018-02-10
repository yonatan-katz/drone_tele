
//black GND,white 3.3V 
int gas_vertical = 0;     // green
int gas_horizont = 1;     // yellow
int pos_vertical = 2;     // grey
int pos_horizont = 3;     // white
                         
char teapotPacket[10] = { '$', 0x02, 0, 0, 0, 0, 0x00, 0x00,'\r', '\n' };

void setup()
{
  Serial.begin(115200);              //  setup serial
}

void loop()
{
  /*
  teapotPacket[2] = analogRead(gas_vertical);     // read the input pin
  teapotPacket[3] = analogRead(pos_vertical);     // read the input pin
  teapotPacket[4] = analogRead(gas_horizont);     // read the input pin
  teapotPacket[5] = analogRead(pos_horizont);     // read the input pin
  Serial.write(teapotPacket, 10); 
  teapotPacket[12]++;
  Serial.write()
  */

  Serial.print(analogRead(gas_vertical));Serial.print(",");
  Serial.print(analogRead(gas_horizont));Serial.print(",");
  Serial.print(analogRead(pos_vertical));Serial.print(",");
  Serial.print(analogRead(pos_horizont));Serial.print(",");
  Serial.println("");
}
