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

Create new Django app (`example`), add a model with a state field of your choice, and define all possible states as choices.

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
    field = 'state'                         # default value
    lookup_field = 'pk'                     # default value
    url_regex = '<int:pk>'                  # default value

    transitions = {
        # draft can remain in draft state or move to approved
        model.DRAFT: [model.APPROVED],
        # once approved no more state changes can occur
        model.APPROVED: [],
    }

    def create(self, obj, json, meta, request):
        # if create is defined then you can PUT new instances at the root URL
        obj.name = json['name']

    def draft_to_approved(self, new_state, obj, request, json, meta, via_admin):
        # {current_state}_to_{new_state} - called for specific state transition
        pass

    def on_approval(self, new_state, obj, request, json, meta, via_admin):
        # on_{new_state} - called for all transitions to new state
        # save data with state transition, e.g. save approval message from request
        meta['message'] = json.get('message', None)

    def all(self, new_state, obj, request, json, meta, via_admin):
        # called for all state transitions
        pass

    def response(self, obj):
        # build custom HTTP response - obj has new state persisted at this point
        # note - this is not called via Django admin
        return JsonResponse({'foo': 'bar'})
```

Generate URLs for state transitions

```python
# example/urls.py
from django.urls import path
from example import flows

urlpatterns = [
    path('', flows.ExampleFlow().urls),
]

# include example app urls in your project urls.py, e.g.
# path('example/', include('example.urls')),
```

For our possible models states this will provide:

| HTTP Method | URI                          | Description                            |
| ----------- | ---------------------------- | -------------------------------------- |
| `PUT`       | `/example/`                  | Create new instance with default state |
| `GET`       | `/example/<int:pk>/history`  | Fetch history of state changes         |
| `POST`      | `/example/<int:pk>/draft`    | Update instance to draft state         |
| `POST`      | `/example/<int:pk>/approved` | Update instance to approved state      |

#### Example

```sh
# create new instance
http PUT localhost:9000/example/ name='test'
{'foo': 'bar'}

# update instance name and remain in default draft state
http POST localhost:9000/example/1/draft/ name='updated'
{'foo': 'bar'}

# update instance state to approved with meta data
http POST localhost:9000/example/1/approved/ message='This is now approved!'
{'foo': 'bar'}

# view history
http GET localhost:9000/example/1/history/
[
    {
        "created_at": "2018-01-29T16:21:59.829Z",
        "meta": {
            "comment": "This is an approval message"
        },
        "new_state": "approved",
        "previous_state": "draft",
        "user": 1
    },
    {
        "created_at": "2018-01-29T16:21:57.794Z",
        "meta": null,
        "new_state": "draft",
        "previous_state": "draft",
        "user": 1
    }
]
```

Similarly to overriding the response format of state transitions with `response`, you can override the history response format by implementing `response_history` in your flow.

```python
class FormatHistoryFlow(flow.Flow):
    def response_history(self, queryset):
        """
        :param queryset:    Django queryset of Flow instances
        """
        # only serialize username and meta data
        return JSONResponse(list(queryset.values('user__username', 'meta')), safe=False)
```

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
