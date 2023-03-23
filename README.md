# Final_progect
# pytest_ui_api_template

## Pattern for automation testing on Python

### Steps
1. Склонировать проект "git clone https://github.com/Vadimkandeev/Lesson_11.git"
2. Установитть все зависимости
3. Запустить тесты "pytest"
4. Сгенерировать отчет "allure generate allure-files -o allure-report"
5. Открыть отчет "allure open allure-report"

### Stack:
 - pytest
 - selenium
 - requests
 - _sqlalchemy_
 - allure
 - config

### Structure:
 - ./test - тесты
 - ./pages - описание страниц
 - ./api Хелперы для работы с API
 - ./db - Хелперя для работы BD
 - tast_config.ini - настройка для тестов

### Useful links
 - [Подсказки по markdown]
 - [Сгенерировать файл .gitignore]

### libraries
 - pip install pytest
 - pip install selenium
 - pip install webdriver-manager
 - pip install allure-pytest
 - pip install requests
 - pip install Faker