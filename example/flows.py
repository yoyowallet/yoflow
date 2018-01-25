from yoflow import exceptions, flow

from example import models


class ParentFlow(flow.Flow):
    model = models.Parent           # define model class
    states = dict(models.STATES)    # define all possible states
    field = 'state'                 # default value if not provided
    lookup_field = 'pk'             # default value if not provided

    # define current state > new states
    transitions = {
        # draft can remain in draft state or move to approved
        models.DRAFT: [models.DRAFT, models.APPROVED],
        # once approved no more state changes can occur
        models.APPROVED: [],
    }


class ExampleFlow(flow.Flow):
    """
    Example instances can only be approved when their parent is approved.
    """
    model = models.Example
    states = dict(models.STATES)

    transitions = {
        models.DRAFT: [models.DRAFT, models.APPROVED],
        models.APPROVED: [],
    }

    def draft_to_approved(self, request, response, obj, via_admin):
        # {current_state}_to_{new_state} - allows for fine grain state changes
        pass

    def on_draft(self, request, response, obj, via_admin):
        # on_{new_state} - catches all changes to new state
        if not via_admin:
            return {'some': 'value'}

    def on_approved(self, request, response, obj, via_admin):
        if obj.parent.state != models.APPROVED:
            # check that parent is approved otherwise raise error
            raise exceptions.FlowException('Unable to approve because parent is not approved - approve parent first.')

    def on_all(self, request, response, obj, via_admin):
        # on_all - catch all state updates - always executed last
        response['all'] = 3
        return response
