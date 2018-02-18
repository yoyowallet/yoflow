# yoflow

> Django workflows

Define all possible state transitions and state change behaviour for model instances, automatically get:

* REST endpoints for creation, deletion, and individual state transitions
* REST endpoint to view instance state transition history
* Programmable user authentication for all views/transitions
* Django admin integration

Documentation & Example Worflow: https://yoyowallet.github.io/yoflow/

## Install

```
pip install git+ssh://git@github.com/yoyowallet/yoflow.git
```

Add `yoflow` to `settings.INSTALLED_APPS`

## Requirements

* Django ≥ 1.10
* PostgreSQL ≥ 9.4 (JSON support required)

## Running Example

```
mkvirtualenv yoflow
make
./manage runserver
```

## Running Tests

```
make test
```
