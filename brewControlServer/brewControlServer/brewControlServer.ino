/*
 Circuit:
 * Ethernet shield attached to pins 10, 11, 12, 13
 
 */

#include <SPI.h>
#include <Ethernet.h>


///////////////////////////////////////////////////
//////////////////////////////CONSTANTS////////////
///////////////////////////////////////////////////

const char HLT[] = "HLT";
const int HLT_LEN = 3;

const char MASH[] = "MASH";
const int MASH_LEN = 4;

const char FERMENTER[] = "FERMENTER";
const int FERMENTER_LEN = 9;

const char  ON[] = "ON";
const int ON_LEN = 2;

const char OFF[] = "OFF";
const int OFF_LEN = 3;

const char GET[] = "GET";
const int GET_LEN = 3;

const int hltActuatorPin = 7;
const int mashActuatorPin = 8;
const int fermenterActuatorPin = 9;

const int hltTemperaturePin = 0;
const int mashTemperaturePin = 1;
const int fermenterTemperaturePin = 2;



const int bufferLength = 128;

boolean verbose = true;

class BrewCommands {
public: 

  const static char commandSeparator = ':';
  const static char argumentSeparator = '-';
  const static char reportSeparator = '=';
  
};
///////////////////////////////////////////////////

//-----------------------------------------------------
//--------------------------GLOBALS--------------------
//-----------------------------------------------------

char messageBuffer[bufferLength], rawCommand[bufferLength], 
    command[bufferLength], variable[bufferLength],argument[bufferLength],
    floatConvertBuffer[bufferLength];

int nMessageBuffer = 0, nRawCommand=0, nCommand=0, nVariable=0, nArgument=0, nFloatConvert=0;

double thermistorResistance, thermistorTemperature;

//-----------------------------------------------------



//>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
//>>>>>>>>>>>>>>>>>>>ETHERNET CONFIG>>>>>>>>>>>>>>>>>>>>>>>>>>
//>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
byte mac[] = { 
  0x00, 0xAA, 0xBB, 0xCC, 0xDE, 0x02 };
IPAddress ip(192,168,11, 101);
IPAddress gateway(192,168,1, 1);
IPAddress subnet(255, 255, 255, 0);

//8334 = BEER in 1337-speak
EthernetServer server(8334);
EthernetClient client;
//>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

///////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////
void setup() {
  pinMode(hltActuatorPin, OUTPUT);
  pinMode(mashActuatorPin , OUTPUT);
  pinMode(fermenterActuatorPin, OUTPUT);
  
  
     char fillChar = '_';
  for(int i=0;i<bufferLength;i++){
    messageBuffer[i] = fillChar;
    rawCommand[i] = fillChar;
    command[i] = fillChar;
    variable[i] = fillChar;
    argument[i] = fillChar;

  }
  // Open serial communications and wait for port to open:
  Serial.begin(9600);
  // this check is only needed on the Leonardo:
  while (!Serial) {
    ; // wait for serial port to connect. Needed for Leonardo only
    

  }


  // start the Ethernet connection:
  Serial.println("Trying to get an IP address using DHCP");
  if (true){//(Ethernet.begin(mac) == 0) {
    Serial.println("Failed to configure Ethernet using DHCP");
    // initialize the ethernet device not using DHCP:
    Ethernet.begin(mac, ip, gateway, subnet);
  }
  // print your local IP address:
  Serial.print("My IP address: ");
  ip = Ethernet.localIP();
  for (byte thisByte = 0; thisByte < 4; thisByte++) {
    // print the value of each byte of the IP address:
    Serial.print(ip[thisByte], DEC);
    Serial.print("."); 
  }
  Serial.println();
  // start listening for clients
  server.begin();
  
  }
///////////////////////////////////////////////////////////////


