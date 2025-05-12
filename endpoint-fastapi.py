#Questão 4: Endpoint FastAPI com validação e UUID
#🎯 Objetivo: Código em Python com validação e geração dinâmica de campo.
#🧠 Prompt:
#Crie um endpoint em FastAPI chamado /item que receba um objeto JSON do tipo Item contendo os campos:

#nome (string, máx. 25 caracteres),

#valor (float),

#data (date, não pode ser maior que a data atual).
#O endpoint deve validar os dados e retornar o mesmo objeto com um campo adicional chamado uuid (identificador único gerado dinamicamente). O código deve estar funcional e conter comentários explicando cada parte.


#RESPOSTA:

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, validator, ValidationError
from uuid import uuid4
from datetime import date

# Inicializando a aplicação FastAPI
app = FastAPI()

# Definindo o modelo Item que será utilizado para validar os dados
class Item(BaseModel):
    nome: str  # Nome do item (máximo de 25 caracteres)
    valor: float  # Valor do item (do tipo float)
    data: date  # Data de criação do item (do tipo date)

    # Validação do campo 'nome' para garantir que não ultrapasse 25 caracteres
    @validator('nome')
    def nome_max_length(cls, v):
        if len(v) > 25:
            raise ValueError('O nome não pode ter mais de 25 caracteres')
        return v

    # Validação do campo 'data' para garantir que não seja maior que a data atual
    @validator('data')
    def data_maxima(cls, v):
        if v > date.today():
            raise ValueError('A data não pode ser maior que a data atual')
        return v

    # Gerando o 'uuid' dinamicamente no momento de resposta
    def generate_uuid(self):
        return str(uuid4())

# Criando o endpoint /item
@app.post("/item")
async def create_item(item: Item):
    try:
        # Aqui, geramos o UUID e retornamos o objeto Item com o campo adicional 'uuid'
        item_dict = item.dict()  # Convertendo o objeto 'Item' para dicionário
        item_dict['uuid'] = item.generate_uuid()  # Adicionando o campo 'uuid'
        return item_dict  # Retornando o dicionário com o UUID gerado

    except ValidationError as e:
        # Caso haja erro na validação dos dados de entrada, retornamos uma mensagem de erro
        raise HTTPException(status_code=400, detail=str(e))

# Instrução para rodar o servidor localmente:
# No terminal, execute: uvicorn <nome_do_arquivo>:app --reload


#Explicação do Código:
#FastAPI e Pydantic: A biblioteca FastAPI é usada para criar o servidor e o endpoint, enquanto o Pydantic é utilizado para validar os dados de entrada. O modelo Item é definido com o uso de Pydantic, que permite a validação de tipos de dados e a criação de validadores personalizados.

#Validação do Nome: O campo nome é validado para garantir que o tamanho não ultrapasse 25 caracteres. Caso contrário, é levantado um erro com uma mensagem apropriada.

#Validação da Data: O campo data é validado para garantir que não seja maior que a data atual. Caso a data fornecida seja futura, um erro será gerado.

#UUID Dinâmico: O campo uuid é gerado dinamicamente usando a função uuid4() da biblioteca uuid e adicionado ao dicionário de resposta antes de retorná-lo.

#Endpoint /item: O endpoint recebe um objeto JSON que corresponde ao modelo Item, realiza as validações e, se tudo estiver correto, retorna o objeto com o campo adicional uuid. Se ocorrer qualquer erro de validação, uma exceção HTTPException é gerada com o status 400 e a descrição do erro.


#Testando a API:
#Para rodar este código, salve-o em um arquivo, por exemplo, main.py, e execute o servidor FastAPI com o comando:

#uvicorn main:app --reload
#Agora, você pode acessar o endpoint através de http://127.0.0.1:8000/item e testar com requisições POST enviando um JSON válido, como este exemplo:

#{
#  "nome": "Produto Exemplo",
#  "valor": 100.5,
#  "data": "2025-05-12"
#}
#A resposta seria algo como:

#{
#  "nome": "Produto Exemplo",
#  "valor": 100.5,
#  "data": "2025-05-12",
#  "uuid": "f742dcb5-0f2d-4a9a-87ea-3e9f9cb16743"
#}