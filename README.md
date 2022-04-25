### Description

Small API to manage images and their tags. Also includes tracking of user interaction with API routes.

### Implementation details
`Django Rest Framework` is used to build API (`Django-filter` is used to handle URL query params).

Images can be uploaded one by one ("Create Image" request can contain the list of existing tags to be assigned to the image). 
Uploaded images are stored on the disk locally.

`Sqlite3` DB is used by default.


### Setup

- clone the repository
- prepare virtual environment (eg. `virtualenv -p python3 venv`)
- install requirements `pip install -r requirements.txt`
- apply Django migrations `./manage.py migrate`
- create user

Admin user:
```
./manage.py createsuperuser --email admin@example.com --username admin
```

Regular user:
`./manage.py shell`
```
>>> from django.contrib.auth.models import User
>>> User.objects.create_user("username", "Pas$w0rd")
<User: username>
```

- start debug server locally (port 8000 by default)
`./manage.py runserver`

In your browser go to `http://127.0.0.1:8000/api/` to see the list of available API routes.
Use username/password to log in.


### Endpoints
CRUD route to handle images: `/api/images/`

CRUD route to handle tags: `/api/tags/`

Read-only route to list trackings: `/api/trackings/` 

All the endpoints can be used via django rest framework UI, alternatively you can use cURL examples.
Note: `trackings` DB records are created automatically when user interact with API (including `GET /api/` endpoint, excluding `/api/trackings/` route)

Eg.
"create tag":
```
curl -X POST -H 'Content-Type: application/json' -d '{"name": "brand new tag"}' -u <username>:<password> http://127.0.0.1:8000/api/tags/
```
 
"create image" (NOTE: tags should already exist in DB):
```
curl -X POST -F 'image=@/<pwd to image>/test123.jpeg' -F 'tags=my tag' -F 'tags=another tag'  -u <username>:<password> http://127.0.0.1:8000/api/images/
```

### Tests
Run `./manage.py test`

To run tests with coverage:
```
pip install coverage
coverage run ./manage.py test
coverage report -m
```

```
Name                                                                              Stmts   Miss  Cover   Missing
---------------------------------------------------------------------------------------------------------------
annalise_test/__init__.py                                                             0      0   100%
annalise_test/common/__init__.py                                                      0      0   100%
annalise_test/common/middleware.py                                                   14      0   100%
annalise_test/common/tests/__init__.py                                                0      0   100%
annalise_test/common/tests/test_middleware.py                                        18      0   100%
annalise_test/images/__init__.py                                                      0      0   100%
annalise_test/images/apps.py                                                          4      0   100%
annalise_test/images/filters.py                                                      23      0   100%
annalise_test/images/migrations/0001_initial.py                                       7      0   100%
annalise_test/images/migrations/__init__.py                                           0      0   100%
annalise_test/images/models.py                                                       12      0   100%
annalise_test/images/serializers.py                                                  10      0   100%
annalise_test/images/tests/__init__.py                                                0      0   100%
annalise_test/images/tests/test_api.py                                               74      0   100%
annalise_test/images/views.py                                                        12      0   100%
annalise_test/settings.py                                                            22      0   100%
annalise_test/tracking/__init__.py                                                    0      0   100%
annalise_test/tracking/apps.py                                                        4      0   100%
annalise_test/tracking/middleware.py                                                 17      0   100%
annalise_test/tracking/migrations/0001_initial.py                                     7      0   100%
annalise_test/tracking/migrations/0002_alter_apiinteractiontracking_response.py       4      0   100%
annalise_test/tracking/migrations/__init__.py                                         0      0   100%
annalise_test/tracking/models.py                                                     12      0   100%
annalise_test/tracking/serializers.py                                                 6      0   100%
annalise_test/tracking/tests/__init__.py                                              0      0   100%
annalise_test/tracking/tests/test_tracking.py                                        19      0   100%
annalise_test/tracking/views.py                                                       8      0   100%
annalise_test/urls.py                                                                11      0   100%
manage.py                                                                            12      2    83%   12-13
---------------------------------------------------------------------------------------------------------------
TOTAL                                                                               296      2    99%

```

### Notes 
`Sqlite3` DB was chosen as an example to simplify the minimum required prerequisites. In production I'd probably expect to see eg. `PostgreSQL` or `MongoDB`.

There is no any limitations to `tags` except the length of 50 chars. Some normalization/validation could be added.

`images` can be uploaded only one by one. Bulk upload looks useful.


### How would I deploy the project into a Cloud environment
Django based projects usually consumes some resources (CPU and memory), so we'd probably go with AWS ECS approach rather than AWS Lambda.

Infrastructure overview:

- ECS service (run docker container with application)
- Load Balancer (route traffic to ECS service)
- API Gateway (accept and process API calls)

The approach will require `Dockerfile` to be created.
Also wsgi http server should be added and configured (uwsgi, gunicorn, etc.)

CI/CD flow will include docker image preparing and deploying updates to AWS ECS service.
ECS service will take care all the updates (including DB migrations) are deployed and after that will switch the traffic to the new task version.
 