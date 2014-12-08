from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'TweetMap.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    #url(r'^$', home),
    url(r'^tweet-sync/', 'TweetMap.views.tweet_sync', name='tweet-sync'),
    url(r'^get_recent_tweets/', 'twitter_service.views.get_recent_tweets'),
    url(r'^admin/', include(admin.site.urls)),
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += patterns('django.contrib.staticfiles.views',
        url(r'^static/(?P<path>.*)$', 'serve'),
    )