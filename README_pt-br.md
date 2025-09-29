# Configuração do Ambiente de Desenvolvimento

Para garantir a portabilidade e evitar conflitos de dependência, este projeto utiliza um ambiente virtual em Python. Siga os passos abaixo para configurar seu ambiente de desenvolvimento.

## Passo 1: Criar e Ativar o Ambiente Virtual

Navegue até o diretório raiz do projeto e crie o ambiente virtual executando o comando a seguir:

```json
python -m venv venv
```

Em seguida, ative-o com o comando apropriado para o seu sistema operacional:

#### Para macOS/Linux:

```json
source venv/bin/activate
```

#### Para Windows

- **Prompt de Comando)**:

```json
venv\Scripts\activate
```

- **PowerShell**:

```json
.\venv\Scripts\activate
```

_Se você estiver usando o Git Bash ou outro terminal no estilo Linux no Windows, use o comando para macOS/Linux._

---

## Passo 2: Instalar as Dependências

Com o ambiente virtual ativado, instale todas as bibliotecas necessárias listadas no arquivo `requirements.txt` usando `pip`.

```json
pip install -r requirements.txt
```

Após isso, será necessário instalar as dependências do front-end, presentes no arquivo `package.json`, utilizando o seguinte comando:

```json
npm install
```

Pronto. O ambiente de desenvolvimento está configurado e pronto para uso.

---

## Passo 3: Inicialização do Banco de Dados

Antes de iniciar a aplicação, você deve configurar o banco de dados. Este projeto usa o PostgreSQL e o Flask CLI para criar as tabelas a partir dos modelos Python.

#### Pré-requisitos:

- Certifique-se de que o servidor `PostgreSQL` está rodando.
- Garanta que o banco de dados (o nome definido em `DATABASE_URL` no seu arquivo `.env`) já foi criado no seu PostgreSQL.

### 3.1 Criação do Banco de Dados Local (PostgreSQL):

Se você não tem o banco de dados principal criado, siga estas instruções no seu terminal.

- **Passo a Passo via Terminal**:

---> **Acesse o Terminal do PostgreSQL (psql):**

```json
psql -U postgres
```

O sistema pedirá a senha do seu usuário postgres.

---> **Crie o Banco de Dados:**

```json
CREATE DATABASE finance_db;
```

---> **Crie o Usuário do Banco (Opcional, mas Recomendado):**

```json
CREATE USER nome_do_seu_usuario WITH PASSWORD 'sua_senha_secreta';
```

---> **Conceda Permissões Essenciais ao Usuário:**

Estes comandos são cruciais para permitir que o usuário crie tabelas e sequências no esquema `public`.

---- **1. Permissão básica de conexão e uso do banco:**

```json
GRANT ALL PRIVILEGES ON DATABASE finance_db TO nome_do_seu_usuario;
```

---- **2. Conecte-se ao novo banco para dar permissões de esquema:**

```json
\c finance_db;
```

---- **3. Permissão para criar tabelas no esquema padrão 'public':**

```json
GRANT ALL ON SCHEMA public TO nome_do_seu_usuario;
```

---- **4. Garante que qualquer TABELA ou SEQUÊNCIA criada FUTURAMENTE neste esquema também pertença a este usuário:**

```json
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO nome_do_seu_usuario;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO nome_do_seu_usuario;
```

Substitua `nome_do_seu_usuario` pelo usuário real que está no seu `.env`.

---> **Saia do psql:**

```json
\q
```

- **Ajuste Final no .env**:

Após criar o usuário e o banco de dados, certifique-se de que seu arquivo `.env` usa exatamente esses valores.

---- **Exemplo de como deve ficar após a criação:**

```json
DATABASE_URL='postgresql://nome_do_seu_usuario:sua_senha_secreta@localhost:5432/finance_db'
```

Com o banco de dados criado e o .env ajustado, seu backend está pronto para a conexão!

### 3.2 Passos para Criar as Tabelas

Siga estes passos na raiz do seu projeto:

- **Ative o Ambiente Virtual (venv)**:

É crucial que o ambiente virtual esteja ativo para que o comando flask funcione corretamente. Caso não tenha ativado ainda, verifique o `Passo 1: Criar e Ativar o Ambiente Virtual`.

- **Execute o Comando de Criação**:

Rode o comando `flask create-tables` que foi configurado no arquivo `create_db.py`.

```json
flask create-tables
```

O sistema irá se conectar ao PostgreSQL e criar as tabelas `User, Transaction, Category` e `Budget`.

- **Opção: Limpar e Recriar as Tabelas:**

Se você precisar apagar todos os dados e recriar as tabelas do zero (útil durante o desenvolvimento e testes), utilize a flag `--drop`:

```json
flask create-tables --drop
```

ATENÇÃO: Este comando irá **DELETAR IRREVERSIVELMENTE** todos os dados existentes nas tabelas. _Use com cautela!_

---
