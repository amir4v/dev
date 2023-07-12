from typing import Any, Dict
from django import forms

from . import models
from django.utils.translation import gettext_lazy as _
from django.forms import BaseModelFormSet
from django.forms import inlineformset_factory
from django.forms import BaseInlineFormSet


class MyForm(forms.Form):
    name = forms.CharField(max_length=100, help_text='Use puns liberally',)

class PostForm(forms.ModelForm):
    class Meta:
        model = models.Post
        fields = ['title', 'content']
        # fields = '__all__'
        # exclude = ['title']
    
    def clean_title(self, title):
        return title
    
    widgets = {
            'title': forms.Textarea(attrs={'cols': 80, 'rows': 20}),
    }
    
    labels = {
        'name': _('Writer'),
    }
    help_texts = {
        'name': _('Some useful help text.'),
    }
    error_messages = {
        'name': {
            'max_length': _("This writer's name is too long."),
        },
    }
    
    # slug = CharField(validators=[validate_slug])
    
    # authors = forms.ModelMultipleChoiceField(queryset=Author.objects.all())
    
    # title = forms.CharField(
    #     max_length=3,
    #     widget=forms.Select(choices=TITLE_CHOICES),
    # )
    
    def clean(self) -> Dict[str, Any]:
        return super().clean()



# ModelForm factory function¶
# You can create forms from a given model using the standalone function modelform_factory(),
# instead of using a class definition. This may be more convenient if you do not have many customizations to make:
#
# >>> from django.forms import modelform_factory
# >>> from myapp.models import Book
# >>> BookForm = modelform_factory(Book, fields=("author", "title"))
#
# >>> from django.forms import Textarea
# >>> Form = modelform_factory(Book, form=BookForm,
# ...                          widgets={"title": Textarea()})





# formset = AuthorFormSet(
#     request.POST, request.FILES,
#     queryset=Author.objects.filter(name__startswith='O'),
# )


# inlineformset_factory(parent, model, fields=(,))