void loop() {
   

  client = server.available();
  while (client.connected()) {
      if (client.available()>0){
        delay(20); 
          
        receiveMessage(client);
        client.flush();
        verbosePrint("got the message: ");
        
        verbosePrintLn(rawCommand, nRawCommand);
        
        //echo for debugging purposes
        //copyArrayToMessageBuffer(rawCommand, nRawCommand);
        //writeMessage(server);

        verbosePrintLn("parsing begin.");
        
        parseCommand();
        verbosePrintLn("command parsed: ");
        verbosePrintLn(command, nCommand);
        
        parseVariable();
        verbosePrintLn("variable parsed: ");
        verbosePrintLn(variable, nVariable);
        
        parseArgument();
        verbosePrintLn("argument parsed: ");
        verbosePrintLn(argument, nArgument);
        
        verbosePrintLn("...parsing complete!");

        verbosePrintLn("report to client complete");
        
        
        
        if (compareArrays(command,nCommand, ON,ON_LEN)){
          if (compareArrays(variable,nVariable, HLT, HLT_LEN))
            digitalWrite(hltActuatorPin, HIGH);
          else if (compareArrays(variable,nVariable, MASH, MASH_LEN))
            digitalWrite(mashActuatorPin, HIGH);
          else if (compareArrays(variable,nVariable, FERMENTER, FERMENTER_LEN))
            digitalWrite(fermenterActuatorPin, HIGH);
        }
        else if (compareArrays(command,nCommand, OFF,OFF_LEN)){
          if (compareArrays(variable,nVariable, HLT, HLT_LEN))
            digitalWrite(hltActuatorPin, LOW);
          else if (compareArrays(variable,nVariable, MASH, MASH_LEN))
            digitalWrite(mashActuatorPin, LOW);
          else if (compareArrays(variable,nVariable, FERMENTER, FERMENTER_LEN))
            digitalWrite(fermenterActuatorPin, LOW);
        }
        
        if (compareArrays(command,nCommand, GET,GET_LEN)){
          if (compareArrays(variable,nVariable, HLT, HLT_LEN)){
            thermistorResistance = readThermistorResistance(hltTemperaturePin);
            thermistorTemperature = resistanceToTemperature(thermistorResistance);
            Serial.print("HLT temperature: ");
            Serial.println(thermistorTemperature);
          }
          else if (compareArrays(variable,nVariable, MASH, MASH_LEN)){
            thermistorResistance = readThermistorResistance(mashTemperaturePin);
            thermistorTemperature = resistanceToTemperature(thermistorResistance);
            Serial.print("mash temperature: ");
            Serial.println(thermistorTemperature);
          }
          else if (compareArrays(variable,nVariable, FERMENTER, FERMENTER_LEN)){
            thermistorResistance = readThermistorResistance(fermenterTemperaturePin);
            thermistorTemperature = resistanceToTemperature(thermistorResistance);
            Serial.print("fermenter temperature: ");
            Serial.println(thermistorTemperature);
          }
          
          server.print(int(thermistorTemperature));
          server.print('.');
          server.println( int( (thermistorTemperature-int(thermistorTemperature))*10 ) );
          
        }
        else{
          copyArrayToMessageBuffer(rawCommand, nRawCommand);
          writeMessage(server);
        }
        
        client.flush();
        client.stop();
      }
  }

}

//:::::::::::::::::::::::::::::::::::::::::::::::::::::
//::::::::::::::::::::FUNCTIONS::::::::::::::::::::::::
//:::::::::::::::::::::::::::::::::::::::::::::::::::::
double readThermistorResistance(int pinNr){
  double R;
  int adcValue = analogRead(pinNr);
  if (adcValue ==0)
    adcValue = 1;
  R = 10000.0/(1023.0/((double)adcValue) -1);
  return R;
}
double resistanceToTemperature(double R){
  double rT;
  rT = 1.0/298.15+(1.0/3950.0)*log(R/10000.0);
  return 1.0/rT-273.15;
}

void parseCommand(){
  char c;
  nCommand = 0;
  int start =0;
  for (int i=start;i<nRawCommand;i++){
    c = rawCommand[i];
    if (c!=BrewCommands::commandSeparator){
      command[nCommand]=c;
      nCommand++;
    }
    else{
      break;
    }
  }
};

void parseVariable(){
  char c;
  nVariable = 0;

  int start =nCommand+1;
  for (int i=start;i<nRawCommand;i++){
    c = rawCommand[i];
    if (c!=BrewCommands::argumentSeparator){
      variable[nVariable]=c;
      nVariable++;
    }
    else{
      break;
    }
    
  }
};

void parseArgument(){
  char c;
  nArgument = 0;
  int start =nVariable+nCommand+2; 
  for (int i=start;i<nRawCommand;i++){
    c = rawCommand[i];
    argument[nArgument]=c;
    nArgument++;
    }
};

void receiveMessage(EthernetClient client){
  
  char c;
  nRawCommand = 0;
  Serial.println("\nbegin reading message.");
  delay(10);
  for (int i = 0;i<bufferLength;i++){
    if(client.available()>0){
      c = client.read();
      rawCommand[i]=c;
      nRawCommand++;
    }
  }

};

void writeMessage(EthernetServer server){
  for (int i=0;i<nMessageBuffer;i++){
    server.write(messageBuffer[i]);
  }
  server.write('\n');
};


void copyArrayToMessageBuffer(char*array, int n){
  nMessageBuffer = 0;
  for (int i=0;i<n;i++){
    messageBuffer[i]=array[i];
    nMessageBuffer++;
  }
};

void serialPrintCharArray(char* array, int n){
  for (int i=0;i<n;i++){
    Serial.print(array[i]);
  }
};
void serialPrintLnCharArray(char* array, int n){
  serialPrintCharArray(array, n);
  Serial.print('\n');
};

boolean compareArrays(char* a1,  int n1, const char* a2, const int n2){
  if (n1!=n2){
    return false;
  }
  for (int i=0;i<n1;i++){
    if (a1[i]!=a2[i]){
      return false;
    }
  }
  return true;
}

void verbosePrint(char printable){
  if (verbose){
    Serial.print(printable);
  }
}
void verbosePrint(char* printable){
  if (verbose){
    Serial.print(printable);
  }
}
void verbosePrint(char* printable, int n){
  if (verbose){
    serialPrintCharArray(printable,n);
  }
}
void verbosePrint(int printable){
  if (verbose){
    Serial.print(printable);
  }
}
void verbosePrintLn(char* printable){
  if (verbose){
    Serial.println(printable);
  }
}
void verbosePrintLn(char* printable, int n){
  if (verbose){
    serialPrintLnCharArray(printable,n);
  }
}

void verbosePrintLn(int printable){
  if (verbose){
    Serial.println(printable);
  }
}


//:::::::::::::::::::::::::::::::::::::::::::::::::::::




