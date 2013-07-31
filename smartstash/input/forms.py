from django import forms


class InputForm(forms.Form):

    text = forms.CharField(
        label='Text Input',
        help_text='cut and paste a block of text',
        widget=forms.Textarea,
        required=True)

    # TODO: alternate inputs- zotero url?
    # use urlfield if appropriate
    # make text input not required, but add form validation
    # so at least one input is required for form to be valid

