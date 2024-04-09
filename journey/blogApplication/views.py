from django.shortcuts import render, get_object_or_404
from .models import Post, Comment
from django.views.generic import ListView
from .forms import EmailPostForm, CommentForm, SearchForm

# The require_POST decorator is used to ensure that the view only accepts POST requests. If the view receives a GET request, it will raise an exception.
from django.views.decorators.http import require_POST

# The send_mail() function is used to send the email. The send_mail() function takes the subject, message, from_email, to_email, and fail_silently arguments.
from django.core.mail import send_mail

# To implement pagination, we need to import the following classes and functions from Django:
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# To filter posts by tags, we need to import the Tag model from the taggit application.
from taggit.models import Tag

# The Count aggregation function is used to generate a calculated field that contains the number of tags shared between the queried post and all the other posts.
# You could import avg, max, min, sum, etc.
from django.db.models import Count

# POSTGRES_SEARCH: Django provides a SearchQuery class to translate terms into a search query object. By default, the terms are passed through stemming algorithms, which helps you to obtain better matches.
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank

# The TrigramSimilarity function is used to calculate the similarity between two strings based on trigram similarity.
from django.contrib.postgres.search import TrigramSimilarity

# Class based view to display a list of posts
class PostListView(ListView):

    '''
    The PostListView class is a subclass of Django's generic ListView class. 
    The ListView class inherits from multiple mixin classes that provide functionality to build views.
    Here queryset is used to retrieve the list of posts.
    context_object_name is used to set the variable to use in the template to display the list of posts.
    paginate_by is used to set the number of objects to include on each page.
    template_name is used to specify the template to use to render the list of posts.
    '''
    
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blogApplication/post/list.html'


# post_list takes an optional tag_slug parameter that allows us to filter posts by a tag. If the tag_slug parameter is provided, we will filter the posts by the tag with the given slug.
def post_list(request, tag_slug=None):
    # Instead of returning a list of all posts, we will return a paginated list of posts. We will use the Paginator class to paginate the list of posts. 
    # The Paginator class takes two arguments: the list of objects to paginate and the number of objects to include on each page.
    # We will include three posts on each page.

    post_list = Post.published.all()
    
    # The tag variable is used to store the Tag object that matches the given tag_slug. If the tag_slug parameter is not provided, the tag variable will be set to None.
    tag = None
    # If the tag_slug parameter is provided, we will filter the posts by the tag with the given slug.
    if tag_slug:
        # get_object_or_404() retrieves the Tag object with the given slug. If the tag does not exist, it will raise a 404 exception.
        tag = get_object_or_404(Tag, slug=tag_slug)
        # The filter() method is used to filter the posts by the tag. The __in field lookup is used to retrieve posts that contain the given tag.
        post_list = post_list.filter(tags__in=[tag])

    # Pagination: with 3 posts per page
    paginator = Paginator(post_list, 3)
    page_number = request.GET.get('page', 1)
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        # Pagination: If page_number is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # Pagination: If page_number is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)
    return render(request, 'blogApplication/post/list.html', {'posts': posts,'tag': tag})

# The post variable is passed to the slug parameter as a way to filter the Post objects by their slug field. It will return name of the post to the slug parameter.
def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post, status=Post.Status.PUBLISHED,
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    # List of active comments for this post
    comments = post.comments.filter(active=True)
    # Form for users to comment
    form = CommentForm()
    
    # The values_list() method is used to retrieve the IDs of the tags of the current post. 
    # The flat=True argument is used to return a flat list of values instead of a list of tuples.

    post_tags_ids = post.tags.values_list('id', flat=True)
    # We are retrieving all the posts that contain any of the tags of the current post, excluding the current post itself.
    similar_posts = Post.published.filter(tags__in=post_tags_ids)\
                                    .exclude(id=post.id)
    
    # Here annotate() is used to calculate the number of tags shared between the queried post and all the other posts.
    # This is done by using the Count aggregation function. The same_tags field is used to store the number of shared tags.
    # The order_by() method is used to order the posts by the number of shared tags in descending order.
    # If two posts have the same number of shared tags, the posts are ordered by the publish field in descending order.
  
    similar_posts = similar_posts.annotate(same_tags=Count('tags'))\
                                    .order_by('-same_tags','-publish')[:4]
    return render(request, 'blogApplication/post/detail.html', {'post': post, 'comments': comments,'form': form, 'similar_posts': similar_posts})



