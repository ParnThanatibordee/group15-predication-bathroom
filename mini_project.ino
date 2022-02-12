#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>

const char* ssid = "khem 2G";
const char* password = "ACJFnpk***2063EG";
const char* url_post = "https://ecourse.cpe.ku.ac.th/exceed15/api/bathroom/update";

int led1 = 5;//1st room
int led2 = 21;//2nd room
int led3 = 22;//3rd room

int ldr1 = 34;
int ldr2 = 39;
int ldr3 = 36;

char str[50];
int st1;
int st2;
int st3;
int st[]={st1,st2,st3};

const int _size = 2*JSON_OBJECT_SIZE(4);

StaticJsonDocument<_size> JSONPost;

void WiFi_Connect(){
  WiFi.disconnect();
  WiFi.begin(ssid,password);
  while(WiFi.status()!=WL_CONNECTED){
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }

  Serial.println("Connected to the WiFi network");
  Serial.print("IP Address : ");
  Serial.println(WiFi.localIP());
}

void _post(){
  if(WiFi.status() == WL_CONNECTED){
    for(int i=0;i<3;i++){
      HTTPClient http;
    
      http.begin(url_post);
      http.addHeader("Content-Type", "application/json");

      JSONPost["number"] = i+1;
      JSONPost["available"] = st[i];

      serializeJson(JSONPost, str);
      int httpCode = http.POST(str);
      Serial.printf("\nTry to send status room : %d\n",st[i]);
    
      if(httpCode == HTTP_CODE_OK){
        String payload = http.getString();
        Serial.println(httpCode);     
        Serial.println("POST result");
        Serial.println(payload);
      } else{
        Serial.println(httpCode);
        Serial.println("ERROR on HTTP Request");
      }
    }
  }else{
    WiFi_Connect();
  }
  delay(10);
}

void setup() {
  xTaskCreatePinnedToCore(TaskA, "Task A", 1024, NULL, 1, NULL, 1);
  pinMode(ldr1, INPUT);
  pinMode(ldr2, INPUT);
  pinMode(ldr3, INPUT);

  pinMode(led1, OUTPUT);
  pinMode(led2, OUTPUT);
  pinMode(led3, OUTPUT);

  digitalWrite(led1, HIGH);
  digitalWrite(led2, LOW);
  digitalWrite(led3, LOW);
  Serial.begin(9600);
  WiFi_Connect();
}

void TaskA(void *parameter){
  while(1){
    if(analogRead(ldr1)>1400){
      digitalWrite(led1, HIGH);//not empty
      st[0]=0;
    }else{
      digitalWrite(led1, LOW);//empty
      st[0]=1;
    }
    if(analogRead(ldr2)>700){
      digitalWrite(led2, LOW);//not empty
      st[1]=0;
    }else{
      digitalWrite(led2, HIGH);//empty
      st[1]=1;
    }
    if(analogRead(ldr3)>1400){
      digitalWrite(led3, LOW);//not empty
      st[2]=0;
    }else{
      digitalWrite(led3, HIGH);//empty
      st[2]=1;
    }
    delay(10);
    vTaskDelay(10/portTICK_PERIOD_MS);
  }
}  

void loop() {
  _post();
  delay(1000);
}
