# test_storage

## Проверка
____
Для проверки работоспособности сервиса, необходимо закомментировать строки: `21 - 24`.

## Недостатки
____
- Создается zip архив, когда он не нужен
- Из storage удаляются только директории дней, а директории месяцев могут остаться пустыми

## Возможные доработки
____
- Добавить функционал с crontab
- Добавить параметризацию при помощи argparse, куда передавать пути до storage и archive + установить значения по умолчанию
