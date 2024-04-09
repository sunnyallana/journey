from django import template
from ..models import Post
from django.db.models import Count

from django.utils.safestring import mark_safe
import markdown


# The template tag is a Python function that is called by the Django template engine to render the output of the template.
# Till now, we have been using the built-in template tags provided by Django. But sometimes, we need to create our own custom template tags.
# Custom template tags are used to add custom template tags to the Django template system.
# The template tags are used to perform some sort of operations on the data and then return the result to the template.

register = template.Library()

# This code defines a custom template tag named total_posts. The total_posts template tag returns the total number of published posts.
# To use it in a template, you need to load the blog_tags template tags library and call the total_posts template tag.
# The @register.simple_tag decorator registers the total_posts function as a simple tag.
# The simple_tag decorator is used to define a custom template tag that does not include any HTML markup.

@register.simple_tag
def total_posts():
 return Post.published.count()

# This code defines a custom template tag named show_latest_posts. The show_latest_posts template tag returns the latest published posts.
# Simple tag and inclusion tag differ in the way they return the output. The simple tag returns a string, while the inclusion tag returns a dictionary of values.
# The difference between simple tag and inclusion tag is that the inclusion tag returns a dictionary of values that are added to the context of the template.

@register.inclusion_tag('blogApplication/post/latest_posts.html')
# Count allows you to specify how many posts you want to display. By default, it will display the latest 5 posts. 
def show_latest_posts(count=5):
    latest_posts = Post.published.order_by('-publish')[:count]
    return {'latest_posts': latest_posts}



# The annotate() method allows you to add extra data to each object in a queryset. This additional data is not part of the model's fields but is dynamically calculated based on the existing data in the queryset.
# The Count aggregation function is used to calculate the total number of comments for each post. The result of the Count aggregation is stored in a new field called total_comments.
# After the annotate() method is applied, each Post object in the queryset will have an additional attribute called total_comments, which represents the total number of comments associated with that post.
@register.simple_tag
def get_most_commented_posts(count=5):
    return Post.published.annotate(
               total_comments=Count('comments')
           ).order_by('-total_comments')[:count]


# The @register.filter(name='markdown') decorator registers a custom template filter named markdown. This filter will be used in Django templates to convert Markdown-formatted text to HTML
# To prevent a name clash between the function name and the markdown module, we have named the function markdown_format and we have named the filter markdown for use in templates, such as {{ variable|markdown }}.
# Inside the markdown_format function, the markdown.markdown() function is called, passing in the text argument. This function converts Markdown syntax into HTML.
# The result of the Markdown conversion is passed to Django's mark_safe() function. This function is crucial because it marks the HTML content as safe for rendering in templates. Without this step, Django would automatically escape the HTML, converting characters like < to &lt;, which would prevent the HTML from being rendered correctly.

@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text))


