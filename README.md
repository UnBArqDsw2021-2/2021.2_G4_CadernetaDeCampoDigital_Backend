# Backend Caderneta de Campo Digital

<div align="center">
    <img src="https://github.com/UnBArqDsw2021-2/2021.2_G4_CadernetaDeCampoDigital_docs/blob/master/docs/assets/logo.png"></img>
</div>

<p align="center">
    <a href="https://github.com/UnBArqDsw2021-2/2021.2_G4_CadernetaDeCampoDigital_Backend/actions/workflows/test.yml">
	    <img alt="Test status" src="https://github.com/UnBArqDsw2021-2/2021.2_G4_CadernetaDeCampoDigital_Backend/actions/workflows/test.yml/badge.svg?style=flat">
	</a>
    <!-- <a href="https://github.com/UnBArqDsw2021-2/2021.2_G4_CadernetaDeCampoDigital_Backend/actions/workflows/test.yml">
	    <img alt="Test status" src="https://github.com/UnBArqDsw2021-2/2021.2_G4_CadernetaDeCampoDigital_Backend/actions/workflows/test.yml/badge.svg?style=flat">
	</a> DEPLOY-->
    <a href="https://codecov.io/gh/UnBArqDsw2021-2/2021.2_G4_CadernetaDeCampoDigital_Backend">
        <img src="https://codecov.io/gh/UnBArqDsw2021-2/2021.2_G4_CadernetaDeCampoDigital_Backend/branch/develop/graph/badge.svg?token=WWRQ3MXK7G"/>
    </a>
    <a href="https://codeclimate.com/github/UnBArqDsw2021-2/2021.2_G4_CadernetaDeCampoDigital_Backend/maintainability"><img src="https://api.codeclimate.com/v1/badges/5a726f1be0757850865f/maintainability" />
    </a>
</p>

<p align="center">
    <a href="https://github.com/UnBArqDsw2021-2/2021.2_G4_CadernetaDeCampoDigital_Mobile"><strong>Repositório Mobile</strong></a>
</p>
<p align="center">
    <a href="https://github.com/UnBArqDsw2021-2/2021.2_G4_CadernetaDeCampoDigital_docs"><strong>Wiki do Projeto</strong></a>
</p>

## Rodando pela primeira vez
Para iniciar o backend pela primeira vez é necessário buildar o docker-compose e realizar os passos iniciais de _migrate_ e _createsuperuser_ do Django.

```bash
# Utilize o docker-compose para iniciar
$ docker-compose up --build

# Migre as models
$ make migrate

# Por fim, basta criar o superuser do django
$ make superuser
```

## Criando novas models
Após a criação de uma nova model é necessário criar as migrações, o django fornece dois comandos para isso.

```bash
# Primeiro crie as migrações
$ make migrations

# Realize a migração
$ make migrate
```

## Rodando os testes
Com o objetivo de criar uma aplicação estável e correta são necessários testes, para isso será usado o _pytest_ como utilitário para execução da suite de testes.
- Obs.: O comando ja executa com a flag -s do pytest, permitindo a utilização do ipdb como breakpoint para debug.

```bash
# Executando todos os testes da aplicação
$ make test

# Selecionando um teste dentro de um módulo ou
# rodando a suite de testes de um módulo
$ make test FILE=seu/arquivo/aqui.py

# Selecionando um teste exclusivo
$ make test TEST=nomeDoSeuTesteOuClasse

# Forma mais eficiente do exemplo anterior (selecionando o arquivo daquele teste)
$ make test FILE=seu/arquivo/aqui.py TEST=nomeDoSeuTesteOuClasse
```

Para a criação de testes facilitada, estão disponíveis utilitário como:
- [Freezegun](https://github.com/spulec/freezegun): Congela o dia e a hora do código.
- [Parameterized](https://github.com/wolever/parameterized): Permite a passagem de parâmetros na chamada de um teste, podendo o mesmo ser reutilizado para diversas entradas.
- [Model-bakery](https://model-bakery.readthedocs.io/en/latest/): Permite a criação de objetos padrões para os testes, tornado os códigos mais enxutos e mais compreensíveis.
- [Mock](https://docs.python.org/3/library/unittest.html): Para mockar funções e fluxos dentro da aplicação
