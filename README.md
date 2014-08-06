secretstash
===========

An application and API for stashing credentials -- Mostly for devops usage  


Setup
=========
Run this as a normal Django application. Change secretstash/settings for settings that suit your environments. Chef/Ansible recipes coming for autoconfig.  

```
python manage.py syncdb --noinput --settings secretstash.settings.local

python manage.py schemamigration secrets --initial --settings secretstash.settings.local
python manage.py migrate secrets --fake --settings secretstash.settings.local
python manage.py migrate secrets --settings secretstash.settings.local

python manage.py createsuperuser --settings secretstash.settings.local
python manage.py runserver --settings secretstash.settings.local
```

Then in the django admin (http://host:port/admin), add some users and some groups. You can also add users through the oauth system.

Some commands to run
===========
Adding secrets -- This one adds a secret called aws_key_s3_bucket1 to your stash. Allows for group "webservers" to access.  

```
curl -X POST -H 'Accept: application/json;indent=4' -H 'Content-Type:application/json' -u username:password -d '{"groups":["webservers"],"description":"AWS key for bucket1 r/w access","content":"AKIAasdfasdf","name":"aws_key_s3_bucket1"}' http://127.0.0.1:8000/secrets/api/secret/

{
    "id": 15, 
    "owner": {
        "id": 4, 
        "username": "asdf", 
        "first_name": "", 
        "last_name": "", 
        "email": ""
    }, 
    "name": "aws_key_s3_bucket1", 
    "description": "AWS key for bucket1 r/w access", 
    "content": "AKIAasdfasdf"
}
```

Getting secrets
```
curl -X GET -H 'Accept: application/json;indent=4'  -u username:password http://127.0.0.1:8000/secrets/api/secret/?name=aws_key_s3_bucket1
[
    {
        "id": 15, 
        "owner": {
            "id": 4, 
            "username": "asdf", 
            "first_name": "", 
            "last_name": "", 
            "email": ""
        }, 
        "name": "aws_key_s3_bucket1", 
        "description": "AWS key for bucket1 r/w access", 
        "content": "AKIAasdfasdf"
    }
]
```

Or  

```
curl -X GET -H 'Accept: application/json;indent=4'  -u username:password http://127.0.0.1:8000/secrets/api/secret/15/                     
{
    "id": 15, 
    "owner": {
        "id": 4, 
        "username": "asdf", 
        "first_name": "", 
        "last_name": "", 
        "email": ""
    }, 
    "name": "aws_key_s3_bucket1", 
    "description": "AWS key for bucket1 r/w access", 
    "content": "AKIAasdfasdf"
}
```

DevOps
=============
Use something like CloudFormation to start up a machine with your SecretStash u/p as parameters in your CF script (or entered at deploytime). Then, during your initial bootstrapping (userdata in CF):
```
curl -X POST -H 'Accept: application/json;indent=4' -H 'Content-Type:application/json' -u username:password http://127.0.0.1:8000/secrets/api/host/   -d '{"name":"random_host_name"}'
{
    "owner": {
        "id": 6, 
        "username": "random_host_name", 
        "first_name": "", 
        "last_name": "", 
        "email": "random_host_name@randomhost.com"
    }, 
    "apikey": {
        "key": "0fcb68b99bd66737d0b9fb1e23913c202dab56f6"
    }, 
    "name": "random_host_name", 
    "id": 2
}

curl -X PUT -H 'Accept: application/json;indent=4' -H 'Content-Type:application/json' -u username:password -d '{"groups":["webserver"],"action":"add"}' http://127.0.0.1:8000/secrets/usergroup/random_host_name/
{
    "groups": [
        "webserver"
    ], 
    "action": "add"
}
```
We just added a "host-as-user" to the system and then added that user to the "webserver" group.  

IMPORTANT! Stash that apikey somewhere. That's how your scripts (chef or ansible or whatever) will access the SecretStash without your credentials. These are meant to be credentials just for an ephemeral host that can be destroyed after the fact.  

If you're going to access secrets from scripts after a host has been registered:  
```
curl -X GET -H 'Authorization: Token 0fcb68b99bd66737d0b9fb1e23913c202dab56f6' -H 'Accept: application/json;indent=4'  http://127.0.0.1:8000/secretsapi/secret/12/
{
    "id": 12, 
    "owner": {
        "id": 4, 
        "username": "asdf", 
        "first_name": "", 
        "last_name": "", 
        "email": ""
    }, 
    "name": "tttttttttttestt", 
    "description": "add", 
    "content": "test2"
}
```
