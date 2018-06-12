# yoflow

> Django workflows

Define valid state changes for your model instances and run custom logic when changes occur.

Documentation & Example Worflow: https://yoyowallet.github.io/yoflow/

## Requirements

* Django ≥ 1.10
* PostgreSQL ≥ 9.4 (JSON support required)

## Install

Install from PyPI:

```
pipenv install yoflow
```

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

## Running Example

```
pipenv install
pipenv run make
pipenv run ./manage runserver
```

## Running Tests

```
pipenv install --dev
pipenv run make test
```

## Release

### Bump Version

This will automatically create a commit and tag for the new version - as per `.bumpversion.cfg`.

```
pipenv run make bump-patch      # x.x.0 > x.x.1
pipenv run make bump-minor      # x.0.x > x.1.x
pipenv run make bump-major      # 0.x.x > 1.x.x
```

To release to PyPI:

```
pipenv run make release
```
