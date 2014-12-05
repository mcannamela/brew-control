
bool verbose = false;
void serialPrintCharArray(char* array, int n){
  for (int i=0;i<n;i++){
    Serial.print(array[i]);
  }
};

void serialPrintLnCharArray(char* array, int n){
  serialPrintCharArray(array, n);
  Serial.print('\n');
};

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


