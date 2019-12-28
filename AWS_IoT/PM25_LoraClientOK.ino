// for 台灣大學講課 LoraWAN
#include <Wire.h>
#include <SPI.h>
//#include <RH_RF95.h>
//#include <LiquidCrystal_I2C.h>
//LiquidCrystal_I2C lcd(0x27,16,2);  // 5V I2C LCD address to 0x27 16 x 2 line display

// for  Dragino Shield + UNO
#define RFM95_CS 10           // SS pin D10
#define RFM95_RST 4
#define RFM95_INT 2            //(interrupt 0 pin D2)
// Singleton instance of the radio driver
//RH_RF95 rf95(RFM95_CS, RFM95_INT); // RH_RF95 rf95(10, 2); // Dragino with RFM95
// Change to 434.0 or other frequency, must match RX's freq!
//#define RF95_FREQ 915.0    //頻率915.0MHz

int counter=0;
// SHARP GP2Y1010AU0F 使用測試代碼: 
//  　依使用說明最後四Pin (　紅　黑　白　藍)
// 　白 Pin　接 Arduino digital Pin ==>D7   註: D2與Dragino Lora Shield相沖
//     藍 Pin　接 Arduino analog Pin ==>A0
// I2C LED   與 Arduino ADK MEGA接線
// SDA to pin 20 SDA (Lilypad A4)
// CLK to pin 21 CLK (Lilypad A5)
//================================================
int dustPin=0;   // A0
float dustVal=0;
int ledPower=7;   // D7
int delayTime=280;
int delayTime2=40;
float offTime=9680;
//=========================
void setup() {
   pinMode(ledPower,OUTPUT);
   pinMode(dustPin, INPUT);
//   lcd.init();
//   // Turn on the blacklight and print a message.
//   lcd.backlight();
//   lcd.setCursor(0,0);
//   lcd.print("Dragino  Shield");
//   lcd.setCursor(0,1);
//   lcd.print("III Lora Client ");
   //====================================
  Serial.begin(115200);
  //while (!Serial) ; // Wait for serial port to be available
//  if (!rf95.init())
//  {
//   Serial.println("init failed");  
//    lcd.setCursor(0,0);
//    lcd.print("init failed        ");   
//  }
//  else
//  {
//    lcd.setCursor(0,0);
//    lcd.print("init succeeded        ");     
//  }

}
void loop()
{
   // ledPower is any digital pin on the arduino connected to Pin 3 on the sensor
    digitalWrite(ledPower,LOW); // power on the LED
    delayMicroseconds(delayTime);
    dustVal=analogRead(dustPin); // read the dust value via pin 5 on the sensor
    delayMicroseconds(delayTime2);
    digitalWrite(ledPower,HIGH); // turn the LED off
    delayMicroseconds(offTime);
    delay(3000);
    float AirQ=float((dustVal/1024)-0.0356)*120000*0.035;
    Serial.println((float(dustVal/1024)-0.0356)*120000*0.035);
    Serial.println(AirQ);
//    lcd.setCursor(0,1);
   String AirQT=" ";
   if (AirQ < 300)   { AirQT=" : Good      ";}
   if (AirQ >= 300 && AirQ < 1050)    { AirQT=" :Moderate";}
   if  ( AirQ >= 1050 && AirQ < 3000){ AirQT=" :Unhealthy";}
   if  (  AirQ > 3000){ AirQT=" :Hazardous";}
   //lcd.print((float(dustVal/1024)-0.0356)*120000*0.035+ AirQT);
//   lcd.print(AirQ+ AirQT);
   Serial.println(AirQ+ AirQT);
  //===============================
//   Serial.println("Sending to rf95_server");
  // Send a message to rf95_server
  // uint8_t data[] = "Hello World!";
  //==============
      uint8_t data[48] ;
      String total_countString = "PM2.5 > "+ String((int)AirQ,DEC)+ AirQT ;
      for (int i=0 ; i< 48; i++)
           {
             data[i] = total_countString.charAt(i);
            }
  //==============
//  rf95.send(data, sizeof(data));
//   lcd.clear();
//   lcd.print("Send Data ...");
//  rf95.waitPacketSent();
  // Now wait for a reply
//  uint8_t buf[RH_RF95_MAX_MESSAGE_LEN];
//  uint8_t len = sizeof(buf);

//  if (rf95.waitAvailableTimeout(3000))
//  { 
//    // Should be a reply message for us now   
//    if (rf95.recv(buf, &len))
//   {
//      Serial.print("got reply: ");
//      Serial.println((char*)buf);
//     // =========optional   added 2/9/2017 ========
//      String lineOut= (char*)buf;
//      lineOut= lineOut+ "                         ";
//      String Line0  = lineOut.substring(0,15);
//      String Line1  = "Rx:"+lineOut.substring(19,42);     
//      int rssiRev = rf95.lastRssi();
////      lcd.setCursor(0,0);
////      lcd.print("Tx:");    
////      lcd.print(counter,DEC);    
////      lcd.print(" RSSI= ");
////      lcd.print(rssiRev,DEC);   
////      lcd.setCursor(0,1);
////      lcd.print(Line1);  
////      Serial.print("RSSI: ");
////      Serial.println(rf95.lastRssi(), DEC);    
//    }
//    else
//    {
//      Serial.println("recv failed");
//    }
//  }
//  else
//  {
//    Serial.println("No reply, is rf95_server running?");
////     lcd.setCursor(0,0);
////     lcd.print("No reply,");
////     lcd.setCursor(0,1);
////     lcd.print("Server not running?");    
//  }
  delay(4000);
  counter++;
}
