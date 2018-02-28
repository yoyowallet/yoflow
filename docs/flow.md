## Workflow

You can override any of the following workflow functions to customise functionality:

### `create(obj, meta, request, json)`

Called via POST `/app/model/`

**Parameters:**

* obj -- model instance
* meta -- dictionary
* request -- web request
* json -- parsed json data from POST body

* * *

### `response(obj)`

Called via state transition endpoints

**Parameters:**

* obj -- model instance

* * *

### `response_delete()`

Called via DELETE `/app/model/<id>/`

* * *

### `response_history(queryset)`

Called via GET `/app/model/<id>/`

**Parameters:**

* queryset -- model queryset

* * *

### `process_{state}_to_{state}(current_state, meta, obj, request, json, new_state, state_changed, via_admin)`

Called via POST `/app/model/<id>/<state>/`

Useful for executing custom logic when an instance transitions for the first time, e.g. emailing support@company.com

**Parameters:**

* current_state -- string
* meta -- dictionary
* obj -- model instance
* request -- web request
* json -- parsed json data from POST body
* new_state -- string
* state_changed -- current_state != new_state
* via_admin -- bool

* * *

### `process_on_{state}(meta, obj, request, json, new_state, state_changed, via_admin, current_state)`

Called via POST `/app/model/<id>/<state>/`

This will be called even when the current state does not change - if you want fine grain control see `process_{state}_to_{state}`.

**Parameters:**

* meta -- dictionary
* obj -- model instance
* request -- web request
* json -- parsed json data from POST body
* new_state -- string
* state_changed -- current_state != new_state
* via_admin -- bool
* current_state -- string

* * *

### `all(meta, obj, request, json, new_state, state_changed, via_admin, current_state)`

Called via POST `/app/model/<id>/<state>/`

Note. the only authentication hook for this is `authenticate` - it will be called on **all** state transitions.

**Parameters:**

* meta -- dictionary
* obj -- model instance
* request -- web request
* json -- parsed json data from POST body
* new_state -- string
* state_changed -- current_state != new_state
* via_admin -- bool
* current_state -- string

### `admin_json(obj)`

Construct JSON object which mimics POST json from admin change request object.

**Parameters:**

* obj - model instance

**Returns: None**
