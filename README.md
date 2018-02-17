# yoflow

> Django workflows

Define all possible state transitions and state change behaviour for model instances, automatically get:

* REST endpoints for creation, deletion, and individual state transitions
* REST endpoint to view instance state transition history
* Configurable user validation for all endpoints
* Django admin integration

Example & Documentation: https://yoyowallet.github.io/yoflow/

## Requirements

* Django ≥ 1.8
* PostgreSQL ≥ 9.4 (JSON required)

## Running Example

```sh
mkvirtualenv yoflow
make
./manage runserver
```

## Running Tests

```sh
make test
```

### TODO
* Return JsonResponse when no matching URL (404)
* Store `Flow` previous_state/new_state as choice value and serialise?
* Tests