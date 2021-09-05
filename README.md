# CatHouse 4.1

<div align="center">
<img src="catsecurity_logo.png" width="150px" height="auto">
</div>


###### **Na pasta _prints_ você pode ver algumas imagens do resultado do App funcionando.**


## **Instalação**

### **Criando env** _"opcional"_
```
python3 -m venv cathouse-env
```
E para ativar o env:
```
source cathouse-env/bin/activate
```

### **Dependências**
A instalação das dependências do projeto pode ser feita através do comando abaixo, utilizando o arquivo requirements.txt deste repositório.
```
pip install -r requirements.txt
```

### **Git clone**
Realize o clone deste repositório GIT com o comando abaixo, dentro da sua pasta de APPs no seu pojeto Django.
```
git clone https://github.com/douglas-vitor/cathouse.git
```

### **Criando o projeto django**
Estando dento do diretório do repositório clonado utilize o comando abaixo:
```
django-admin startproject ch4_1 .
```

### **Settings.py**
Vá para o diretório ch4_1 e altere o _settings.py_ ; dentro da lista INSTALLED_APPS, adicione o App 'ch_app' .
No fim deste mesmo arquivo adicione as seguintes linhas:
```
STATIC_URL = '/ch_app/static/'

LOGIN_REDIRECT_URL = 'home'
```
Então salve e feche o arquivo.

### **urls.py**
Ainda no diretório ch4_1 abra o arquivo _urls.py_ para realizar as seguintes modificações.
Adicione o seguinte import:
```
from django.urls import include
```
Na lista urlpatterns, adicione o seguinte path:
```
path("", include('ch_app.urls')),
```
Salve e feche este arquivo.

### **Migrate**
Vá para a raiz do projeto e então realize o primeiro migrate do seu projeto com o comando abaixo:
```
python3 manage.py migrate
```

### **Cria super usuario**
Agora com o comando a seguir crie um usuário para ter acesso ao App.
```
python3 manage.py createsuperuser
```

### **Sincronizar banco de dados**
Sincronize o banco de dados com as tabelas do nosso App.
```
python3 manage.py migrate --run-syncdb 
```

### **Iniciando o sevidor**
Agora execute o comando a baixo para iniciar o servidor para poder testar o App.
```
python3 manage.py runserver
```

## **Informações tabelas BD**
### **Tabela R_wifis** 
###### **Rw e Ip = _Ip interno do dispositivo IOT;_**
###### **Type = _Tipo deste dispositivo (LUZ, TOMADA, TRAVA);_**
###### **Type2 = _Tipo complementar deste dispositivo, usado no caso de dimmers ou RGB (DIMMER = com dimmer; RGB = com RGB ou 0 = nenhum);_**
###### **Name = _Nome do dispositivo "Recomendado colocar o nome do ambiente onde esta o dispositivo IOT";_**

### **Tabela Sensor_wifis**
###### **Ip = _Ip interno do dispositivo IOT;_**
###### **Name = _Nome do dispositivo "Recomendado colocar o nome do ambiente onde esta o dispositivo IOT";_**

### **Tabela Timers**
###### **Arm = _0 = Desligado; 1 = Ligado;_**
###### **Time = _Hora no formato 24Horas HH:MM;_**
###### **Window = _0;_**
###### **Days = _Iniciais dos dias da semana em inglês, substituindo os dias não desejados por " - ", exemplo: S-TW-FS ;_**
###### **Repeat_timer = _0 = Não repetir; 1 = Repetir;_**
###### **Output = _1;_**
###### **Action = _0 = Desligar; 1 = Ligar;_**
###### **Ip = _Ip interno do dispositivo IOT_**
###### **Name = _Nome do timer no seguinte formato: timer{NUM}. Exemplo: timer2, timer6;_**
###### **Name_for_user = _Nome resumido para o usuário;_**