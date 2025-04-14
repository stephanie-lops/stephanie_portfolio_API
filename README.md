
# [API] Stephanie's Portfolio Register Center
**Autor: Stephanie Lopes**

Este projeto é o meu MVP da Sprint 3 do curso de **Desenvolvimento Full Stack Básico** da PUC RIO, 2024-2025.

Objetivo: Criação de API integrada a website pessoal para divulgação de fotografias analógicas e campo de contato para parcerias de trabalho. Essa API é responsável por:
```
(1) registro de clientes para banco de dados de contatos (Subscribe);
(2) contato com campo de mensagem que será enviada diretamente para o fotógrafo (Contact).
```
ATENÇÃO:
```
A chave  que está no repositório do MVP foi cancelada, por favor, utilizar a chave informada no drive do vídeo. (Atualizado: 14/04)
```
As rotas da função "Subscribe" utiliza 2 informações: nome e e-mail.

```
{
  "email": "string",
  "nome": "string"
}
```

A rota da função "Contact" (API externa) 3 informações: nome, e-mail e mensagem.

```
{
  "email": "user@example.com",
  "mensagem": "string",
  "nome": "string"
}
```

![image](https://github.com/user-attachments/assets/cc8a1090-bf9f-428e-bd53-8f42775b80c9)

---
## Como executar 

Será necessário ter todas as libs python listadas no `requirements.txt` instaladas.
Após clonar o repositório, é necessário ir ao diretório raiz, pelo terminal, para poder executar os comandos descritos abaixo.

> É fortemente indicado o uso de ambientes virtuais do tipo [virtualenv](https://virtualenv.pypa.io/en/latest/installation.html).

Criar ambiente virtual env:

```
python3 -m venv env
```

Ativar ambiente virtual env (Windows):

```
.\env\Scripts\activate
```

Instalar as dependências/bibliotecas, descritas no arquivo `requirements.txt`.

```
(env)$ pip install -r requirements.txt
```

## 1 - Para executar através do Flask

Para executar a API  basta executar:

```
(env)$ flask run --host 0.0.0.0 --port 5000
```

Em modo de desenvolvimento é recomendado executar utilizando o parâmetro reload, que reiniciará o servidor
automaticamente após uma mudança no código fonte. 

```
(env)$ flask run --host 0.0.0.0 --port 5000 --reload
```

Abra o [http://localhost:5000/#/](http://localhost:5000/#/) no navegador para verificar o status da API em execução.

---
## 2 - Como executar através do Docker

Certifique-se de ter o [Docker](https://docs.docker.com/engine/install/) instalado e em execução em sua máquina.

Navegue até o diretório que contém o Dockerfile e o requirements.txt no terminal.
Execute **como administrador** o seguinte comando para construir a imagem Docker:
```
$ docker build -t stephanie-portfolio-api .
```

Uma vez criada a imagem, para executar o container basta executar, **como administrador**, seguinte o comando:
```
$ docker run -p 5000:5000 stephanie-portfolio-api
```

Uma vez executando, para acessar a API, basta abrir o [http://localhost:5000/#/](http://localhost:5000/#/) no navegador.


### Alguns comandos úteis do Docker

**Para verificar se a imagem foi criada** você pode executar o seguinte comando:
```
$ docker images
```

 Caso queira **remover uma imagem**, basta executar o comando abaixo . Subistituindo o `IMAGE ID` pelo código da imagem
```
$ docker rmi <IMAGE ID>
```

**Para verificar se o container está em execução:
```
$ docker container ls --all
```

 Caso queira **parar um conatiner**:
```
$ docker stop <CONTAINER ID>
```

 Caso queira **destruir um conatiner**, basta executar o comando:
```
$ docker rm <CONTAINER ID>
```


---
## Como utilizar as rotas no Swagger

Para adicionar um cliente através da rota POST/client:
```
1 - Editar o campo Request body com os dados de nome e e-mail do cliente e ser registrado:

{
  "email": "joao@email.com",
  "nome": "joao"
}

2 - Clicar em Execute.
```

Para editar um cliente através da rota PUT:

```
1 - Editar o campo Request body com os dados atuai e os dados como eu gostaria de editar:

{
  "email": "stephanie_atualizado@email.com",
  "nome": "stephanie atuaizado",
  "originalEmail": "stephanie@email.com",
  "originalName": "stephanie"
}

2 - Clicar em Execute.
```

Para excluir um cliente através da rota DELETE:
```
1 - Editar o campo Request body com os dados de nome e e-mail do cliente a ser excluído:

{
  "email": "joao@email.com",
  "nome": "joao"
}

2 - Clicar em Execute.
```
Para buscar um cliente através da rota GET:
```
1 - Preencher o formulário com nome e e-mail ou pelo menos o nome, para ser buscado o e-mail.
2 - Clicar em Execute.
```

Para adicionar uma mensafem através da rota POST/contact:
```
1 - Editar o campo Request body com os dados de nome, e-mail do cliente e ser registrado e a mensagem a ser transmitida:

{
  "email": "beatriz@example.com",
  "mensagem": "Olá, gostaria de te chamar para participar de um projeto...",
  "nome": "beatriz"
}

2 - Clicar em Execute.
```
