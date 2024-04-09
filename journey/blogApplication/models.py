from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

# Taggit is a reusable Django application that allows you to add metadata to your models. We will use it to add tags to our posts. Install Taggit using pip install django-taggit.
from taggit.managers import TaggableManager

# The default manager for models is objects. We can create custom managers for our models. Custom managers are useful when we want to put custom methods in the manager and make those methods available to the model objects. We can also use custom managers to modify the initial QuerySet that the manager returns. For example, we can use a custom manager to return only the published posts from the database.
class PublishedManager(models.Manager):
# The PublishedManager class is inheriting from models.Manager. We are overriding the get_queryset method of the manager to return a QuerySet that contains only the published posts. We use the super() method to get the initial QuerySet of the model.
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status=Post.Status.PUBLISHED)


class Post(models.Model):
    # Django, by default, creates a primary key field for each model. We can override the default primary key field by using the primary_key argument to the field.

    # Django's ORM: The object is in memory and not persisted to the database unless save() is called.

    ''' Queries with field lookup methods are built using two underscores, for example publish__year. The __year part is a field lookup method that retrieves the year from the date field. Django supports many field lookup methods, such as __year, __month, __day, __gt (greater than), __lt (less than), __gte (greater than or equal to), __lte (less than or equal to), and many others.
        Same notation is used to access related objects. For example, author__username will retrieve the username field from the related User model.
    '''

    objects = models.Manager() # The default manager.
    published = PublishedManager() # Our custom manager.
    
    tags = TaggableManager() # The tags field is a TaggableManager field. This field allows us to add, retrieve, and remove tags from Post objects. We will use this field to add tags to our posts. The TaggableManager field is provided by the django-taggit library.


    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'

    title = models.CharField(max_length=250) # CharField is used to define short to medium length string. It translates to VARCHAR column in SQL.
    slug = models.SlugField(max_length=250, 
                            unique_for_date='publish') 
    
    # SlugField is used to store URL. It is short label for something, containing only letters, numbers, underscores or hyphens. It builds beautiful SEO-friendly URLs.
    # unique_for_date: This is used to build URLs for posts using their publish date and slug. Django will prevent multiple posts from having the same slug for the same date.

    author = models.ForeignKey(User, # ForeignKey is used to define many-to-one relationships. We have used it to link the Post model with the User model. We have used CASCADE to specify that when the referenced user is deleted, the database will also delete all related blog posts.
                              on_delete=models.CASCADE,
                              related_name='blog_posts') # related_name is the name of the reverse relation from User to Post. It allows us to access related objects easily. We will use this property to retrieve all posts written by a specific user.
    body = models.TextField() # TextField is used to define large text field in a database. It translates to TEXT column in SQL.
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10,
                              choices=Status.choices,
                              default=Status.DRAFT)
    
    class Meta:
        ordering = ('-publish',)
        # db_table can be used here to specify a custom table name for the model.
        # default_manager_name can be used here to specify the default manager for the model. Otherwise, the first manager in the model is the default manager.


    # The get_absolute_url method is used to build the canonical URL of the object. The canonical URL is the preferred URL of an object. It is used to avoid duplicate content issues in search engines. The get_absolute_url method returns the canonical URL of the object. We will use this method in templates to link to specific posts.
    def get_absolute_url(self):
        return reverse('blogApplication:post_detail',
                       args=[self.publish.year,
                             self.publish.month,
                             self.publish.day, self.slug])


    def __str__(self):
        return self.title
    







class Comment(models.Model):

    '''
    The related_name attribute allows you to name the attribute that you use for the relationship from the 
    related object back to this one. We can retrieve the post of a comment object using comment.post and 
    retrieve all comments associated with a post object using post.comments.all(). If you don’t define 
    the related_name attribute, Django will use the name of the model in lowercase, followed by _set 
    (that is, comment_set) to name the relationship of the related object to the object of the model, where 
    this relationship has been defined. 
    '''

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['created']
        indexes = [
            models.Index(fields=['created']),
        ]

    def __str__(self):
        return f'Comment by {self.name} on {self.post}'
 