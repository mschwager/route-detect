from django.urls import include, path, re_path
from django.contrib.auth.decorators import login_required, permission_required
from django.views.generic import TemplateView

urlpatterns = [
    # ruleid: django-route-authenticated
    path('index/', login_required(views.index), name='main-view'),
    # ruleid: django-route-authenticated
    path('bio/<username>/', login_required(views.bio), name='bio'),
    # ruleid: django-route-authorized
    path('articles/<slug:title>/', permission_required('permission')(views.article), name='article-detail'),
    # ruleid: django-route-authenticated
    path('articles/<slug:title>/<int:section>/', login_required(views.section), name='article-section'),
    # ruleid: django-route-authenticated
    path('about/', login_required(TemplateView.as_view(template_name="about.html"))),
    # ruleid: django-route-unauthenticated
    path('about/', TemplateView.as_view(template_name="about.html")),
    # ruleid: django-route-unauthenticated
    path('blog/', include('blog.urls')),
    # ok: django-route-authenticated
    not_path('blog/', include('blog.urls')),
]

urlpatterns = [
    # ruleid: django-route-authenticated
    re_path(r'^index/$', login_required(views.index), name='index'),
    # ruleid: django-route-authenticated
    re_path(r'^bio/(?P<username>\w+)/$', login_required(views.bio), name='bio'),
    # ruleid: django-route-unauthenticated
    re_path(r'^blog/', include('blog.urls')),
    # ok: django-route-authenticated
    not_re_path('blog/', include('blog.urls')),
]
