# Projeto Blog 

Este é o blog que foi criado no curso de Python de Luiz Otávio Miranda

## Criando um projeto Django


```
python -m venv venv
activate 
pip install django
django-admin startproject project .
python manage.py runserver
```


## Gerando chave secreta para o arquivo .env

Podemos utilizar o seguinte script Python para gerar uma sequência aleatória de caracteres para preencher o valor da 'SECRET_KEY' no arquivo '.env', na máquina local:

```python
import string as s
from secrets import SystemRandom as SR

print(''.join(SR().choices(s.ascii_letters+s.digits+s.punctuation, k=64)))
```

Ou podemos usar o seguinte comando no terminal:

```
python -c "import string as s;from secrets import SystemRandom as SR;print(''.join(SR().choices(s.ascii_letters+s.digits+s.punctuation, k=64)));"
```
