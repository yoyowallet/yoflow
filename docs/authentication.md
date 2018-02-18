## Authentication & Permissions

You can override the following authentication/permission checks. You can return `True` to pass the check, return `False` and yoflow will raise `yoflow.exceptions.PermissionDenied` or raise your own exception.

All hooks, apart from `authenticate`, return `False` by default - this means yoflow will prevent execution of the view/workflow logic and raise `yoflow.exceptions.PermissionDenied`.

### `authenticate(request)`

Initial test on all requests, by default returns `request.user.is_authenticated`

**Parameters:**

* request -- web request

* * *

### `can_create(request)`

Subsequent check on create endpoint only

**Parameters:**

* request -- web request

* * *

### `can_delete(request, obj)`

Subsequent check on delete endpoint only

**Parameters:**

* request -- web request
* obj - model instance

* * *

### `can_view_history(request, obj)`

Subsequent check on history endpoint only

**Parameters:**

* request -- web request
* obj - model instance

* * *

### `has_{state}_permission(request, obj)`

Subsequent test on individual transitions

**Parameters:**

* request -- web request
* obj - model instance
