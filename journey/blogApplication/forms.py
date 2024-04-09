from django import forms
from.models import Comment

class EmailPostForm(forms.Form):
    
    '''
    The EmailPostForm class is a subclass of Django's Form class. 
    The Form class is a helper class that allows us to create forms in Django.
    '''
    
    name = forms.CharField(max_length=25) # Charfield is rendered as an <input type="text"> element in the HTML form.
    email = forms.EmailField() # EmailField is rendered as an <input type="email"> element in the HTML form.
    to = forms.EmailField() 
    
    '''
    Default widget for CharField is TextInput. We can override this by using the widget argument. 
    Here we are using Textarea widget to render the comments field as a <textarea> element in the HTML form.
    '''

    comments = forms.CharField(required=False, widget=forms.Textarea) 
    
    # If any of these fields are not valid, the form will raise a ValidationError.


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment # The model attribute is used to specify the model that the form will interact with.
        fields = ['name', 'email', 'body'] # The fields attribute is used to specify the fields that will be included in the form.


class SearchForm(forms.Form):
    query = forms.CharField() # The query field is rendered as an <input type="text"> element in the HTML form.
    
    '''
    The query field is required by default. We can make it optional by setting the required attribute to False.
    '''
    
    # If the query field is not valid, the form will raise a ValidationError.

