from django import forms


class InputForm(forms.Form):

    start_text = '''
    The hippopotamus (Hippopotamus amphibius), or hippo, from the ancient Greek for "river horse", is a large, mostly herbivorous mammal in sub-Saharan Africa, and one of only two extant species in the family Hippopotamidae (the other is the pygmy hippopotamus). After the elephant and rhinoceros, the hippopotamus is the third-largest type of land mammal and the heaviest extant artiodactyl. Despite their physical resemblance to pigs and other terrestrial even-toed ungulates, their closest living relatives are cetaceans (whales, porpoises, etc.) from which they diverged about 55 million years ago. The common ancestor of whales and hippos split from other even-toed ungulates around 60 million years ago. The earliest known hippopotamus fossils, belonging to the genus Kenyapotamus in Africa, date to around 16 million years ago.
    '''
    text = forms.CharField(
        label='Cut and paste a block of text.',
        help_text='Cut and paste a block of text.',
        widget=forms.Textarea(attrs={'tabindex': 4, 'id': 'texto'},
                              initial=start_text, required=False)
    )

    zotero_user = forms.CharField(
        label='Enter your Zotero username.',
        help_text="Enter your Zotero username.",
        widget=forms.TextInput(attrs={'tabindex': 5},
                               required=False)
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
