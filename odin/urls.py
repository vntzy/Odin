from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin
from django.contrib.auth import views


urlpatterns = patterns('',
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^adminfiles/', include('adminfiles.urls')),
    url(r'^ckeditor/', include('ckeditor.urls')),

    url(r'^pages/', include('django.contrib.flatpages.urls')),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT}),

    url(r'^api/', include('odin.api', namespace='api')),
    url(r'^polls/', include('polls.urls', namespace='polls')),
    url(r'', include('website.urls')),
    url(r'', include('courses.urls', namespace='courses')),
    url(r'', include('faq.urls', namespace='faq')),
    url(r'', include('students.urls', namespace='students')),
    url(r'', include('applications.urls', namespace='applications')),
    url(r'^forum/', include('forum.urls', namespace='forum')),
    url(r'^stats/', include('statistics.urls', namespace='statistics')),

    url(r'^password_reset/$', views.password_reset, {'template_name': 'password_reset_form.html'}, name='password_reset'),
    url(r'^password_reset/done/$', views.password_reset_done, {'template_name': 'password_reset_done.html'}, name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.password_reset_confirm, {'template_name': 'password_reset_confirm.html'}, name='password_reset_confirm'),
    url(r'^reset/done/$', views.password_reset_complete, {'template_name': 'password_reset_final.html'}, name='password_reset_complete'),
)
