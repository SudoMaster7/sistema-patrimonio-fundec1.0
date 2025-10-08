# Sistema de Gerenciamento de Patrimônio - SUDO / FUNDEC

![Status](https://img.shields.io/badge/status-em%20desenvolvimento-yellow)
![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![Flask](https://img.shields.io/badge/Flask-2.2-black?logo=flask)
![Vercel](https://img.shields.io/badge/Deploy-Vercel-black?logo=vercel)

Uma aplicação web simples e eficiente desenvolvida pela **SUDO** para a **FUNDEC**, com o objetivo de catalogar e gerenciar o patrimônio de equipamentos eletrônicos. O sistema utiliza uma interface limpa, se conecta a uma Planilha Google para armazenamento de dados em tempo real e está publicado na Vercel para acesso remoto.

**➡️ [Acesse a aplicação aqui!](https://sistema-patrimonio-fundec1-0.vercel.app/)** ---

## ✨ Funcionalidades

* **Formulário de Cadastro Intuitivo:** Interface simples para a captura de novos equipamentos.
* **Registro em Lote:** Capacidade de adicionar múltiplos itens similares de uma só vez, com números de série únicos ou idênticos.
* **Visualização e Edição:** Uma tabela exibe os últimos itens cadastrados, permitindo a edição rápida de qualquer informação incorreta.
* **Armazenamento em Tempo Real:** Todos os dados são salvos instantaneamente em uma Planilha Google, facilitando o acesso e a manipulação externa.
* **Tema Claro e Escuro:** Um seletor de tema para melhorar o conforto visual e a acessibilidade.
* **Design Responsivo:** Acessível e funcional em desktops, tablets e celulares.

---

## 🚀 Tecnologias Utilizadas

* **Backend:** Python 3, Flask
* **Frontend:** HTML5, CSS3, Bootstrap 5, JavaScript
* **Base de Dados:** Google Sheets API
* **Deploy:** Vercel, Git, GitHub

---

## 🔧 Rodando o Projeto Localmente

Siga os passos abaixo para configurar e rodar o projeto na sua máquina local.

#### **Pré-requisitos**

* Python 3.8+
* Git

#### **Instalação**

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/SudoMaster7/sistema-patrimonio-fundec1.0.git](https://github.com/SudoMaster7/sistema-patrimonio-fundec1.0.git)
    cd sistema-patrimonio-fundec1.0
    ```

2.  **Crie e ative um ambiente virtual:**
    ```bash
    # Para Windows
    python -m venv .venv
    .\.venv\Scripts\activate

    # Para macOS/Linux
    python3 -m venv .venv
    source .venv/bin/activate
    ```

3.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

#### **🔑 Configuração**

Para que a aplicação se comunique com o Google Sheets, são necessárias as credenciais da API do Google Cloud.

1.  Siga um tutorial para criar uma **Conta de Serviço** no Google Cloud e ative as APIs **Google Drive** e **Google Sheets**.
2.  Baixe o arquivo JSON de credenciais.
3.  **Para desenvolvimento local:** Renomeie o arquivo para `credentials.json` e coloque-o na raiz do projeto.
4.  **Para deploy na Vercel:** Não inclua o arquivo! Em vez disso, copie todo o conteúdo do JSON e crie uma variável de ambiente no painel da Vercel chamada `GOOGLE_CREDENTIALS_JSON` com esse conteúdo.
5.  **Compartilhe sua Planilha Google** com o email encontrado no campo `client_email` do seu arquivo JSON, dando a ele permissão de **Editor**.

#### **Execução**

Após a configuração, inicie o servidor Flask:
```bash
flask run
```
A aplicação estará disponível em `http://127.0.0.1:5000`.

---

## ☁️ Deploy

Este projeto está configurado para deploy contínuo na Vercel. Qualquer `push` para a branch `main` no GitHub iniciará um novo build e deploy automaticamente.

---

## 👨‍💻 Autor

Desenvolvido por **[SudoMaster7](https://github.com/SudoMaster7)**.
