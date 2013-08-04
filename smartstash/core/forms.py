import os
from django import forms
from django.conf import settings

class InputForm(forms.Form):

    text = forms.CharField(
        label='Cut and paste a block of text.',
        help_text='Cut and paste a block of text.',
        widget=forms.Textarea(attrs={'tabindex': 4, 'id': 'texto'}),
        initial=open(os.path.join(settings.STATICFILES_DIRS[0], "default.txt")).read(),
        required=False
    )

    zotero_user = forms.CharField(
        label='Enter your Zotero username.',
        help_text="Enter your Zotero username.",
        widget=forms.TextInput(attrs={'tabindex': 5}),
        required=False
    )

    # TODO: alternate inputs- zotero url?
    # use urlfield if appropriate
    # make text input not required, but add form validation
    # so at least one input is required for form to be valid

    def clean(self):
        cleaned_data = super(InputForm, self).clean()

        text = cleaned_data.get('text', '').strip()
        zotero_user = cleaned_data.get('zotero_user', '').strip()

        if not any([text, zotero_user]):
            raise forms.ValidationError('Please enter some text or a Zotero username.')

        # Always return the full collection of cleaned data.
        return cleaned_data
