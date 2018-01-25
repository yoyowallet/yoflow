# yoflow

> Unopinionated Django workflows

Define all possible states for your model using choices. Setup the mapping between states and define logic to run on state change requests. Automatically generate permissions and REST interface based on all possible states.

## Usage example

Create new Django app (`example`) and add a model with a state field of your choice:

```python
# example/models.py
from django.db import models

class Example(models.Model):
    DRAFT = 1
    APPROVED = 2
    STATES = (
        (DRAFT, 'draft'),
        (APPROVED, 'approved'),
    )
    name = models.CharField(max_length=256)
    state = models.IntegerField(choices=STATES, default=DRAFT)
```

Create a `flows.py` module and define state transitions for our model:

```python
# example/flows.py
from yoflow import flow

from example import models

class ExampleFlow(flow.Flow):
    model = models.Example
    states = dict(models.Example.STATES)
    field = 'state'							# default if not provided
    lookup_field = 'pk'						# default if not provided

    transitions = {
        # draft can remain in draft state or move to approved
        model.DRAFT: [model.DRAFT, model.APPROVED],
        # once approved no more state changes can occur
        model.APPROVED: [],
    }

    @classmethod
    def draft_to_approved(cls, request, response, obj):
        # {current_state}_to_{new_state} - allows for fine grain state changes
        pass

    @classmethod
    def on_draft(cls, request, response, obj):
        # on_{new_state} - catches all changes to new state
        response['on_draft'] = True
        return response

    @classmethod
    def on_all(cls, request, response, obj):
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

## TODO

* generate permissions automatically based on states (optional)
* track state changes (datetime/user etc) (optional, django history/new table?)