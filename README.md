# Instalação
## Clonando o Repositório
Clone o repositório em uma pasta de sua preferência

## Instalando Dependências
### Pipenv
Instalar o pipenv, que gerencia as dependências do projeto.

Caso esteja no MacOS brew install pipenv
```brew install pipenv```

Caso esteja usando Debian Buster+
```sudo apt install pipenv```

Caso esteja usando Fedora
```sudo dnf install pipenv```

Caso esteja usando FreeBSD
```pkg install py36-pipenv```

Caso contrário
```pip install pipenv```

## Iniciando o projeto
Rode o pipenv na raíz do projeto onde estão os arquivos Pipfile e Pipfile.lock com o comando ```pipenv install```

Isso irá instalar todas as dependência internas do projeto

Inicie o virtualenv do pipenv com o comando ```pipenv shell```

Vá para a pasta raíz da aplicação em ```risk_calculator```

Atualize as migrações padrões do django através do comando ```python manage.py migrate```

Inicie o servidor do projeto com o comando ```python manage.py runserver```

Para desativar o pipenv basta usar o comando ```exit``` ou ```Ctrl+d```

## Rodando testes
Para rodar os testes do projeto basta usar o comando ```python manage.py test```

## Endpoints
### /risk/calculator - POST
É necessário enviar um CRSFTOKEN no header através da chave ```X-CSRFToken````, para fins do teste, usar o endpoint abaixo para conseguir o valor.

#### Request Payload
```
{
  "age": 35,
  "dependents": 2,
  "house": {"ownership_status": "owned"},
  "income": 0,
  "marital_status": "married",
  "risk_questions": [0, 1, 0],
  "vehicle": {"year": 2018}
}
````
Todas as chaves são obrigatórias, no caso de vehicle e house, caso o usuário não tenha carro ou casa enviar um dicionário vazio ```{}```

#### Response Payload
```
{
    "auto": "economic",
    "disability": "ineligible",
    "home": "economic",
    "life": "regular"
}
```
Cada campo pode ter uma das seguintes respostas ```economic, ineligible, regular, responsible``` . O status code da resposta é 200.

No caso de algum valor inválido será retornado um HTTPResponse, com status code 400 e uma breve descrição do que está incorreto.

### /risk/crsf - GET
Endpoint conceitual apenas para fornecer de forma fácil o CRSF Token para os fins do teste.

#### Response Payload
O token CRSF para ser usado nos Headers do calculator/risk
