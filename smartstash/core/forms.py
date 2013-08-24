import os
from django import forms
from django.conf import settings
from social_auth.models import UserSocialAuth
from pyzotero import zotero


class InputForm(forms.Form):

    text = forms.CharField(
        label='Cut and paste a block of text.',
        help_text='Cut and paste a block of text.',
        widget=forms.Textarea(attrs={'tabindex': 4, 'id': 'texto'}),
        initial=open(os.path.join(settings.STATICFILES_DIRS[0], "default.txt")).read(),
        required=True
        )

    # TODO: alternate inputs- zotero url?
    # use urlfield if appropriate
    # make text input not required, but add form validation
    # so at least one input is required for form to be valid

    # def clean(self):
    #     cleaned_data = super(InputForm, self).clean()

    #     text = cleaned_data.get('text', '').strip()
    #     zotero_user = cleaned_data.get('zotero_user', '').strip()

    #     if not any([text, zotero_user]):
    #         raise forms.ValidationError('Please enter some text or a Zotero username.')

    #     # Always return the full collection of cleaned data.
    #     return cleaned_data


class ZoteroInputForm(forms.Form):
    default_choices = [('recent', 'recent entries')]
    default_field_args = {
        'help_text': 'Choose which part of your Zotero library to use',
        'required': True
    }
    selection = forms.ChoiceField(choices=default_choices, **default_field_args)

    def __init__(self, user=None, *args, **kwargs):
        super(ZoteroInputForm, self).__init__(*args, **kwargs)

        if user is not None:
            # retrieve zotero user info
            zotero_user = UserSocialAuth.objects.get(user=user, provider='zotero')
            zot = zotero.Zotero(zotero_user.uid, 'user', zotero_user.tokens['oauth_token'])

            # generate a list of tuples: collection key, name
            collections = []
            for coll in zot.collections():
                collections.append(('collection:%s' % coll['collectionKey'],
                                     coll['name']))

            # similar for groups
            groups = []
            for grp in zot.groups():
                groups.append(('group:%s' % grp['group_id'], grp['name']))

            # similar for tags
            # NOTE: tag results for my library has tags with type 0 (tags I created)
            # and tags with type 1 - seems to be subjects from records (?);
            # only including type 1 for now
            tags = [('tag:%s' % t['tag'], t['tag']) for t in zot.tags()
                    if t['type'] == 0]

            # if we found any groups or collections, re-init choice field
            # with the new list
            if collections or groups or tags:
                choices = [] + self.default_choices
                if collections:
                    choices.append(('Collections', collections))
                if groups:
                    choices.append(('Groups', groups))
                if tags:
                    choices.append(('Tags', tags))
                self.fields['selection'] = forms.ChoiceField(
                    choices=choices,
                    widget=forms.widgets.Select(attrs={'size': 10})
                    )
