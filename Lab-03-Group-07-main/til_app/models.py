from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.crypto import get_random_string




class TempRegister(models.Model):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150)
    name = models.CharField(max_length=50)
    date_of_birth = models.DateField()
    token = models.CharField(max_length=64, unique=True)  
    created_at = models.DateTimeField(auto_now_add=True)  
    verification_url = models.URLField()
    
    def save(self, *args, **kwargs):
        if not self.token:
            self.token = get_random_string(length=64)  
        super().save(*args, **kwargs)
# Custom Account Manager
class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)  
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('date_of_birth', '1990-01-01')
        return self.create_user(username, email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=10, unique=True)
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=50)
    date_of_birth = models.DateField()
    role = models.CharField(max_length=50)


    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()  
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username


# Competition Model
class Competition(models.Model):
    start_date = models.DateField(null=False, blank=False)
    end_date = models.DateField(null=False, blank=False)
    registration_fee = models.FloatField(null=False, blank=False)
    prize_pool = models.FloatField(null=False, blank=False)
    status = models.CharField(max_length=50, null=False, blank=False)
    name = models.CharField(max_length=255, null=False, blank=False, unique=True)  
    image = models.ImageField(upload_to='competition_images/', null=False, blank=False)
    def __str__(self):
        return f"Competition {self.id} ({self.status})"

# UserCompetition (Registration) Model - Many-to-Many relationship between User and Competition
class UserCompetition(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE)
    registration_date = models.DateField(null=False, blank=False)
    level = models.CharField(max_length=50,null=False, blank=False)#add level
    def __str__(self):
        return f"{self.user.username} - {self.competition.id}"
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'competition'], name='unique_user_competition')
        ]

# BulletinBoard Model
class BulletinBoard(models.Model):
    id = models.AutoField(primary_key=True)
    # competition = models.ForeignKey(Competition, on_delete=models.CASCADE)
    post_title = models.CharField(max_length=255)
    post_body = models.TextField()
    created_date = models.DateTimeField(auto_now_add=False)
    updated_date = models.DateTimeField(auto_now=True)
    expiration_date = models.DateField(auto_now=False)
    picture = models.ImageField(upload_to="static/images/media", blank=True, null=True)
    is_top = models.IntegerField(default=0)

    def __str__(self):
        return self.post_title

# Post Model
class Post(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=255, default='Untitled Post')  
    content = models.TextField(max_length=1000, default='No content provided.')  
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='post_images/', null=True, blank=True)
    pinned_at = models.DateTimeField(null=True, blank=True)


    def __str__(self):
        return self.title
    
    def like_count(self):
        return self.post_likes.count()

class Comment(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField(max_length=500, default='No content provided.')
    comment_date = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0)

    def __str__(self):
        return f"Comment by {self.creator.username} on {self.post.title}"

    def like_count(self):
        return self.comment_likes.count()


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    post = models.ForeignKey(Post, null=True, blank=True, on_delete=models.CASCADE, related_name='post_likes')
    comment = models.ForeignKey(Comment, null=True, blank=True, on_delete=models.CASCADE, related_name='comment_likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'post'], name='unique_user_post_like'),
            models.UniqueConstraint(fields=['user', 'comment'], name='unique_user_comment_like')
        ]

    def __str__(self):
        if self.post:
            return f"{self.user.username} likes Post {self.post.id}"
        elif self.comment:
            return f"{self.user.username} likes Comment {self.comment.id}"
        
# Payment Model
class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE)
    amount = models.FloatField()
    payment_date = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=50)

    def __str__(self):
        return f"Payment {self.id} by {self.user.username} for Competition {self.competition.id}"
