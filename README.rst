Для запуска тестов выполните::

    tox

в корне репозитория.

Сборщик заголовков::

    grep -o -P -i '^# Calculate.*' -r /var/lib/layman/calculate/profiles/templates/3.1/* -h --color=never | sort | uniq > headers.txt


