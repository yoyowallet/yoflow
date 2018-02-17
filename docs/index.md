
There are four main steps to create a workflow:

1. Create/use existing Django model
2. Define flow permissions
3. Write custom flow transition logic
4. Generate and integrate workflow URLs

### Model

Create new Django app (`example`), add a model extending `FlowModel` with a state field of your choice, and define all possible states as choices. `FlowModel` will automatically take care of tracking state transitions.

```python
# example/models.py
from django.db import models
from yoflow.models import FlowModel

class Example(FlowModel):
    DRAFT = 1
    APPROVED = 2
    STATES = (
        (DRAFT, 'draft'),
        (APPROVED, 'approved'),
    )
    name = models.CharField(max_length=256)
    state = models.IntegerField(choices=STATES, default=DRAFT)
```

### Permissions

By default most endpoints will raise `yoflow.exceptions.PermissionDenied`, in this example we will mute all permission checking - this is not recommended - instead you should access the request object and raise an exception to prevent further changes.

```python
# example/permissions.py
from yoflow import permissions

class ExamplePermissions(permissions.Permissions):

    @staticmethod
    def authenticate(request):
        pass

    @staticmethod
    def can_create(request):
        pass

    @staticmethod
    def can_delete(request):
        pass

    @staticmethod
    def can_view_history(request):
        pass

    @staticmethod
    def has_draft_permission(request):
        pass

    @staticmethod
    def has_approved_permission(request):
        pass
```

### Flow

Our flow defines all possible transitions between model states and any custom logic to run from various endpoints.

```python
# example/flows.py
from django.http import JsonResponse
from yoflow import flow
from example import models

class ExampleFlow(flow.Flow):
    model = models.Example
    states = dict(models.Example.STATES)
    permissions = permissions.ExamplePermissions

    transitions = {
        # draft can remain in draft state or move to approved
        model.DRAFT: [model.APPROVED],
        # once approved no more state changes can occur
        model.APPROVED: [],
    }

    def create(self, obj, json, meta, request):
        obj.name = json['name']

    def on_draft(self, new_state, obj, request, json, meta, via_admin):
        obj.name = json.get('name', obj.name)

    def draft_to_approved(self, new_state, obj, request, json, meta, via_admin):
        pass

    def on_approved(self, new_state, obj, request, json, meta, via_admin):
        meta['message'] = json.get('message', None)

    def all(self, new_state, obj, request, json, meta, via_admin):
        pass

    def response(self, obj):
        return JsonResponse({'name': obj.name, 'state': obj.get_state_display()})
```

### URLs

Finally, expose our workflow URLs by including them in your normal `urls.py`.

```python
# example/urls.py
from django.conf.urls import urlw
from example import flows

urlpatterns = [
    url('^$', flows.ExampleFlow().urls),
]

# include example app urls in your project urls.py, e.g.
# url('^example/', include('example.urls')),
```

For our possible model states this will provide:

| HTTP Method | URI                          | Description                            |
| ----------- | ---------------------------- | -------------------------------------- |
| `POST`      | `/example/`                  | Create new instance with default state |
| `GET`       | `/example/<int:pk>/history`  | Fetch history of state changes         |
| `POST`      | `/example/<int:pk>/draft`    | Update instance to draft state         |
| `POST`      | `/example/<int:pk>/approved` | Update instance to approved state      |
| `DELETE`    | `/example/<int:pk>/`         | Delete instance from database          | 

#### HTTP Example

```sh
# create new instance
$ http POST localhost:9000/example/ name='test'
{'name': 'test', 'state': 'draft'}

# update instance name and remain in default draft state
$ http POST localhost:9000/example/1/draft/ name='updated'
{'name': 'updated', 'state': 'draft'}

# update instance state to approved with meta data
$ http POST localhost:9000/example/1/approved/ message='This is now approved!'
{'name': 'updated', 'state': 'approved'}

# view history
$ http GET localhost:9000/example/1/history/
[
    {
        "created_at": "2018-01-29T16:21:59.829Z",
        "meta": {
            "message": "This is now approved!"
        },
        "new_state": "approved",
        "previous_state": "draft",
        "user": null
    },
    {
        "created_at": "2018-01-29T16:21:57.794Z",
        "meta": null,
        "new_state": "draft",
        "previous_state": null,
        "user": null
    }
]
```

Similarly to overriding the response format of state transitions with `response`, you can override the history response format by implementing `response_history` in your flow:

```python
class FormatHistoryFlow(flow.Flow):
    def response_history(self, queryset):
        # only serialize username and meta data
        return JSONResponse(list(queryset.values('user__username', 'meta')), safe=False)
```

## Authentication & Permissions

You can override the following authentication/permission checks:

| Function                 | Description                               | Default Value                        |
| -------------------------|-------------------------------------------|--------------------------------------|
| `authenticate`           | Initial test on all requests              | `request.user.is_authenticated`      |
| `can_create`             | Subsequent test on create endpoint        | `yoflow.exceptions.PermissionDenied` |
| `can_delete`             | Subsequent test on delete endpoint        | `yoflow.exceptions.PermissionDenied` |
| `can_view_history`       | Subsequent test on history endpoint       | `yoflow.exceptions.PermissionDenied` |
| `has_{state}_permission` | Subsequent test on individual transitions | `yoflow.exceptions.PermissionDenied` |

To override any of these; extend the yoflow permissions class and link to your defined flow:

```python
from yoflow import flow, permissions

class ExamplePermissions(permissions.Permissions):
    @staticmethod
    def authenticate(request):
        pass  # allow all requests
        
class ExampleFlow(flow.Flow):
    permissions = ExamplePermissions
```

### Admin Integration

Support for admin via `FlowAdmin` - limits available state choices based on transitions and shows inline historical state changes:

```python
# example/admin.py
from django.contrib import admin
from example import models, flows, forms
from yoflow.admin import FlowAdmin

@admin.register(models.Example)
class ExampleAdmin(FlowAdmin):
    flow = flows.ExampleFlow
    form = forms.ExampleForm
```

### Settings

##### `YOFLOW_STATE_MAX_LENGTH` (default=256)

Max length of `CharField` used to store value of before/after state transition.

##### `YOFLOW_OBJECT_ID_MAX_LENGTH` (default=256)

Max length of `CharField` used to store object pk. Usually this will be an integer primary key but in some cases you might wish to use uuid or something else.
