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
