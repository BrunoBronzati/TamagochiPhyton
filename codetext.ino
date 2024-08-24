#include "WiFi.h"
#include "esp_wifi.h"
#include "WiFiClientSecure.h"

/*  Notas de Versão: Versão atualizada dia 31/08/2023
Nessa versão o código se preocupa em: (Padrão, Mais Atual)
- se conectar a internet
- verifica se as entradas 1 ou 2 ficaram 4 ou mais segundos pressionadas
- emite uma luz ao enviar as mensagens
- somente reenvia a mensagem depois de X minutos, definidos pelo programador na aba Temporizadores.
- controle de relê
- 4 portas de nível
- envia mensagem quando o nível retorna ao normal
- envia somente 1 mensagem enquanto o nivel não for reestabelecido
- envia mensagem para um amigo cadastrado.
- Tenta se reconectar a internet. Caso não consiga, ele reinicia o sistema
*/

// Editáveis do Cliente
const char* ssid = "Joaozinho Sehnem III"; //nome da rede do cliente
const char* password = "imortaltricolor"; //senha da rede do cliente
const char* token = "o.eVLc0nyPd3w8FdVkoXMMHg5X1eAJgFk4"; //pushbullet da placa
const char* tituloMSG = "Aguia Bullet";
const char* emailAmigo = "bulletgabineteprefeito@gmail.com"; // Substitua pelo email real do seu amigo
const char* corpoMSG01 = "Bomba Ligada";
const char* corpoMSG02 = "Caixa 01: Alerta nível 2 baixo";
const char* corpoMSG03 = "Caixa 01: Alerta nível 3 baixo";
const char* corpoMSG04 = "Caixa 01: Alerta nível 4 baixo";
const char* respostaMSG01 = "Bomba Desligada";
const char* respostaMSG02 = "Null, Não sera enviada ao cliente";
const char* respostaMSG03 = "Null, Não sera enviada ao cliente";
const char* respostaMSG04 = "Null, Não sera enviada ao cliente";
int Nivel01 = true;
int Nivel02 = true;
int Nivel03 = true;
int Nivel04 = true;

// Pinagens
int Saida01 = 13;
int Saida02 = 14;
int Saida03 = 23;
int Saida04 = 25;
int RelePin = 12;

// do sistema
int Recarga1 = 0;
int Recarga2 = 0;
int Temporizador1 = 0;
int Temporizador2 = 0;

// Pinagem da Luz
int LuzPin = 2;

// Temporizadores
unsigned long timer1 = 0;
unsigned long timer2 = 0;
unsigned long timer3 = 0;
unsigned long timer4 = 0;
unsigned long intervalo1 = 5000 ; // Tempo em milissegundos para reenviar a mensagem 1 (1 hora)
unsigned long intervalo2 = 5000; // Tempo em milissegundos para reenviar a mensagem 2 (1 hora)
unsigned long intervalo3 = 5000; // Tempo em milissegundos para reenviar a mensagem 3 (1 hora)
unsigned long intervalo4 = 5000; // Tempo em milissegundos para reenviar a mensagem 4 (1 minuto)

// Variáveis de controle das portas
bool porta01Ativada = false;
bool porta02Ativada = false;
bool porta03Ativada = false;
bool porta04Ativada = false;
bool porta01MensagemEnviada = false;
bool porta02MensagemEnviada = false;
bool porta03MensagemEnviada = false;
bool porta04MensagemEnviada = false;
unsigned long tempoPorta01Ativada = 0;
unsigned long tempoPorta02Ativada = 0;
unsigned long tempoPorta03Ativada = 0;
unsigned long tempoPorta04Ativada = 0;
unsigned long tempoPorta01Desativada = 0;
unsigned long tempoPorta02Desativada = 0;
unsigned long tempoPorta03Desativada = 0;
unsigned long tempoPorta04Desativada = 0;
unsigned long tempoMinimoAtivacao = 4000; // Tempo mínimo em milissegundos para ativação da porta (4 segundos)
unsigned long tempoMinimoDesativacao = 5000; // Tempo mínimo em milissegundos para desativação da porta (5 segundos)

