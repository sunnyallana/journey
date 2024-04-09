from django.contrib.sitemaps import Sitemap
from .models import Post

# The Sitemap class is a Django class that generates sitemap XML files for search engines. The sitemap XML file contains a list of URLs on your site that you want search engines to index.

class PostSitemap(Sitemap):
    changefreq = 'weekly'
    # The priority attribute is used to indicate the priority of the page relative to other pages on your site. The value should be a floating-point number between 0.0 and 1.0.
    priority = 0.9

    def items(self):
        return Post.published.all()
    def lastmod(self, obj):
        return obj.updated
    

# The items() method returns the QuerySet of objects to include in this sitemap. By default, Django calls the get_absolute_url() method on each object to retrieve its URL.
# The lastmod() method returns the last time the object was modified. This information is used by search engines to determine how often the page should be indexed.
# Both the changefreq and priority attributes can be either methods or attributes of the Sitemap class. If they are methods, they should take an object as an argument and return the desired value.
    
    