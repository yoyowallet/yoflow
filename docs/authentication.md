## Authentication & Permissions

You can override the following authentication/permission checks:

| Function                 | Description                               | Default Value                        |
| -------------------------|-------------------------------------------|--------------------------------------|
| `authenticate`           | Initial test on all requests              | `request.user.is_authenticated`      |
| `can_create`             | Subsequent test on create endpoint        | `yoflow.exceptions.PermissionDenied` |
| `can_delete`             | Subsequent test on delete endpoint        | `yoflow.exceptions.PermissionDenied` |
| `can_view_history`       | Subsequent test on history endpoint       | `yoflow.exceptions.PermissionDenied` |
| `has_{state}_permission` | Subsequent test on individual transitions | `yoflow.exceptions.PermissionDenied` |
