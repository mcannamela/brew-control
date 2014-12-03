/*
 Circuit:
 * Ethernet shield attached to pins 10, 11, 12, 13
 
 */
#include <WebServer.h>
#include <SPI.h>
#include <Ethernet.h>
#include <brewControl.h>
#include <verbosePrint.h>

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

int nMessageBuffer = 0, nRawCommand=0, nCommand=0, nVariable=0, nArgument=0, nFloatConvert=0, loopCounter;

double thermistorResistance, hltTemperature, mashTemperature, fermenterTemperature, thermistorTemperature;


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
	setupBrewPins();
	setupBuffers();
	setupSerial();
	setupEthernet();
  }
///////////////////////////////////////////////////////////////


void loop() {
	//don't burn the place down
	loopCounter++;
	if (loopCounter>=1000){
		deactuate();
		loopCounter=0;
	}
	
	hltTemperature = getHltTemperature();
	mashTemperature = getMashTemperature();
	fermenterTemperature = getFermenterTemperature();

	client = server.available();
  
	if (!client.connected()){ 
	  printTemperatures();
	}
  
  while (client.connected()) {
      if (client.available()>0){
        delay(20); 
          
        receiveMessage(client);
        client.flush();

        parseMessage();
        
        
        if (compareArrays(command,nCommand, ON,ON_LEN)){
          if (compareArrays(variable,nVariable, HLT, HLT_LEN))
            actuateHltHeater();
          else if (compareArrays(variable,nVariable, MASH, MASH_LEN))
            actuateMashHeater();
          else if (compareArrays(variable,nVariable, FERMENTER, FERMENTER_LEN))
            actuateFermenterHeater();
        }
        else if (compareArrays(command,nCommand, OFF,OFF_LEN)){
          if (compareArrays(variable,nVariable, HLT, HLT_LEN))
            deactuateHltHeater();
          else if (compareArrays(variable,nVariable, MASH, MASH_LEN))
            deactuateMashHeater();
          else if (compareArrays(variable,nVariable, FERMENTER, FERMENTER_LEN))
            deactuateFermenterHeater();
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

void setupBuffers(){
	char fillChar = '_';
	for(int i=0;i<bufferLength;i++){
		messageBuffer[i] = fillChar;
		rawCommand[i] = fillChar;
		command[i] = fillChar;
		variable[i] = fillChar;
		argument[i] = fillChar;
	}
}

void setupSerial(){
	Serial.begin(9600);
	// this check is only needed on the Leonardo:
	while (!Serial) {
	; // wait for serial port to connect. Needed for Leonardo only
	}
}

void setupEthernet(){
	Serial.println("Configure static ip...");
	Ethernet.begin(mac, ip, gateway, subnet);
	Serial.print("My IP address: ");
	ip = Ethernet.localIP();
	for (byte thisByte = 0; thisByte < 4; thisByte++) {
		Serial.print(ip[thisByte], DEC);
		Serial.print("."); 
	}
	Serial.println();
	server.begin();
}

void printTemperatures(){
	Serial.print("(HLT, MASH, FERM) = ");
    Serial.print(hltTemperature);
    Serial.print(", ");
    Serial.print(mashTemperature);
    Serial.print(", ");
    Serial.println(fermenterTemperature);
    delay(20);
}

void parseMessage(){
	verbosePrint("got the message: ");
	verbosePrintLn(rawCommand, nRawCommand);

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
}

bool isOnCommand(){
	compareArrays(command,nCommand, ON,ON_LEN);
}

bool isOffCommand(){
	compareArrays(command,nCommand, OFF,OFF_LEN);
}

bool isGetCommand(){
	compareArrays(command,nCommand, GET,GET_LEN)
}

bool isMash(){
	compareArrays(variable,nVariable, MASH, MASH_LEN)
}

bool isHlt(){
	compareArrays(variable,nVariable, HLT, HLT_LEN)
}

bool isFermenter(){
	compareArrays(variable,nVariable, FERMENTER, FERMENTER_LEN)
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




//:::::::::::::::::::::::::::::::::::::::::::::::::::::




