# Якут


## Установка
- #### Клонировать репозиторий и перейти в него в командной строке:

  ```shell
  git clone 
  ```

  ```shell
  cd yacut
  ```

- #### Создать и активировать виртуальное окружение:

  ```shell
  python3 -m venv venv
  ```

  - Если у вас Linux/macOS

    ```shell
    source venv/bin/activate
    ```

  * Если у вас windows

    ```commandline
    venv/scripts/Activate
    ```

- #### Установить зависимости из файла requirements.txt:

  ```shell
  python3 -m pip install --upgrade pip
  ```
  
  ```shell
  pip install -r requirements.txt
  ```
  
## Запуск
Рекомендуется использвать wsgi сервер. В пакете yacut для его запуска есть приложение app. Но можно запустить отладочный сервер Flask.
```shell
python run.py
```

## Используется
- Python
- Flask
  - SQLAlchemy
  - WTForms

## Структура проекта

![](https://github.com/Raidzin/yacut/blob/master/graphviz.svg?raw=true)

использован инструмент [Pylint](https://pylint.pycqa.org/en/latest/pyreverse.html)

## Разработчик
                            
- [Raidzin](https://github.com/Raidzin "github.com/Raidzin")