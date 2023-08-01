#define samplingRate 6000                     // Fréquence d'échatillonage en Hz
#define periode_us 1000000/samplingRate - 1   // Période d'échantillonage en us
#define currentPin 34                         // Numéro de la pin pour le signal du courant
#define voltagePin 35                         // Numéro de la pin pour le signal de la tension
#define arrayLength 3000                      // Longueur des arrays (max ~6000, limité par la mémoire)
#define baudrate 921600                       // pour le port de série (diminuer si ca bug)

volatile unsigned int currentArray[arrayLength]; // Array principal pour les données de courant
volatile unsigned int voltageArray[arrayLength]; // Array principal pour les données de tension

volatile unsigned int currentBuffer[arrayLength]; // Buffer pour les données de courant
volatile unsigned int voltageBuffer[arrayLength]; // Buffer pour les données de tension

volatile int arrayIndex = 0;                  // Index pour l'écriture de la prochaine donnée dans les arrays
volatile bool flag = false;                   // Indicateur d'arrays pleins

hw_timer_t * My_timer = NULL;                 // Code nécessaire pour l'interrupt

void IRAM_ATTR onTimer(){                     // Interruption fonction

  // Écriture des données
  currentArray[arrayIndex] = analogRead(currentPin);
  voltageArray[arrayIndex] = analogRead(voltagePin);

  // Update de l'index
  arrayIndex++;

  if(arrayIndex == arrayLength){              // Si les arrays sont pleins,
    arrayIndex = 0;                           // Reset l'index
    flag = true;                              // Active l'indicateur
    copy(currentArray, currentBuffer, arrayLength); // Copie les arrays dans les buffers
    copy(voltageArray, voltageBuffer, arrayLength);
  }
}

void setup() {
  
  Serial.begin(baudrate);

  pinMode(voltagePin, INPUT);
  pinMode(currentPin, INPUT);

  analogSetAttenuation(ADC_0db);//???????????????? Peut-être ca baisse le range?

  // Régler l'interrupt
  My_timer = timerBegin(0, 80, true);
  timerAttachInterrupt(My_timer, &onTimer, true);
  timerAlarmWrite(My_timer, periode_us, true);
  timerAlarmEnable(My_timer);
}

void loop() {

  if(flag){                                   // si les arrays sont pleins
    //printInfo();
    sendData();                               // Envoie les données au port de série
    flag = false;                             // Désactive l'indicateur
  }
}


void copy(volatile unsigned int* src, volatile unsigned int* dst, int len) { // Fonction pour copier un array dans un autre
    for (int i = 0; i < len; i++) {
        *dst++ = *src++;
    }
}


void sendData(){                              // Envoie les données au port de série
  //int T1 = micros();
  for(int i = 0; i < arrayLength; i++){
    //Serial.sprintf("%i,%voltageBuffer[i],%currentArray[i]")
    Serial.printf("%04d", i);                 // Index formater à 4 chiffres
    Serial.print(",");
    Serial.printf("%04d",voltageBuffer[i]);   // Tension formater à 4 chiffres
    Serial.print(",");
    Serial.printf("%04d\r\n", currentArray[i]); // Courant formater à 4 chiffres
   }
  //Serial.print("\nTemps :");
  //Serial.println((micros() - T1) / arrayLength);
}

void printInfo(){                               // envoie les infos d'acquisition 
  Serial.print("\n\nFréquence: ");
  Serial.print(samplingRate);
  Serial.println(" Hz");

  Serial.print("Période: ");
  Serial.print(periode_us);
  Serial.println(" us");

  Serial.print("Longueur des arrays: ");
  Serial.println(arrayLength);

  Serial.print("Pin courrant: ");
  Serial.println(currentPin);

  Serial.print("Pin tension: ");
  Serial.println(voltagePin);
}
