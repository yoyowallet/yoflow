## Workflow

You can override any of the following workflow functions to customise functionality:

### `create(**kwargs)`

Called via POST `/app/model/`

**Parameters:**

* obj -- (optional) model instance
* meta -- (optional) dictionary
* request -- (optional) web request
* json -- (optional) parsed json data from POST body

* * *

### `response(**kwargs)`

Called via state transition endpoints

**Parameters:**

* obj -- (optional) model instance

* * *

### `response_delete()`

Called via DELETE `/app/model/<id>/`

* * *

### `response_history(**kwargs)`

Called via GET `/app/model/<id>/`

**Parameters:**

* queryset -- (optional) model queryset

* * *

### `process_{state}_to_{state}(**kwargs)`

Called via POST `/app/model/<id>/<state>/`

Useful for executing custom logic when an instance transitions for the first time, e.g. emailing support@company.com

**Parameters:**

* current_state -- (optional) string
* meta -- (optional) dictionary
* obj -- (optional) model instance
* request -- (optional) web request
* json -- (optional) parsed json data from POST body
* new_state -- (optional) string
* state_changed -- (optional) current_state != new_state
* via_admin -- (optional) bool

* * *

### `process_on_{state}(**kwargs)`

Called via POST `/app/model/<id>/<state>/`

This will be called even when the current state does not change - if you want fine grain control see `process_{state}_to_{state}`.

**Parameters:**

* meta -- (optional) dictionary
* obj -- (optional) model instance
* request -- (optional) web request
* json -- (optional) parsed json data from POST body
* new_state -- (optional) string
* state_changed -- (optional) current_state != new_state
* via_admin -- (optional) bool
* current_state -- (optional) string

* * *

### `all(**kwargs)`

Called via POST `/app/model/<id>/<state>/`

Note. the only authentication hook for this is `authenticate` - it will be called on **all** state transitions.

**Parameters:**

* meta -- (optional) dictionary
* obj -- (optional) model instance
* request -- (optional) web request
* json -- (optional) parsed json data from POST body
* new_state -- (optional) string
* state_changed -- (optional) current_state != new_state
* via_admin -- (optional) bool
* current_state -- (optional) string