// Variáveis de controle do relé
bool releFechado = false;
unsigned long tempoSinalOriginal = 0;
bool sinalOriginal = false;

void setup() {
  Serial.begin(115200);
  WiFi.begin(ssid, password);

  Serial.print("Conectando");
  while (WiFi.status() != WL_CONNECTED) {
    Serial.print(".");
    delay(100);
  }
  blinkLed(1, 1000);
  Serial.println("Conectado");
  Serial.print("Direccion IP: ");
  Serial.println(WiFi.localIP());

  pinMode(Saida01, INPUT_PULLUP);
  pinMode(Saida02, INPUT_PULLUP);
  pinMode(Saida03, INPUT_PULLUP);
  pinMode(Saida04, INPUT_PULLUP);
  pinMode(LuzPin, OUTPUT);
  pinMode(RelePin, OUTPUT);
  digitalWrite(RelePin, LOW); // Inicialmente, o relé está aberto
}

void loop() {
  // Verificar a conexão WiFi
  if (WiFi.status() != WL_CONNECTED) {

    Serial.println("Conexão WiFi perdida. Tentando reconectar...");
    WiFi.begin(ssid, password); // Tentar reconectar à rede WiFi
    int tentativas = 0;
    digitalWrite(LuzPin, HIGH);
    while (WiFi.status() != WL_CONNECTED && tentativas < 10) {
      delay(1000); // Aguardar 1 segundo para verificar a conexão novamente
      Serial.print(".");
      tentativas++;
    }
    if (WiFi.status() == WL_CONNECTED) {
      Serial.println("\nConexão WiFi restabelecida.");
          digitalWrite(LuzPin, LOW);

    } else {
      Serial.println("\nFalha ao reconectar. Reiniciando...");
      ESP.restart(); // Reiniciar o ESP32
    }
  }
  if (Nivel01) {
    if (digitalRead(Saida01) == 0) {
      if (!porta01Ativada) {
        tempoPorta01Ativada = millis(); // Registrar o tempo de ativação da porta
        porta01Ativada = true;
        porta01MensagemEnviada = false; // Reiniciar o status da mensagem enviada
      }
      if (millis() - tempoPorta01Ativada >= tempoMinimoAtivacao) {
        if (!porta01MensagemEnviada && millis() - timer1 >= intervalo1) {
          Serial.println("Comando enviado.");
          blinkLed(1, 1000);
          EnviarMensagem(tituloMSG, corpoMSG01);
          timer1 = millis(); // Reiniciar o temporizador
          porta01MensagemEnviada = true; // Marcar mensagem enviada
          delay(2000);
        }
      }
    } else {
      if (porta01Ativada) {
        if (millis() - tempoPorta01Desativada >= tempoMinimoDesativacao) {
          if (porta01MensagemEnviada) {
            EnviarMensagem(tituloMSG, respostaMSG01);
          }
          porta01Ativada = false;
          porta01MensagemEnviada = false; // Reiniciar o status da mensagem enviada
          tempoPorta01Desativada = millis();
        }
      }
    }
  }

  if (Nivel02) {
    if (digitalRead(Saida02) == 0) {
      if (!porta02Ativada) {
        tempoPorta02Ativada = millis(); // Registrar o tempo de ativação da porta
        porta02Ativada = true;
        porta02MensagemEnviada = false; // Reiniciar o status da mensagem enviada
      }
      if (millis() - tempoPorta02Ativada >= tempoMinimoAtivacao) {
        if (!porta02MensagemEnviada && millis() - timer2 >= intervalo2) {
          Serial.println("Comando enviado.");
          blinkLed(1, 1000);
          EnviarMensagem(tituloMSG, corpoMSG02);
          timer2 = millis(); // Reiniciar o temporizador
          porta02MensagemEnviada = true; // Marcar mensagem enviada
          delay(2000);
        }
      }
    } else {
      if (porta02Ativada) {
        if (millis() - tempoPorta02Desativada >= tempoMinimoDesativacao) {
          if (porta02MensagemEnviada) {
            //EnviarMensagem(tituloMSG, respostaMSG02);
          }
          porta02Ativada = false;
          porta02MensagemEnviada = false; // Reiniciar o status da mensagem enviada
          tempoPorta02Desativada = millis();
        }
      }
    }
  }

  if (Nivel03) {
    if (digitalRead(Saida03) == 0) {
      if (!porta03Ativada) {
        tempoPorta03Ativada = millis(); // Registrar o tempo de ativação da porta
        porta03Ativada = true;
        porta03MensagemEnviada = false; // Reiniciar o status da mensagem enviada
      }
      if (millis() - tempoPorta03Ativada >= tempoMinimoAtivacao) {
        if (!porta03MensagemEnviada && millis() - timer3 >= intervalo3) {
          Serial.println("Comando enviado.");
          blinkLed(1, 1000);
          EnviarMensagem(tituloMSG, corpoMSG03);
          timer3 = millis(); // Reiniciar o temporizador
          porta03MensagemEnviada = true; // Marcar mensagem enviada
          delay(2000);
        }
      }
    } else {
      if (porta03Ativada) {
        if (millis() - tempoPorta03Desativada >= tempoMinimoDesativacao) {
          if (porta03MensagemEnviada) {
            //EnviarMensagem(tituloMSG, respostaMSG03);
          }
          porta03Ativada = false;
          porta03MensagemEnviada = false; // Reiniciar o status da mensagem enviada
          tempoPorta03Desativada = millis();
        }
      }
    }
  }

if (Nivel04) {
    if (digitalRead(Saida04) == 0) {
      if (!porta04Ativada) {
        tempoPorta04Ativada = millis(); // Registrar o tempo de ativação da porta
        porta04Ativada = true;
        porta04MensagemEnviada = false; // Reiniciar o status da mensagem enviada
      }
      if (millis() - tempoPorta04Ativada >= tempoMinimoAtivacao) {
        if (!porta04MensagemEnviada && millis() - timer4 >= intervalo4) {
          Serial.println("Comando enviado.");
          blinkLed(1, 1000);
          EnviarMensagem(tituloMSG, corpoMSG04);
          timer4 = millis(); // Reiniciar o temporizador
          porta04MensagemEnviada = true; // Marcar mensagem enviada
          delay(2000);
        }
      }
    } else {
      if (porta04Ativada) {
        if (millis() - tempoPorta04Desativada >= tempoMinimoDesativacao) {
          if (porta04MensagemEnviada) {
            //EnviarMensagem(tituloMSG, respostaMSG04);
          }
          porta04Ativada = false;
          porta04MensagemEnviada = false; // Reiniciar o status da mensagem enviada
          tempoPorta04Desativada = millis();
        }
      }
    }
  }

}

