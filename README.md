secretstash
===========

An application and API for stashing credentials -- Mostly for devops usage

```
python manage.py syncdb --noinput --settings secretstash.settings.local

python manage.py schemamigration secrets --initial --settings secretstash.settings.local
python manage.py migrate secrets --fake --settings secretstash.settings.local
python manage.py migrate secrets --settings secretstash.settings.local

python manage.py createsuperuser --settings secretstash.settings.local
```