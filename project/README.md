# VKbot
## admin.py
### File for admins function (such as generate tokens)
## bot.py
### Main file for connect with VK
## login.py
### Autification for users and admins 
## response.py
### Simple answers and call main ML function 
## result.py - запуск цикла в котором запускается функция из true_project.py (работает пока не будет введен exit) 
### Simple example for use ML function
## tokens.py
### Tokens generate and validate (for login)
## Model files:
### test_1.py - объявление функций (нормализация, векторизация, предсказание класс, annoy, предсказание ответа), импорт обученных моделей (w2v, annoy, вектора)
### true_project.py - объявление функции, в которой осуществляется классификация и находится ответ
### anothers_files_with_data(is empty now)
## Dockerfile
### File for compile in docker
## requirements.txt
### Requirements for docker
