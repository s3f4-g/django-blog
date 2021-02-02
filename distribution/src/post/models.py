from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
User = get_user_model()

class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField()
    def __str__(self):
        return self.user.username
    

class Category(models.Model):
    title = models.CharField(max_length=20)
    def __str__(self):
        return self.title
    
class Post(models.Model):
    title = models.CharField(max_length=100)
    content = RichTextUploadingField('content', config_name='extends', null=True)
    overview = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    #comment_count = models.IntegerField(default= 0)
    #view_count = models.IntegerField(default= 0)

    author = models.ForeignKey(Author,on_delete=models.CASCADE)# foreignkey: atıfta bulunmak, on_delete = models.cascade author u sildiğimiz zaman bütün veriler silinecek
    thumbnail = models.ImageField()
    categories = models.ManyToManyField(Category) # bir postun birden fazla katogorisi olabilir katogori de birden fazla postta olabilir
    featured = models.BooleanField(True)
    previous_post = models.ForeignKey('self',related_name='previous',on_delete=models.SET_NULL,blank=True,null=True) # on_delete=models.SET_NULL means if the owner of an existing object got deleted set this field for existing object to null.
    next_post = models.ForeignKey('self',related_name='next',on_delete=models.SET_NULL,blank=True,null=True)

    def __str__(self):
        return self.title
    def get_absolute_url(self):
        return reverse("post-detail", kwargs={"id": self.id})
    def get_update_url(self):
        return reverse("post-update", kwargs={"id": self.id})   
    def get_delete_url(self):
        return reverse("post-delete", kwargs={"id": self.id})
    
    @property 
    def get_comments(self):    # propery decorator ı is declare that it can be accessed like it's a regular property.
        return self.comments.all().order_by('-timestamp')
    @property
    def view_count(self):
        return PostView.objects.filter(post=self).count()

    @property
    def comment_count(self):
        return Comment.objects.filter(post=self).count()
    

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp =  models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    post = models.ForeignKey('Post',related_name='comments',on_delete=models.CASCADE)
    def __str__(self):
        return self.user.username

class PostView(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    def __str__(self):
        return self.user.username