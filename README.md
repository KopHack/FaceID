# FaceID

Demonstration: http://gosuclygi.site/

![image](https://user-images.githubusercontent.com/72864649/186428306-01e12c43-9e88-45d3-bddb-0883969e1760.png)

Также алгоритму не страшны аксессуары на лице, маски, очки.
![image](https://user-images.githubusercontent.com/72864649/186429111-5a626e84-7579-4289-bcbc-fd6e436bba69.png)

# Настройка
Для начало необходимо настроить среду в которой будет производится работа. Для этого на сервер нужно установить все необходимые инструменты, язык программирования, фреймворк, библиотеки и настроить связи между ними. 

### Этап 1. Установка Python

Для установки Python, необходимо перейти в виртуальное окружение Doker, следующей командой:

  o1233239@furs3:~ [0] $ ssh localhost -p222
  
Далее нужно создать временный каталог и перейти в него, используя следующие команды:

(docker) o1233239@furs3:~ [0] $ mkdir -p ~/.beget/tmp && cd ~/.beget/tmp/ 

Для Python версии 3.7 нужно собрать библиотеку ffi, следующей командой: 

(docker) o1233239@furs3:~/.beget/tmp [0] $ wget ftp://sourceware.org/pub/libffi/libffi-3.2.1.tar.gz

После того как архив с библиотекой ffi скачался, его необходимо распаковать, а также перейдём в каталог с исходным кодом следующими командами:

(docker) o1233239@furs3:~/.beget/tmp [0] $ tar -xf libffi-3.2.1.tar.gz && cd libffi-3.2.1

Утилита configure настроит все зависимости, префиксы, переменные, далее сгенерируем Makefile:

(docker) o1233239@furs3:~/.beget/tmp/libffi-3.2.1 [0] $ ./configure --prefix $HOME/.local LDFLAGS="-L/usr/local/lib"

В директории libffi-3.2.1/x86_64-unknown-linux-gnu/include создадим два файла: ffi.h и ffitarget.h. И копируем их в ~/.local/include:

(docker) o1233239@furs3:~/.beget/tmp/libffi-3.2.1 [0] $ mkdir -p ~/.local/include

(docker) o1233239@furs3:~/.beget/tmp/libffi-3.2.1 [0] $ cp x86_64-unknown-linux-gnu/include/ffi.h ~/.local/include/

(docker) o1233239@furs3:~/.beget/tmp/libffi-3.2.1 [0] $ cp x86_64-unknown-linux-gnu/include/ffitarget.h ~/.local/include/

Теперь устанавливаем Python версии 3.7.0:

(docker) o1233239@furs3:~ [0] $ cd ~/.beget/tmp

(docker) o1233239@furs3:~/.beget/tmp [0] $ wget https://www.python.org/ftp/python/3.7.0/Python-3.7.0.tgz

Далее разархивируем архив и переходим в каталог с исходным кодом:

(docker) o1233239@furs3:~/.beget/tmp [0] $ tar -xf Python-3.7.0.tgz && cd Python-3.7.0

Утилита configure настроит все зависимости, префиксы, переменные, далее сгенерируем Makefile:

(docker) o1233239@furs3:~/.beget/tmp/Python-3.7.0 [0] $ ./configure --prefix=$HOME/.local LDFLAGS="-L/usr/local/lib"

Следующие команды запускают процессы компиляции и установки:

(docker) o1233239@furs3:~/.beget/tmp/Python-3.7.0 [0] $ make -j33 && make install

Python установлен на сервер по пути ~/.local/bin/python3.7, а его стандартные библиотеки по пути ~/.local/lib/python3.7. Также был установлен пакетный менеджер pip.

### Этап 2. Установка Django

Django как и сам Python можно было установить в отдельное виртуальное окружение, чтобы они были видны только одному сайту. Но было решено устанавливать их локально.  
Для установки Django нужно ввести следующую команду:

(docker) o1233239@furs3:~/gosuclygi.site [0] $ pip3 install django

При этом необходимо использовать пакетный менеджер pip3 вместо pip. Это связано с тем, что pip3 используется для третьей версии Python, то есть для всех версий Python 3.*.
После установки Django, нужно создать проект, который будет объединять создаваемые в дальнейшем приложения, которые в свою очередь будут выполнять подзадачи, и являться основой всего проекта на Django. Для создания проекта нужно ввести команду:

(docker) o1233239@furs3:~/gosuclygi.site [0] $ django-admin.py startproject PytonSite

Теперь в дирректории ~/gosuclygi.site необходимо создать файл passenger_wsgi.py. Здесь путь /home/o/o1233239/gosuclygi.site/PytonSite - это путь к проекту, а  путь к Django /home/o/o1233239/.local/lib/python3.7/site-packages. 

Далее в файле, по пути ~gosuclygi.site/PytonSite/PytonSite/setting.py необходимо в список ALLOWED_HOSTS указать разрешённые домены на котором будет работать сайт.

ALLOWED_HOSTS = ['gosuclygi.site', 'www.gosuclygi.site'] 

А так же в этом же файле запишим настройки для подключения к базе данных MySQL:
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'o1233239_dataset',
        'USER': 'o1233239_dataset',
        'PASSWORD': 'dfger456%#',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}

И ещё в этом файле добавим две переменные:

BASE_DIR_IMAGE = f'/home/o/o1233239/gosuclygi.site/PytonSite/Algoritm/static/image/'

DIR_IMAGE = f'/home/o/o1233239/gosuclygi.site/public_html/image/'

Затем в папке gosuclygi.site/public_html необходимо создать файл .htaccess:
PassengerEnabled On
PassengerPython /home/o/o1233239/.local/bin/python3.7

Где /home/o/o1233239/.local/bin/python3.7 - это путь до Python.

Когда пользователь обращается к сайту, первым делом проверяется этот файл, если он существует. Далее система понимает, что сайт будет использовать Python, поэтому в корневой папке сайта происходит поиск файла passenger_wsgi.py, который указывает путь на Django и какой проект использовать для работы сайта. Далее уже, считывай настройки проекта, загружается сайт, используя написанные приложения.
Для того, чтобы сервер перезагружался и видел внесённые изменения, необходимо создать файл restart.txt в папке tmp. Используем следующую команду:

(docker) o1233239@furs3:~/gosuclygi.site [0] $ mkdir tmp; touch tmp/restart.txt

Далее создадим приложение под названием Algoritm в нашем проекте. Для этого воспользуемся командой:

(docker) o1233239@furs3:~/gosuclygi.site/PytonSite [0] $ pyton manage.py startapp Algoritm

### Этап 3. Установка необходимых библиотек и настройка зависимостей

Для установки библиотек, создадим файл requirements.txt со следующим содержимым:
face-recognition==0.3.0
opencv-python-headless==4.5.5.64
mysql-connector-python==8.0.29

В данном файле описаны библиотеки и их версии. Следующая команда запустит процесс их установки:

(docker) o1233239@furs3:~ [0] $ cat requirements.txt

Библиотека face-recognition позволит находить области лица и формировать вектора черт лица.
С OpenCV будем открывать, преобразовывать и сохранять изображения.
Библиотека mysql-connector поможет работать с базой данных.

