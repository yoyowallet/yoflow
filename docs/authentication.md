## Authentication & Permissions

You can override the following authentication/permission checks:

### `authenticate`

> Initial test on all requests

Default value checks that user is authenticated via `request.user.is_authenticated`.

### `can_create`

> Subsequent check on create endpoint only

By default raises `yoflow.exceptions.PermissionDenied`.

### `can_delete`

> Subsequent check on delete endpoint only

By default raises `yoflow.exceptions.PermissionDenied`.

### `can_view_history`

> Subsequent check on history endpoint only 

By default raises `yoflow.exceptions.PermissionDenied`.

### `has_{state}_permission`

> Subsequent test on individual transitions

By default raises `yoflow.exceptions.PermissionDenied`.