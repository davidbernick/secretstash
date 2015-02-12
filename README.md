secretstash
===========

An application and API for stashing credentials -- Mostly for devops usage.  

Putting credentials, secrets and more in code and in github is bad. So run your own server that let's multiple levels of users and hosts have access to only what they need. 

Using SecretStash, the only credential you'll need is what's in your head -- a username and password to the secretstash system. That u/p does not have to be stored anywhere. You can enter it at "deploytime" in CloudFormation or Heat scripts using their parameter functions. Your bootstrapping scripts can call those parameters and the machine gets it's own temporary SecretStash key to access secrets.  

But what about Databags or Hiera or Ansible Vault? Yes, but you have to use ONLY chef or ONLY puppet or ONLY ansible to use those things. If you have a heterogeneous environment, you want something that's universally compatible. Hence an API/Service for this.


Setup
=========
Run this as a normal Django application. Change secretstash/settings for settings that suit your environments.  Please put this behing nginx/apache for SSL termination.   


```
python manage.py syncdb --noinput --settings secretstash.settings.local

python manage.py schemamigration secrets --initial --settings secretstash.settings.local
python manage.py migrate secrets --fake --settings secretstash.settings.local
python manage.py migrate secrets --settings secretstash.settings.local

python manage.py migrate --settings secretstash.settings.local

python manage.py createsuperuser --settings secretstash.settings.local --email='test@test.com' --username='admin'
python manage.py runserver --settings secretstash.settings.local
```

Then in the django admin (http://host:port/admin), add some users and some groups. You can also add users through the oauth system.  

It is also advantageous to add Object Permissions to Groups to allow only specific group membership to add Hosts to specific groups of secrets. For instance, if you intend to have a bunch of secrets in a group called SecretGroup, you should give specific users or groups of users permissions to "Change Group" to allow them to add hosts to that group. This means you can add a user that can launch machines, but only machines that can access the specific secrets in the specific group they are allowed.  

In the admin interface, click on a Group, click "object permissions", click "manage group" to allow specic groups to have "Change Group" access so they can add Hosts to this group. This means that not all users need to be superusers.


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

Adding another group for access to secret:
```
curl -v -X PATCH -H 'Accept: application/json;indent=4' -H 'Content-Type:application/json' -u username:password -d '{"groups":["databases"]}' http://127.0.0.1:8000/secrets/api/secret/15/
```

DevOps (using in the field)
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

TODO
============
More tests -- make sure error messages work
Encrypted backend by default?  
Audit trail?  
Chef cookbook for setup  
Ansible playbook for setup  
Library for ease-of-use

