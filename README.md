# 📌 Rede Social Winx

Aplicação acadêmica desenvolvida para simular uma rede social, com funcionalidades de CRUD, consultas SQL avançadas e visualização de dados através de gráficos. O projeto tem como objetivo aplicar conceitos de modelagem de banco de dados, integração com Python e análise visual de informações.

---

## 📖 Sobre o Projeto

A **Rede Social Winx** foi criada como parte de um trabalho acadêmico na disciplina de Banco de Dados.  
O sistema possibilita:

- Inserção, atualização, exclusão e consulta de dados.
- Execução de consultas SQL otimizadas para análise da base.
- Geração de gráficos para interpretação visual dos dados.

---

## 🛠 Tecnologias Utilizadas

- **Python 3.10+** – Linguagem principal do projeto.
- **SQLAlchemy** – Mapeamento objeto-relacional (ORM).
- **PostgreSQL** – Banco de dados relacional utilizado.
- **Matplotlib** – Criação de gráficos para visualização dos dados.
- **Faker** – Geração de dados fictícios para testes.
- **Questionary** – Interface de linha de comando interativa.

---

## 📂 Estrutura do Projeto

```
ProjetoFinal/
├── app/
│   └── main.py              # Arquivo principal da aplicação
├── db/
│   ├── connection.py        # Conexão com o banco de dados
│   └── init_db.py           # Inicialização e reset da base
├── models/
│   └── models.py            # Definição das entidades e relacionamentos
├── services/
│   ├── inserir_registros.py
│   ├── apagar_registros.py
│   ├── consultar_registros.py
│   └── atualizar_registros.py
├── utils/
│   └── helpers.py           # Funções auxiliares
├── requirements.txt         # Dependências do projeto
├── run.sh                   # Script para execução em Linux/macOS
├── run.bat                  # Script para execução no Windows
└── README.md
```

---

## 🚀 Como Executar

### No Linux/macOS:

```bash
./run.sh
```

### No Windows:

```bat
run.bat
```

Os scripts realizam:
1. Criação e ativação de ambiente virtual.  
2. Instalação das dependências listadas em `requirements.txt`.  
3. Inicialização do projeto com `python -m app.main`.  

---

## 📊 Consultas e Relatórios

O sistema possui consultas SQL pré-configuradas para análise dos dados, com geração de gráficos utilizando `Matplotlib` para melhor visualização dos resultados obtidos.

---

## 👨‍💻 Autor

Desenvolvido por **Ian Andriani Gonçalves** como parte de atividade acadêmica na disciplina de Banco de Dados, com foco em aplicar conceitos de modelagem, integração Python-SQL e visualização de dados.

---

## 📜 Licença

Distribuído sob a licença MIT. Consulte o arquivo `LICENSE` para mais detalhes.
