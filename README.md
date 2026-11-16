
# Sistema de Gerenciamento de um Café

## Descrição
Sistema web para gerenciamento de produtos de um café,
permitindo cadastrar, listar, editar e excluir produtos.

## Tecnologias utilizadas
- Python
- Flask
- SQLite
- HTML, CSS e JavaScript

## Banco de dados
Foi escolhido o SQLite por ser um banco de dados
relacional, simples e adequado para projetos pequenos.

A tabela produtos contém:
- id
- nome
- categoria
- preco
- estoque

O banco é criado automaticamente ao iniciar o servidor
pela primeira vez, com 10 produtos iniciais.

Limitações: o sistema não possui autenticação e utiliza
um banco de dados local.

## Como executar
1. Instalar Python.
2. Abrir a pasta do projeto no terminal.
3. Executar:
   python -m pip install -r requirements.txt
4. Executar:
   python app.py
5. Abrir no navegador:
   http://127.0.0.1:5000

## Rotas da API
GET /api/produtos - Listar produtos
POST /api/produtos - Cadastrar produto
PUT /api/produtos/:id - Editar produto
DELETE /api/produtos/:id - Excluir produto

## Uso de inteligência artificial
O ChatGPT foi utilizado como apoio na estruturação
do projeto, na elaboração do código e nas orientações
de implementação e testes.
