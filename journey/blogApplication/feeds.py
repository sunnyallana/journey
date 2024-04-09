import markdown
from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords_html
from django.urls import reverse_lazy
from .models import Post

class LatestPostsFeed(Feed):
    title = 'My blog'

# ReverseLazy: The reverse_lazy() utility function is a lazily evaluated version of reverse(). It allows you to use a URL reversal before the project’s URL configuration is loaded.
    link = reverse_lazy('blogApplication:post_list')
    description = 'New posts of my blog.'

    def items(self):
        return Post.published.all()[:5]

    def item_title(self, item):
        return item.title

# In the item_description() method, we use the markdown() function to convert Markdown content to HTML and the truncatewords_html() template filter function to cut the description of posts after 30 words, avoiding unclosed HTML tags.
    def item_description(self, item):
        return truncatewords_html(markdown.markdown(item.body), 30)

    def item_pubdate(self, item):
        return item.publish