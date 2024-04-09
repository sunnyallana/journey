from django.contrib import admin
from .models import Post, Comment

# The admin.site.register(Post) code registers the Post model with the Django admin application.
# admin.site.register(Post)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    # The list_display attribute allows you to set the fields of your model that you want to display on the admin object list page.
    list_display = ('title', 'slug', 'author', 'publish', 'status')
    # list_filter creates a right sidebar with the fields specified in the list_filter tuple. It allows people to filter the results based on the fields included in list_filter.
    list_filter = ('status', 'created', 'publish', 'author')
    search_fields = ('title', 'body')
    # prepopulated_fields attribute is used to specify the fields where the value is automatically set using the value of other fields. The slug field is populated with the value of the title field.
    prepopulated_fields = {'slug': ('title',)}
    # raw_id_fields attribute is used to specify the fields where the value is set to an input of type text instead of a select input. This is useful when there are a lot of items and you don't want to load them all in the select input.
    raw_id_fields = ('author',)
    date_hierarchy = 'publish'
    ordering = ('status', 'publish')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'post', 'created', 'active']
    list_filter = ['active', 'created', 'updated']
    search_fields = ['name', 'email', 'body']