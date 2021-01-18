#include <RGBLed.h>
RGBLed led(11, 10, 9, RGBLed::COMMON_CATHODE);

/*
	Pin 9  - Red
	Pin 10 - Green
	Pin 11 - Blue
*/

String RGB = ""; 
String RGB_Previous = "255.255.255"; 
String DEBUG = "";
String ON = "ON"; 
String OFF = "OFF"; 
boolean RGB_Completed = false;
 
void setup() {
  Serial.begin(9600); 
}
 
void loop() {

  while(Serial.available()){
    char ReadChar = (char)Serial.read();
 
    if(ReadChar == '\n'){
      RGB_Completed = true;
      Serial.print(ReadChar);
    }else{
      RGB += ReadChar;
      Serial.print(ReadChar); 
    }
  }
  
  if(RGB_Completed){
 
      Serial.print("RGB:");
      Serial.println(RGB);
      Serial.print("PreRGB:");
      Serial.println(RGB_Previous);
      Serial.print("Debug:");
      Serial.println(DEBUG);
      
      if(RGB==ON){
          RGB = RGB_Previous; 
          Light_RGB_LED();
      }else if(RGB==OFF){
          RGB = "0.0.0"; 
          Light_RGB_LED();
      }else{
          Light_RGB_LED();   
          RGB_Previous = RGB;
          DEBUG=RGB  ;   
      }
      RGB = "";
      RGB_Completed = false;      
  } 
} 
 
void Light_RGB_LED(){

 // Delimiters
  int SP1 = RGB.indexOf(' ');
  int SP2 = RGB.indexOf(' ', SP1+1);
  int SP3 = RGB.indexOf(' ', SP2+1);
  
  String R = RGB.substring(0, SP1);
  String G = RGB.substring(SP1+1, SP2);
  String B = RGB.substring(SP2+1, SP3);

  Serial.print("R=");
  Serial.println( constrain(R.toInt(),0,255));
  Serial.print("G=");
  Serial.println(constrain(G.toInt(),0,255));
  Serial.print("B=");
  Serial.println( constrain(B.toInt(),0,255));
 
  led.setColor(R.toInt(), G.toInt(), B.toInt());

}
