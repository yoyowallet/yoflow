# yoflow

> Django workflows

Define valid state changes for your model instances and run custom logic when changes occur.

Documentation & Example Worflow: https://yoyowallet.github.io/yoflow/

## Requirements

* Django ≥ 3.2
* PostgreSQL ≥ 9.4 (JSON support required)

## Install

Install via github:
```
pip install https://github.com/yoyowallet/yoflow.git
```
(Or similar)

Add `yoflow` to your `INSTALLED_APPS`:

```
INSTALLED_APPS = [
    # ...
    'yoflow',
]
```

Apply yoflow database migrations:

```
python manage.py migrate
```
