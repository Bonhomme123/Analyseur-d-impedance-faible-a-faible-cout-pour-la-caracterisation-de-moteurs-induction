#define samplingRate 6000 // Hz
#define periode_us 1000000/samplingRate - 1
#define currentPin 34
#define voltagePin 35
#define arrayLenght 3000// max ~6000

volatile unsigned int currentArray[arrayLenght];
volatile unsigned int voltageArray[arrayLenght];

volatile unsigned int currentBuffer[arrayLenght];
volatile unsigned int voltageBuffer[arrayLenght];

volatile int arrayIndex = 0;
volatile bool flag = false;

hw_timer_t * My_timer = NULL;


void IRAM_ATTR onTimer(){
  //interruption fonction
  currentArray[arrayIndex] = analogRead(currentPin);
  voltageArray[arrayIndex] = analogRead(voltagePin);

  arrayIndex++;

  if(arrayIndex == arrayLenght){
    arrayIndex = 0;
    flag = true;
    copy(currentArray, currentBuffer, arrayLenght);
    copy(voltageArray, voltageBuffer, arrayLenght);
  }
}

void setup() {
  // put your setup code here, to run once:
  Serial.begin(921600);

  pinMode(voltagePin, INPUT);
  pinMode(currentPin, INPUT);

  //analogSetAttenuation(attenuation)???????????????? Peut-être ca baisse le range?
  
  My_timer = timerBegin(0, 80, true);
  timerAttachInterrupt(My_timer, &onTimer, true);
  timerAlarmWrite(My_timer, periode_us, true);
  timerAlarmEnable(My_timer);
}

void loop() {
  // put your main code here, to run repeatedly:
  if(flag){
    //printInfo();
    sendData();
    flag = false;
  }
}


void copy(volatile unsigned int* src, volatile unsigned int* dst, int len) {
    for (int i = 0; i < len; i++) {
        *dst++ = *src++;
    }
}


void sendData(){
  //int T1 = micros();
  for(int i = 0; i < arrayLenght; i++){
    //Serial.sprintf("%i,%voltageBuffer[i],%currentArray[i]")
    Serial.printf("%04d", i);
    Serial.print(",");
    Serial.printf("%04d",voltageBuffer[i]);
    Serial.print(",");
    Serial.printf("%04d\r\n", currentArray[i]);
   }
  //Serial.print("\nTemps :");
  //Serial.println((micros() - T1) / arrayLenght);
}

void printInfo(){
  Serial.print("\n\nFréquence: ");
  Serial.print(samplingRate);
  Serial.println(" Hz");

  Serial.print("Période: ");
  Serial.print(periode_us);
  Serial.println(" us");

  Serial.print("Longueur des arrays: ");
  Serial.println(arrayLenght);

  Serial.print("Pin courrant: ");
  Serial.println(currentPin);

  Serial.print("Pin tension: ");
  Serial.println(voltagePin);
}
