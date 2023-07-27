from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    following = models.ManyToManyField('self', blank=True, related_name="followers", symmetrical=False)
    bio = models.TextField(max_length=200, blank=True, default="Bio")

    def __str__(self):
        return f"u/{self.username}"
    
    @property
    def get_user_followers(self):
        return User.objects.get(username=self.username).following.all()
    
    @property
    def get_user_following(self):
        return User.objects.get(username=self.username).followers.all()

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    opinion = models.CharField(max_length=850)
    pub_date = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(User, blank=True, related_name="likes")
    sup_post = models.ForeignKey('self', null=True, on_delete=models.CASCADE, related_name="sub_post")

    def __str__(self):
        return f"u/{self.user.username} posted {self.opinion[:50]}"

    class Meta:
        ordering = ['-pub_date']

    @property
    def get_likes_count(self):
        return Post.objects.get(pk=self.id).likes.count()
    
    @property
    def get_post_like_list(self):
        return Post.objects.get(pk=self.id).likes.all()
    
    @property
    def get_sub_post(self):
        return Post.objects.filter(sup_post=self).order_by('-pub_date')

    @property
    def get_comment_count(self):
        return self.sub_post.all().count()

    @property
    def get_sub_post_of_followed_user(self):
        post = Post.objects.filter(sup_post=self)
        
        

