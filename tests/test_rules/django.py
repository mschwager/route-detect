from django.urls import include, path, re_path

urlpatterns = [
    # ruleid: django-route-authenticated
    path('index/', views.index, name='main-view'),
    # ruleid: django-route-authenticated
    path('bio/<username>/', views.bio, name='bio'),
    # ruleid: django-route-authenticated
    path('articles/<slug:title>/', views.article, name='article-detail'),
    # ruleid: django-route-authenticated
    path('articles/<slug:title>/<int:section>/', views.section, name='article-section'),
    # ruleid: django-route-authenticated
    path('blog/', include('blog.urls')),
    # ok: django-route-authenticated
    not_path('blog/', include('blog.urls')),
]

urlpatterns = [
    # ruleid: django-route-authenticated
    re_path(r'^index/$', views.index, name='index'),
    # ruleid: django-route-authenticated
    re_path(r'^bio/(?P<username>\w+)/$', views.bio, name='bio'),
    # ruleid: django-route-authenticated
    re_path(r'^blog/', include('blog.urls')),
    # ok: django-route-authenticated
    not_re_path('blog/', include('blog.urls')),
]
