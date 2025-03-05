# tenderplan-test

<!-- PROJECT LOGO -->
<div align="center">
  <h2>tenderplan-test</h2>

  <h3 align="center">README тестового задания</h3>

  <p align="center">
    Парсер сайта государственных закупок (ЕИС), главной страницы поиска тендеров
  </p>
</div>

<a name="readme-top"></a>

<hr>

<!-- ABOUT THE PROJECT -->
## About The Project

Требования:
* Нужно реализовать программу на Python, которая обходит первые две страницы по
44ФЗ на сайте государственных закупок (ЕИС)
* При обходе, у каждого элемента списка (тендера), нужно собирать ссылку на его
печатную форму
* Получить ссылку на печатную XML-форму
* Распарсив этот XML, для каждого тендера нужно получить значение XML-поля publishDTInEIS, или None в случае его отсутствия.
* Результат вывести прямо в консоль, в виде пары “ссылка на печатную форму”-”дата публикации”
* Рекомендуемый стек:
  - Python3
  - пакет Requests
  - пакет BeautifulSoup
  - пакет XmlToDict
* Основной трудный момент этого тестового задания - нужно распараллелить задачи обхода списка и парсинга XML-форм,
разбить написанный выше скрипт на отдельные таски. Для этого нужно использовать пакет Celery.
Рекомендуемая разбивка на (асинхронные) подзадачи:
  - сбор ссылок с каждой страницы - отдельный таск (для каждой страницы)
  - парсинг печатных XML-форм - отдельный таск (для каждой формы)


<!-- GETTING STARTED -->
## Getting Started

### Prerequisites

Copy project to repository on local machine (HTTPS or SSH)
  ```sh
  git clone https://github.com/SuperLalka/tenderplan-test.git
  ```
  ```sh
  git clone git@github.com:SuperLalka/tenderplan-test.git
  ```

### Installation

Для запуска проекта достаточно собрать и запустить контейнеры Docker.

```sh
docker-compose -f docker-compose.yml up -d --build
```

Запуск тестов:

```sh
sh start_tests.sh
```