from django import forms
from django.core.exceptions import ValidationError

from yoflow.exceptions import FlowException


class FlowForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # limit available choices based on current state
        self.current_state = getattr(self.instance, self.flow.field)
        available_states = self.flow.transitions.get(self.current_state, [])
        states = tuple((k, v) for k, v in self.flow.states.items() if k in available_states or k is self.current_state)
        if len(states) == 1:
            self.fields[self.flow.field].disabled = True
        else:
            self.fields[self.flow.field].choices = states

    def clean(self):
        cleaned_data = super().clean()
        new_state = cleaned_data.get(self.flow.field)
        # call user defined flow logic for state change
        try:
            if self.instance.yoflow_created:
                self.flow.process(
                    obj=self.instance,
                    new_state=self.flow.states[new_state],
                    request=self.request,
                    via_admin=True,
                )
        except FlowException as e:
            raise ValidationError(e, code='error')
        return cleaned_data
