from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^create_sale/((?P<sale_id>.+)/)?$', views.create_sale, name='create_sale'),
    url(r'^view_sale/((?P<vid>.+)/)?$', views.view_sale, name='view_sale'),
    url(r'^login',views.login_user, name='login'),
    url(r'^logout/$','django.contrib.auth.views.logout', {'template_name':'logout.html'}),
    url(r'^register',views.register, name='register'),
]
