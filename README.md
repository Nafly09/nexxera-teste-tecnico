## <b> 🖥 Nexxera-Accounts </b>

## <b> 🛠 Tecnologias utilizadas </b>

#### Framework

- Django

#### Bibliotecas

- python-dotenv
- djangorestframework
- coverage

<br>

## 🛠 Organização para ambiente do projeto

<p>Caso queira fazer uma clonagem e rodar o processo na sua máquina siga as seguintes instruções:</p>

1 - Inicie um ambiente virtual (<code>venv</code>) no seu projeto:

```sh
$ python -m venv venv && source venv/bin/activate
```

2 - Instale as dependências presentes no arquivo <code>requirements.txt</code> com o seguinte comando no terminal:
<br>

```
$ pip install -r requirements.txt
```

4 - Verifique as variáveis de ambientes de configuração necessárias no arquivo <code>.env.example</code>, crie uma cópia desse arquivo preencha as chaves necessárias e nomeie-o <code>.env</code>

3 - Em seguida, inicie a aplicação django rodando o seguinte comando no terminal:
<br>

```
$ ./manage.py runserver
```

<hr>
<br>

## 🛠 Organização para ambiente de produção
<p>Caso tenha apenas interesse em utilizar a api, ela está disponibilizada para ser utilizado em um servidor heroku, segue o endpoint público para utilização:</p>
<b>nexxera-accounts.herokuapp.com/</b>
<br>
<p>Divirta-se</p>

## <b> 🔚 Endpoints </b>

<br>

## <b> > Contas </b>

<br>

### <b> Registro </b>

<i> POST /api/accounts/ </i>

<br>

Você pode passar a chave balance com um valor para definir um saldo inicial para a conta. Caso não informado o valor padrão será de 0.

```json
{
	"account_owner": "Erwin Smith"
}
```

Dessa requisição é esperado um retorno com os dados do usuário cadastrado, como mostrado a seguir:

```json
{
	"account_id": "ebad0eab-4100-4cea-a63d-ee48f8b44cf7",
	"account_owner": "Erwin Smith",
	"balance": 0.0
}
```

<br>

### <b> Listagem </b>

<i> GET /api/accounts/ </i>

<br>

Esta rota retornará todos os dados de todas as contas registradas. Por pedido da equipe, nessa primeira versão não haverá autenticação por JWT ou similares.

<br>

```json
[
	{
		"account_id": "f997561c-0996-4fff-92f8-7668a5ca6098",
		"account_owner": "Jane Doe",
		"balance": 0.0
	},
	{
		"account_id": "7e69c0cc-71c3-42a5-901e-4525682656f7",
		"account_owner": "Smith Doe",
		"balance": 150.0
	},
	{
		"account_id": "ebad0eab-4100-4cea-a63d-ee48f8b44cf7",
		"account_owner": "Erwin Smith",
		"balance": 100.0
	}
]
```

<br>

### <b> Atualizar saldo </b>

<i> PATCH /api/accounts/<transaction_type>/<account_id>/</i>

<br>

Essa rota recebe dois parâmetros sendo eles:
  
  <br>
  
  - <b>transaction_type</b>: Nesse parâmetro você tem 2 opções para escolher, crédito ou débito. Crédito para adicionar saldo em conta e débito para retirar o saldo em conta.
  - <b>account_id</b>: Nesse parâmetro você deve informar o ID da conta na qual você deseja fazer a transação. Você também pode passar na requisição a chave description e adicionar uma descrição á transação para organizar melhor, porém ela é opcional e caso não informado é retornado apenas uma string vazia.
  <br>
  
```json
{
	"balance": 50,
	"transaction_description": "Pix da firma"
}
```
<br>
  
Após a requisição você deve receber um retorno com os dados da conta com o ID informado e seu saldo atualizado.

<br>
  
```json
{
	"account_id": "ebad0eab-4100-4cea-a63d-ee48f8b44cf7",
	"account_owner": "Erwin Smith",
	"balance": 100.0
}
```
<br>
  
### <b> Retirar extrato </b>

<i> GET /api/extracts/<account_id>/?transaction_type=credit/debit

<br>

Essa rota recebe um parâmetros e tem a possibilidade de receber um query param também, sendo eles:
  
  <br>
  
  - <b>transaction_type</b>: Nesse parâmetro você tem 2 opções para escolher, crédito ou débito. Crédito para filtrar os dados do extrato apenas por crédito e débito para filtrar os dados do extrato apenas por débito
  - <b>account_id</b>: Nesse parâmetro você deve informar o ID da conta na qual você deseja fazer a transação.
  <br>
  
Após a requisição você deve receber um retorno com os dados do extrato da conta com o ID informado. Caso não tenha passado o query param opcional você receberá o extrato com todas as transações da conta no período.

<br>
  
```json
{
	"extract_id": "a4de9ac9-0272-48f2-8c6b-39abd0eb060f",
	"extract_date": "2022-06-09 12:26:07.642150+00:00",
	"former_account_balance": 50.0,
	"current_account_balance": 100.0,
	"transactions": [
		{
			"transaction_id": "1d472b5a-6280-4ae2-bbf7-ad5f3e75afb1",
			"transaction_type": "debit",
			"transaction_value": 50.0,
			"transaction_date": "2022-06-09 12:25:59.606218+00:00",
			"transaction_description": ""
		},
		{
			"transaction_id": "4615086b-1843-4565-b550-d58ba2c28569",
			"transaction_type": "credit",
			"transaction_value": 50.0,
			"transaction_date": "2022-06-09 12:26:05.300466+00:00",
			"transaction_description": ""
		},
		{
			"transaction_id": "eba74f69-079d-4286-92e4-4cd17d19e49b",
			"transaction_type": "credit",
			"transaction_value": 50.0,
			"transaction_date": "2022-06-09 12:26:06.416240+00:00",
			"transaction_description": ""
		},
		{
			"transaction_id": "d20bf7f3-73cd-4420-8571-bd4aa6dc20ce",
			"transaction_type": "credit",
			"transaction_value": 50.0,
			"transaction_date": "2022-06-09 12:26:07.652896+00:00",
			"transaction_description": ""
		}
	]
}
```

## 🛠 Organização para ambiente de testes do projeto

<p>Caso queira rodar os testes na sua máquina local, certifique-se de ter todas as dependências e siga os próximos passos:</p>

1 - Rode os testes utilizando o coverage para gerar um relatório.:

```sh
$ coverage run ./manage.py test
```
2 - Após isso rode o seguinte comando no terminal para gerar o relatório escrito para resultado dos testes e cobertura de código.

```sh
$ coverage report > report.txt
```
<i>Caso tudo tenha dado certo você terá visto um OK no terminal sinalizando que todos os testes passaram e terá um arquivo report.txt na raiz do projeto com os dados de coverage do código com o testes.<i/>



