
There are four main steps to create a workflow:

1. Create Django model
2. Define workflow permissions
3. Write custom workflow transition logic
4. Integrate workflow URLs into project

Imagine we want to publish blog posts on a website but need to manage the status of individual posts. Each blog post can be in one of two states; draft or approved. We want to create and modify blog post instances via a REST interface which will be called via a web application.

### Model

We will create a `Blog` model in `models.py` which has a name, content, and a state field. We can optionally extend `FlowModel` - this will automatically take care of tracking state transitions so we can maintain an audit trail.

```python
# blog/models.py
from django.db import models
from yoflow.models import FlowModel

class Blog(FlowModel):
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

### Permissions

yoflow provides authentication hooks for all views and state changes. By default all endpoints will raise `yoflow.exceptions.PermissionDenied`, in this example we will mute all permission checking - **this is not recommended** - instead you should access the request object and raise an exception to prevent further changes.

```python
# blog/permissions.py
from yoflow import permissions

class BlogPermissions(permissions.Permissions):

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

More authentication information available [here](authentication).

### Workflow

We want to be able to:

* Create new draft blog posts
* Update draft blog posts
* Approve draft blog posts to approved with an optional message

We will create a flow class and extend `yoflow.flow.Flow`, we need to define our model, all possible states, our permissions, and all possible state transitions. Note. transitions allow the state of the instance to remain in the same state - in our example draft blog posts can remain as draft or be moved to approved.

We override `create` & `on_draft` to take `name` and `content` from the POST request and save this to our blog post.

We override `on_approved` to save an optional message from the POST request to meta data - `FlowModel` will take care of storing this meta data along with our state transition history.

We also override the default `response` so that the blog post name and current state is returned on all requests.

```python
# blog/flows.py
from django.http import JsonResponse
from yoflow import flow
from blog import models, permissions

class BlogFlow(flow.Flow):
    model = models.Blog
    states = dict(models.Blog.STATES)
    permissions = permissions.BlogPermissions

    transitions = {
        model.DRAFT: [model.APPROVED],
        model.APPROVED: [],
    }

    def create(self, obj, json, **kwargs):
        obj.name = json['name']
        obj.content = json['content']

    def on_draft(self, obj, json, **kwargs):
        obj.name = json.get('name', obj.name)
        obj.content = json.get('content', obj.content)

    def on_approved(self, json, meta, **kwargs):
        meta['message'] = json.get('message', None)

    def response(self, obj):
        return JsonResponse({'name': obj.name, 'state': obj.get_state_display()})
```

More flow information available [here](flow).

### URLs

Finally, expose workflow URLs by including them in our `urls.py`.

```python
# blog/urls.py
from django.conf.urls import urlw
from blog import flows

urlpatterns = [
    url('^$', flows.BlogFlow().urls),
]
```

For our possible model states this will provide:

| HTTP Method | URI                       | Description                       |
| ----------- | ------------------------- | ----------------------------------|
| `POST`      | `/blog/`                  | Create new instance               |
| `GET`       | `/blog/<int:pk>/history`  | Fetch history of state changes    |
| `POST`      | `/blog/<int:pk>/draft`    | Update instance to draft state    |
| `POST`      | `/blog/<int:pk>/approved` | Update instance to approved state |
| `DELETE`    | `/blog/<int:pk>/`         | Delete instance from database     | 

* * *

#### HTTP Example

```sh
# create new instance
$ http POST localhost:9000/blog/ name='test' content='abc'
{'name': 'test', 'state': 'draft'}

# update instance name and remain in default draft state
$ http POST localhost:9000/blog/1/draft/ name='updated'
{'name': 'updated', 'state': 'draft'}

# update instance state to approved with meta data
$ http POST localhost:9000/blog/1/approved/ message='This is now approved!'
{'name': 'updated', 'state': 'approved'}

# view history
$ http GET localhost:9000/blog/1/history/
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

Similarly to overriding the response format with `response`, you can override the history response format by implementing `response_history` in your flow:

```python
class FormatHistoryFlow(flow.Flow):
    def response_history(self, queryset):
        # only serialize username and meta data
        return JSONResponse(list(queryset.values('user__username', 'meta')), safe=False)
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