from django import forms
from .models import Post, Category, Tag, PostComment, EmailSubscription
from django.forms import CheckboxSelectMultiple



# form for email subscription cho nho huyen lao nhao
class EmailSubscriptionForm(forms.ModelForm):
    class Meta:
        model = EmailSubscription
        fields = ['email']

        # cai nay de them may cai thuoc tinh html vao form
        widgets = {
            'email': forms.EmailInput(attrs={'placeholder': 'Enter your email to subscribe...'})
        }

    # ham kiem tra coi la email co ton tai hay chua
    def clean_email(self):
        # lay email tu cai form
        email = self.cleaned_data.get('email')

        # exist (v): ton tai
        # kiem tra xem email da ton tai trong bang EmailSubscription chua
        if EmailSubscription.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already subscribed.")
        
        return email



class PostAdminForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=CheckboxSelectMultiple,
    )
    
    class Meta:
        model = Post
        fields = ['user', 'title', 'category', 'tags', 'content']
        
        
class PostForm(forms.ModelForm):
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=True,
        label="Category"
    )
    tags = forms.CharField(
        required=False,
        help_text="Add tags separated by commas",
        widget=forms.TextInput(attrs={'placeholder': 'Add tags separated by commas...'})
    )

    title = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter an engaging title...',
            'maxlength': 200
        })
    )
    content = forms.CharField(widget=forms.Textarea(attrs={
        'placeholder': 'Enter your post content...',
        'rows': 10
    }))

    class Meta:
        model = Post
        fields = ['title', 'content', 'category', 'tags']
        
        
class PostCommentForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea(attrs={'rows': 5}))
    
    class Meta:
        model = PostComment
        fields = ['name', 'email', 'content']
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        self.post = kwargs.pop('post', None)
        super().__init__(*args, **kwargs)
   
        
    def clean(self):
        cleaned_data = super().clean()
        
        if not (self.user and self.post):
            raise forms.ValidationError('User and Post are required.')
        
        return cleaned_data
        
    def save(self, commit=True):
        comment = super().save(commit=False)
        comment.user = self.user
        comment.post = self.post
        
        if commit:
            comment.save()
            
        return comment
        
class CommentReplyForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea(attrs={'rows': 2}))
    
    class Meta:
        model = PostComment
        fields = ['content']
        
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        self.post = kwargs.pop('post', None)
        self.comment = kwargs.pop('comment', None)
        super().__init__(*args, **kwargs)
        
    def clean(self):
        cleaned_data = super().clean()
        
        if not (self.user and self.post and self.comment):
            raise forms.ValidationError('User, Post and Comment are required.')
        
        return cleaned_data
    
    def save(self, commit=True):
        reply = super().save(commit=False)
        reply.user = self.user
        reply.post = self.post
        reply.parent = self.comment
        
        if commit:
            reply.save()
            
        return reply