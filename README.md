# yoflow

> Unopinionated Django workflows

Define all possible states for your model using choices. Setup the mapping between states and define logic to run on state change requests. Automatically generate permissions and REST interface based on all possible states.

## Usage example

Create new Django app (`example`) and add a model with a state field of your choice - you **must** define all possible states as choices:

```python
# example/models.py
from django.db import models
from yoflow import permissions

class Example(models.Model):
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

    def draft_to_approved(self, request, response, obj, via_admin):
        # {current_state}_to_{new_state} - allows for fine grain state changes
        pass

    def on_draft(self, request, response, obj, via_admin):
        # on_{new_state} - catches all changes to new state
        if not via_admin:
            return {'some': 'value'}

    def on_all(self, request, response, obj, via_admin):
        # on_all - catch all state updates - always executed last
        response['on_all'] = True
        return response
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

* `host:port/example/<pk>/draft/`
* `host:port/example/<pk>/approved/`

### Permissions

If permissions are included `request.user` is checked when a state change occurs - HTTP 403 is returned when the user does not have the correct permission. Alternatively, skip defining model permissions and handle this yourself in flow transition hooks, or use a combination of both.

### Admin Integration

Support for admin via `FlowForm` and ` FlowAdmin` - limits available state choices based on transitions.

```python
# example/forms.py
from django import forms
from yoflow.forms import FlowForm

class ExampleForm(FlowForm):
    pass
```

```python
# example/admin.py
from django.contrib import admin
from example import models, flows, forms
from yoflow.admin import FlowAdmin

@admin.register(models.Example)
class ExampleAdmin(FlowAdmin):
    flow = flows.ParentFlow
    form = forms.ParentForm
```
