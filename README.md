# Gerenciamento de Tarefas - MongoDB

Este projeto é uma aplicação de gerenciamento de tarefas desenvolvida como parte da disciplina de Banco de Dados. O sistema permite realizar operações de CRUD (Criar, Ler, Atualizar e Deletar) em uma base de dados MongoDB, oferecendo uma interface simples para organizar atividades diárias.

O projeto foi baseado na estrutura de aprendizado do repositório [example_crud_mongo](https://github.com/howardroatti/example_crud_mongo.git).

## 📋 Funcionalidades

O sistema é capaz de realizar as seguintes operações com tarefas:
* **Criar Tarefa**: Adicionar uma nova tarefa com descrição e status.
* **Listar Tarefas**: Visualizar todas as tarefas cadastradas no banco.
* **Atualizar Tarefa**: Modificar a descrição ou o status de uma tarefa existente.
* **Deletar Tarefa**: Remover uma tarefa do banco de dados.

## 🛠️ Tecnologias Utilizadas

* **Linguagem**: Python 3.x
* **Banco de Dados**: MongoDB (Atlas ou Local)
* **Bibliotecas**:
    * `pymongo` (Driver de conexão com o MongoDB)
    * `pandas` (Opcional, para manipulação de dados, se utilizado)

## 🚀 Como Executar o Projeto

Siga os passos abaixo para configurar e rodar a aplicação em sua máquina local.

### Pré-requisitos
* Ter o [Python](https://www.python.org/) instalado.
* Ter o [Git](https://git-scm.com/) instalado.
* Ter uma instância do MongoDB rodando (localmente ou via MongoDB Atlas).

### Instalação

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/CarinedeSantana/Gerenciamento-de-Tarefas-mongoBD.git](https://github.com/CarinedeSantana/Gerenciamento-de-Tarefas-mongoBD.git)
    cd Gerenciamento-de-Tarefas-mongoBD
    ```

2.  **Crie um ambiente virtual (opcional, mas recomendado):**
    ```bash
    # No Windows
    python -m venv venv
    .\venv\Scripts\activate

    # No Linux/Mac
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```
    *(Nota: Se o arquivo requirements.txt não existir, instale manualmente o pymongo com: `pip install pymongo`)*

### Configuração do Banco de Dados

Certifique-se de configurar a string de conexão com o MongoDB no código (geralmente no arquivo de configuração ou diretamente na classe de conexão):

```python
# Exemplo de string de conexão
client = MongoClient("mongodb://localhost:27017/")
db = client["gerenciador_tarefas"]# Gerenciamento-de-Tarefas-
