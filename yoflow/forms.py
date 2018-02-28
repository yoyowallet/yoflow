from django import forms
from django.core.exceptions import ValidationError

from yoflow.exceptions import FlowException


class FlowForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # limit available choices based on current state
        state_field = self.flow.state_field
        self.current_state = getattr(self.instance, state_field)
        available_states = self.flow.transitions.get(self.current_state, [])
        states = tuple((k, v) for k, v in self.flow.states.items() if k in available_states or k is self.current_state)
        if len(states) == 1:
            self.fields[state_field].disabled = True
        else:
            self.fields[state_field].choices = states

    def clean(self):
        cleaned_data = super().clean()
        new_state = cleaned_data.get(self.flow.state_field)
        try:
            if self.instance.pk:
                self.flow.process(
                    obj=self.instance,
                    new_state=self.flow.states[new_state],
                    request=self.request,
                    cleaned_data=cleaned_data,
                )
            else:
                self.flow.process_new(
                    obj=self.instance,
                    request=self.request,
                    cleaned_data=cleaned_data,
                )
        except FlowException as e:
            raise ValidationError(e, code='error')
        return cleaned_data
