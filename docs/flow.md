## Workflow

You can override any of the following workflow functions to customise behaviour:

### `validate_data(data, request, obj, state, via_admin)`

Called via create and transition endpoints to process incoming request and validate data. By default this will return the JSON payload of the request if not provided. You may wish to customise this behaviour, for example, using django rest framework serializers to validate incoming requests. You can return any object from this function and use it later in other transitional hooks.

**Parameters:**

* data -- dict
* request -- web request
* obj -- model instance
* state -- new state
* via_admin -- bool

### `create(meta, request, validated_data)`

Called via POST `/app/model/` - **not called via admin**

**Parameters:**

* meta -- dictionary
* request -- web request
* validated_data -- validated data from request

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

### `process_{state}_to_{state}(current_state, meta, obj, request, validated_data, new_state, state_changed, via_admin)`

Called via POST `/app/model/<id>/<state>/`

Useful for executing custom logic when an instance transitions for the first time, e.g. emailing support@company.com

**Parameters:**

* current_state -- string
* meta -- dictionary
* obj -- model instance
* request -- web request
* validated_data
* new_state -- string
* state_changed -- current_state != new_state
* via_admin -- bool

* * *

### `process_on_{state}(meta, obj, request, validated_data, new_state, state_changed, via_admin, current_state)`

Called via POST `/app/model/<id>/<state>/`

This will be called even when the current state does not change - if you want fine grain control see `process_{state}_to_{state}`.

**Parameters:**

* meta -- dictionary
* obj -- model instance
* request -- web request
* validated_data
* new_state -- string
* state_changed -- current_state != new_state
* via_admin -- bool
* current_state -- string

* * *

### `all(meta, obj, request, validated_data, new_state, state_changed, via_admin, current_state)`

Called via POST `/app/model/<id>/<state>/`

Note. the only authentication hook for this is `authenticate` - it will be called on **all** state transitions.

**Parameters:**

* meta -- dictionary
* obj -- model instance
* request -- web request
* validated_data
* new_state -- string
* state_changed -- current_state != new_state
* via_admin -- bool
* current_state -- string

* * *

### `admin_json(obj)`

Construct JSON object which mimics POST json from admin change request object.

**Parameters:**

* obj - model instance

**Returns: None**
