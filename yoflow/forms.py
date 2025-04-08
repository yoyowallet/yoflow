from django import forms
from django.core.exceptions import ValidationError


class FlowForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # limit available choices based on current state
        state_field = self.flow.field

        current_state = getattr(self.instance, state_field)
        available_states = self.flow.transitions.get(current_state, [])
        states = tuple((k, v) for k, v in self.flow.states.items() if k in available_states or k is current_state)
        if len(states) == 1:
            self.fields[state_field].disabled = True
        else:
            self.fields[state_field].choices = states

    def clean(self):
        cleaned_data = super().clean()
        new_state = cleaned_data.get(self.flow.field)
        if self.instance.state != new_state:
            try:
                if self.instance.pk:
                    self.flow.process(
                        obj=self.instance,
                        to_state=new_state,
                        request=self.request,
                    )
            except Exception as e:
                raise ValidationError(e, code="error")
        return cleaned_data
