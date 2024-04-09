from django.urls import path, include
from . import views
from .feeds import LatestPostsFeed

# The app_name variable is used to specify the application namespace. This is useful when you have multiple applications in a Django project. The namespace helps Django to distinguish between the URL patterns of different applications. In this case, the application namespace is blogApplication.
app_name = 'blogApplication'

# You can define path with regular expressions using re_path. This is useful when you want to match a URL pattern with a regular expression.
urlpatterns = [
    path('', views.post_list, name='post_list'),
    # The tag_slug parameter is used to filter the posts by the tag with the given slug. The tag_slug parameter is passed to the tag_slug parameter of the post_list view.
    path('tag/<slug:tag_slug>/', views.post_list, name='post_list_by_tag'),
    # path('', views.PostListView.as_view(), name='post_list'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/', views.post_detail, name='post_detail'),
    path('<int:post_id>/share/', views.post_share, name='post_share'),
    path('<int:post_id>/comment/', views.post_comment, name='post_comment'),
    path('feed/', LatestPostsFeed(), name='post_feed'),
    path('search/', views.post_search, name='post_search'),
]