const char* host = "api.pushbullet.com";
void EnviarMensagem(String titulo, String msg) {

  WiFiClientSecure client;
  client.setInsecure();
  if (!client.connect(host, 443)) {
    Serial.println("Nao foi possivel se conectar ao servidor");
    return;
  }

  String url = "/v2/pushes";
  String message = "{\"type\": \"note\", \"title\": \"" + titulo + "\", \"body\": \"" + msg + "\", \"email\": \"" + emailAmigo + "\"}\r\n";
  Serial.print("Requesting URL: ");
  Serial.println(url);
  // Envia uma mensagem
  client.print(String("POST ") + url + " HTTP/1.1\r\n" +
               "Host: " + host + "\r\n" +
               "Authorization: Bearer " + token + "\r\n" +
               "Content-Type: application/json\r\n" +
               "Content-Length: " +
               String(message.length()) + "\r\n\r\n");
  client.print(message);

  delay(2000);
  while (client.available() == 0);

  while (client.available()) {
    String line = client.readStringUntil('\n');
    Serial.println(line);
  }
}

void blinkLed(int vezes, int tempo) {
  for (int i = 0; i < vezes; i++) {
    digitalWrite(LuzPin, HIGH);
    delay(tempo);
    digitalWrite(LuzPin, LOW);
    delay(tempo);
  }
}
