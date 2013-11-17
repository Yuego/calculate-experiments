Для запуска тестов выполните::

    tox

в корне репозитория.

Сборщик заголовков::

    grep -o -P -i '^# Calculate.*' -r /var/lib/layman/calculate/profiles/templates/3.1/* -h --color=never | sort | uniq > headers.txt


TODO: парсеры

* apache
* **bind**
* compiz
* *desktop*
* **dhcp**
* diff
* dovecot
* *ini*
* **kde**
* ldap
* **openrc**
* patch
* **plasma**
* postfix
* procmail
* **samba**
* squid
* **world**
* xml_gconf
* xml_gconf_tree
* xml_xfce
* xml_xfcepanel
