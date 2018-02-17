# yoflow

> Django workflows

Define all possible state transitions and state change behaviour for model instances, automatically get:

* REST endpoints for creation, deletion, and individual state transitions
* REST endpoint to view instance state transition history
* Configurable user validation for all endpoints
* Django admin integration

Example & Documentation: www.yoyowallet.github.io/yoflow

## Requirements

* Python3
* Django ≥ 1.11
* PostgreSQL ≥ 9.4 (JSON required)

## Running Example

```sh
mkvirtualenv yoflow
make virtualenv
createdb yoflow
./manage migrate
./manage runserver
```

## Running Tests

```sh
mkvirtualenv yoflow
make virtualenv
tox
```

### TODO
* Return JsonResponse when no matching URL (404)
* Store `Flow` previous_state/new_state as choice value and serialise?
* Tests