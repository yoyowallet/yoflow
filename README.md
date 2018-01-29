# yoflow

> Django workflows

Define all possible state transitions and state change behaviour for model instances, automatically get:

* REST endpoint to view instance state history
* REST endpoint for each state transition
* Permission validation per state transition
* State transition tracking
* Admin integration

## Requirements

* Django 2.0
* PostgreSQL ≥ 9.4

## Usage example

Create new Django app (`example`) and add a model with a state field of your choice - you **must** define all possible states as choices. **Do not use `all` as a value for choices - this is reserved for performing a special action inside flows.**

```python
# example/models.py
from django.db import models
from yoflow import permissions
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

    class Meta:
        # create permission for each state, skip if permissions not required
        permissions = permissions(STATES)
```

Create a `flows.py` module and define state transitions for our model:

```python
# example/flows.py
from django.http import JsonResponse
from yoflow import flow
from example import models

class ExampleFlow(flow.Flow):
    model = models.Example
    states = dict(models.Example.STATES)
    field = 'state'                         # default if not provided
    lookup_field = 'pk'                     # default if not provided

    transitions = {
        # draft can remain in draft state or move to approved
        model.DRAFT: [model.DRAFT, model.APPROVED],
        # once approved no more state changes can occur
        model.APPROVED: [],
    }

    def draft_to_approved(self, new_state, obj, request, meta, via_admin):
        # {current_state}_to_{new_state} - allows for fine grain state changes
        pass

    def on_draft(self, new_state, obj, request, meta, via_admin):
        # on_{new_state} - catches all changes to new state
        pass

    def on_all(self, new_state, obj, request, meta, via_admin):
        # on_all - catch all state updates
        pass

    def response(self, obj):
        # build custom HTTP response - obj has new state persisted at this point
        return JsonResponse({'foo': 'bar'})
```

Generate URLs for state transitions

```python
# example/urls.py
from django.urls import path
from example import flows

urlpatterns = [
    path('<int:pk>/', flows.ExampleFlow().urls),
]

# include urls in your project urls.py, e.g.
# path('example/', include('example.urls')),
```

For our possible models states this will provide:

| HTTP Method | URI                      | Description                       |
| ----------- | ------------------------ | --------------------------------- |
| `GET`       | `/example/<pk>/history`  | Fetch history of state changes    |
| `POST`      | `/example/<pk>/draft`    | Update instance to draft state    |
| `POST`      | `/example/<pk>/approved` | Update instance to approved state |

### Authentication

By default we check if `request.user.is_authenticated` on all views - if this is not appropriate you can override this behaviour in your flow using `authenticate(self, request)`.

```python
class NoAuthenticationFlow(flow.Flow):
    def authenticate(self, request):
        pass
```

### Permissions

If permissions are included `request.user` is checked when a state change occurs - HTTP 403 is returned when the user does not have the correct permission. Alternatively, skip defining model permissions and handle this yourself in flow transition hooks, or use a combination of both.

### Admin Integration

Support for admin via `FlowAdmin` - limits available state choices based on transitions and shows inline historical state changes.

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

### TODO
* Django 1.11 support