def post_share(request, post_id):

    '''
    The post_share view function takes the post_id parameter to retrieve the post object to share. 
    The post_id parameter is used to retrieve the post object from the database.
    The post object is then passed to the EmailPostForm form class.
    The form is validated using the is_valid() method. If the form is not valid, the form is rendered with the invalid data.
    If the form is valid, the data is retrieved from the form using the cleaned_data attribute.
    The send_mail() function is used to send the email. The send_mail() function takes the subject, message, from_email, to_email, and fail_silently arguments.
    The fail_silently argument is set to False to raise an exception if the email fails to send.
    The email is sent and the success message is displayed
    '''

    # Retrieve post by id
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    sent = False
    if request.method == 'POST':
        # Form was submitted
        form = EmailPostForm(request.POST) # Create form instance with the submitted data
        if form.is_valid():
            # Form fields passed validation
            cd = form.cleaned_data
            # request.build_absolute_uri() method is used to build the complete URL of the post
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recommends you read {post.title}"
            message = f"Read {post.title} at {post_url}\n\n" \
                      f"{cd['name']}\'s comments:  {cd['comments']}"
            send_mail(subject, message, 'programming.sunnyallana@gmail.com', [cd['to']])
            sent = True
    else:
        form = EmailPostForm() # Create a new form instance to display if a GET request is made
    return render(request, 'blogApplication/post/share.html', {'post': post, 'form': form, 'sent': sent})


# Django will throw a Http 405 if some other method is used to access the view
@require_POST
def post_comment(request,post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    comment = None
    # A comment was posted
    form = CommentForm(data=request.POST)
    if form.is_valid():
        # Create a Comment object without saving it to the database
        comment = form.save(commit=False)
        # Assign the post to the comment
        comment.post = post
        # Save the comment to the database
        comment.save()
    return render(request, 'blogApplication/post/comment.html',
                           {'post': post,
                            'form': form,
                            'comment': comment})



# POSTGRES_SEARCH: The post_search view function is used to implement full-text search functionality in the blog application.
def post_search(request):
    form = SearchForm()
    query = None
    results = []

    #  To check whether the form is submitted, we look for the query parameter in the request.GET dictionary. 

    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']

            #  We can pass a config attribute to SearchVector and SearchQuery to use a different search configuration.
                # search_vector = SearchVector('title', 'body', config='spanish')
                # search_query = SearchQuery(query, config='spanish')

            search_vector = SearchVector('title', weight='A') + SearchVector('body', weight='B')
            search_query = SearchQuery(query)

            # annotate() is used to add the search and rank fields to the queryset. The search field is used to store the search vector, and the rank field is used to store the search rank.

            # results = Post.published.annotate(
            #     search=search_vector,
            #     rank=SearchRank(search_vector, search_query)
            # ).filter(rank__gte=0.3).order_by('-rank')
    
            ''' Another search approach is trigram similarity. A trigram is a group of three consecutive characters. 
                You can measure the similarity of two strings by counting the number of trigrams that they share. 
                This approach turns out to be very effective for measuring the similarity of words in many languages.
                To use trigrams in PostgreSQL, you will need to install the pg_trgm extension first. 
            '''

            results = Post.published.annotate(similarity=TrigramSimilarity('title', query),).filter(similarity__gt=0.1).order_by('-similarity')

    return render(request,
                  'blogApplication/post/search.html',
                  {'form': form,
                   'query': query,
                   'results': results})