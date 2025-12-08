CupcakeApp

Sistema de e-commerce para venda de cupcakes, desenvolvido como parte do **Projeto Integrador Transdisciplinar II (PIT-II)** do curso de Sistemas de Informação.

O projeto segue a arquitetura **MVC (Model-View-Controller)** e utiliza **Python com Flask** no backend.

Funcionalidades

* **Catálogo de Produtos:** Visualização de cupcakes disponíveis com filtros visuais.
* **Sistema de Autenticação:** Cadastro e Login de usuários.
* **Carrinho de Compras:** Adicionar itens, alterar quantidades e remover produtos.
* **Painel Administrativo:** Cadastro de novos produtos com **upload de fotos**.
* **Persistência de Dados:** Banco de dados relacional (SQLite/SQLAlchemy).
* **Interface Responsiva:** Design adaptável para mobile usando Bootstrap 5.

Tecnologias Utilizadas

* **Linguagem:** Python 3.x
* **Framework Web:** Flask
* **ORM (Banco de Dados):** Flask-SQLAlchemy
* **Frontend:** HTML5, CSS3, Jinja2, Bootstrap 5
* **Banco de Dados:** SQLite (padrão do projeto)

Estrutura do Projeto (MVC)

O projeto foi organizado seguindo rigorosamente o padrão de arquitetura de software MVC:

```text
projeto-cupcake/
│
├── docs/                  # Documentação do projeto (PDFs, Diagramas)
├── src/                   # Código Fonte Principal
│   ├── app.py             # Ponto de entrada (Inicialização e Configuração)
│   ├── models/            # [MODEL] Definição das tabelas do Banco de Dados
│   │   └── database.py
│   ├── controllers/       # [CONTROLLER] Lógica de rotas e regras de negócio
│   │   └── routes.py
│   └── views/             # [VIEW] Interface do usuário
│       ├── static/        # Arquivos estáticos (CSS, Imagens, Uploads)
│       └── templates/     # Arquivos HTML
│
└── requirements.txt       # Dependências do projeto
