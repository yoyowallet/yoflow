Imagine we want to publish blog posts on a website but need to manage the status of individual posts. Each blog post can be in one of two states; draft or approved. We want to create and modify blog posts via a REST interface which will be called from a web application. When a blog post is transitioned to the approved state we should send an email to recipients informing them of the change. *The following code can be found in the example directory of this repository.*

### Model

We will create a `Post` model with some basic fields but importantly a state field. All potential states must be defined using choices. We can optionally extend `FlowModel` - this will add automatic state tracking so we can maintain and query an audit trail.

```python
# example/models.py
from django.db import models
from yoflow.models import FlowModel

class Post(FlowModel):
    DRAFT = 1
    APPROVED = 2
    STATES = (
        (DRAFT, 'draft'),
        (APPROVED, 'approved'),
    )
    name = models.CharField(max_length=256)
    content = models.TextField()
    state = models.IntegerField(choices=STATES, default=DRAFT)
```

### Workflow

Our workflow must define the model, and all possible state transitions.

```python
# example/flows.py
from django.core.mail import send_mail
from yoflow import flow
from example import models

class PostFlow(flow.Flow):
    model = models.Post
    transitions = {
        model.DRAFT: [model.APPROVED],
        model.APPROVED: [],
    }

    @staticmethod
    def draft_to_approved(obj, meta):
        pass

    @staticmethod
    def on_approved(obj, meta):
        send_mail('Approved!', '{} was approved'.format(obj), 'from@example.com', ['to@example.com'])

    @staticmethod
    def all(obj, meta):
        pass

```

Our transitions dict defines that blog posts in a 'draft' state can be updated to an 'approved' state, but once 'approved' they can't revet back to 'draft'. In reality you will likely have more states/choices.

We implement `on_approved` to send an email whenever the state is updated to 'approved'. There are several available transition hooks:

| Function             | Description                       |
|----------------------|-----------------------------------|
| {state}\_to\_{state} | Called for specific state changes |
| on_{state}           | Called for all changes to state   |
| all                  | Called on all transitions         |

More workflow information is available [here](flow).

### View

You are free to use any view logic - in this example we use django-rest-framework because it provides a lot of useful functionality.

```python
# example/views.py
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from yoflow.decorators import transition
from example import flows, models, serializers

class PostViewSet(viewsets.ModelViewSet):
    queryset = models.Post.objects.all()
    serializer_class = serializers.PostSerializer
    flow = flows.PostFlow

    @action(methods=['post'], detail=True)
    @transition(to_state=models.Post.APPROVED)
    def approved(self, request, pk=None):
        return Response({ 'name': obj.name, 'state': obj.get_state_display() })

    @action(methods=['get'], detail=True)
    def history(self, request, pk=None):
        qs = self.get_object().yoflow_history.all()
        return Response(qs.values('created_at', 'new_state', 'previous_state', 'meta', 'user'))
```

You can decorate individual views with `@transition` - this will:

* Validate the requested transition based on current state
* Update the state of the instance
* Create a yoflow_history instance **if** your model extends `FlowModel`
* Run custom flow logic

#### HTTP Example

```sh
# create new instance
$ http POST localhost:8000/blog/post/ name='test' content='abc'
{"name": "test", "state": "draft"}

# update instance state to approved with meta data
$ http POST localhost:8000/blog/post/1/approved/ message='this is now approved'
{"name": "updated", "state": "approved"}

# view history
$ http GET localhost:8000/blog/post/1/history/
[
    {
        "created_at": "2018-01-29T17:00:00.000Z",
        "new_state": "approved",
        "previous_state": "draft",
        "meta": {
            "message": "this is now approved"
        }
        "user": null
    }
]
```

## Admin Integration

Support for admin via `FlowAdmin` - limits available state choices based on transitions and shows inline historical state changes:

```python
# example/admin.py
from django.contrib import admin
from yoflow.admin import FlowAdmin
from example import models, flows

@admin.register(models.Post)
class ParentAdmin(FlowAdmin):
    flow = flows.PostFlow
    list_display = ('name', 'state')
    list_filter = ('state',)
```

## Settings

##### `YOFLOW_STATE_MAX_LENGTH`

Max length of `CharField` used to store value of before/after state transition. *Default 256*

##### `YOFLOW_OBJECT_ID_MAX_LENGTH`

Max length of `CharField` used to store object pk. Usually this will be an integer primary key but in some cases you might wish to use uuid or something else. *Default 256*

##### `YOFLOW_DEFAULT_STATE_FIELD`

Default name of state field - useful if you following naming conventions and frequently use the same name for choices state field rather than defining in every view. *Default 'state'*

##### `YOFLOW_TYPE_ERROR`

Type of exception to raise when invalid meta data sent to yoflow history. If using django-rest-framework it is useful to use APIException as this provides nice JSON resposnes. *Default TypeError*
