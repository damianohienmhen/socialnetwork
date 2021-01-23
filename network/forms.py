from .models import Post
from django import forms



class CommentPosts(forms.ModelForm):
    post_content = forms.CharField(label ="", widget = forms.Textarea( 
    attrs ={ 
        'class':'form-control', 
        'rows':2, 
        'cols':30}))
    class Meta:
        model = Post
        fields = ['post_content']
        
class EditPosts(forms.ModelForm):
    post_content = forms.CharField(label ="", widget = forms.Textarea( 
    attrs ={ 
        'class':'form-control', 
        'rows':2, 
        'cols':30}))
    class Meta:
        model = Post
        fields = ['post_content']


    