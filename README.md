# Face Recognition App

## Descrição

Aplicação simples de reconhecimento facial usando OpenCV para captura e detecção de rostos. Os dados dos usuários (nome, CPF, telefone e imagem) são armazenados em um banco de dados PostgreSQL, garantindo organização e segurança.

## Requisitos

- Python 3.7-3.12
- PostgreSQL
- Dependências listadas em `requirements.txt`

## Instalação

1. Clone o repositório:

    ```
    git clone <url-do-repositorio>
    cd <nome-do-diretorio>
    ```

2. Crie um ambiente virtual (opcional, mas recomendado):

    ```
    python -m venv venv
    source venv/bin/activate  # Linux/Mac
    venv\Scripts\activate     # Windows
    ```

3. Instale as dependências:

    ```
    pip install -r requirements.txt
    ```

4. Configure o banco de dados:
    - Crie um arquivo `.env` na raiz do projeto com a variável `DATABASE_URL` apontando para o seu banco PostgreSQL:

    ```
    DATABASE_URL=postgresql://usuario:senha@host:porta/nome_do_banco?sslmode=require
    ```


## Uso

1. Execute o script `face.py`
2. Escolha uma opção:

    - **Cadastrar usuário:** Capture a imagem e insira os dados do usuário.
    - **Verificar entrada:** Verifique o rosto contra os dados cadastrados.
    - **Sair:**  Finalize a aplicação.

## Funcionalidades

- Captura de imagem via webcam.
- Detecção básica de rosto com o OpenCV.
- Armazenamento de dados (nome, CPF, telefone e imagem) diretamente no banco de dados PostgreSQL.
- Interface de linha de comando simples e direta.

## Estrutura do Banco de Dados

A tabela `usuarios` armazena os seguintes campos:

- `id`: Identificador único (chave primária).
- `nome`: Nome do usuário.
- `cpf`: CPF do usuário.
- `telefone`: Telefone do usuário.
- `imagem`: Imagem do rosto armazenada em formato binário.

## Próximos Passos

- Melhorar precisão de reconhecimento.
- Adicionar suporte a múltiplos rostos por imagem.
- Implementar autenticação mais robusta.