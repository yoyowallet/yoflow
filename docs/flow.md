## Workflow

You can override any of the following workflow functions to customise behaviour:

### `process_{state}_to_{state}(obj)`

Useful for executing custom logic when an instance transitions for the first time, e.g. emailing support@company.com

**Parameters:**

* obj -- model instance

* * *

### `process_on_{state}(obj)`

This will be called even when the current state does not change - if you want fine grain control see `process_{state}_to_{state}`.

**Parameters:**

* obj -- model instance

* * *

### `all(obj)`

Note. the only authentication hook for this is `authenticate` - it will be called on **all** state transitions.

**Parameters:**

* obj -- model instance

* * *

### `validate(view)`

A decorated view with `@transition` can run validation checks before processing the state transition and flow logic. This is useful if you want to validate incoming POST data etc.

**Parameters:**

* view -- view instance
