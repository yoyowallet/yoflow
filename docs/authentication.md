## Authentication & Permissions

You can override the following authentication/permission checks:

### `authenticate(request)`

Initial test on all requests

**Parameters:**

* request -- web request

Default value checks that user is authenticated via `request.user.is_authenticated`.

* * *

### `can_create(request)`

Subsequent check on create endpoint only

**Parameters:**

* request -- web request

By default raises `yoflow.exceptions.PermissionDenied`.

* * *

### `can_delete(request)`

Subsequent check on delete endpoint only

**Parameters:**

* request -- web request

By default raises `yoflow.exceptions.PermissionDenied`.

* * *

### `can_view_history(request)`

Subsequent check on history endpoint only

**Parameters:**

* request -- web request

By default raises `yoflow.exceptions.PermissionDenied`.

* * *

### `has_{state}_permission(request)`

Subsequent test on individual transitions

**Parameters:**

* request -- web request

By default raises `yoflow.exceptions.PermissionDenied`.