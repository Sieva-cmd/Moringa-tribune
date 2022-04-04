from django.urls import path,re_path
from django.conf import settings
from django.conf.urls.static import static


from . import views
import news


urlpatterns =[
            # path('',views.welcome,name ='welcome'),
            path('',views.news_of_today,name='newsToday'),
            re_path(r'^archives/(\d{4}-\d{2}-\d{2})/$',views.past_days_news,name = 'pastNews'),
            re_path(r'search/',views.search_results,name='search_results'),
            re_path(r'^article/(\d+)',views.article,name ='article'),
            re_path(r'register/', views.register_request, name="register"),
            re_path(r'login/', views.login_request, name="login"),
            re_path(r'logout', views.logout_request, name= "logout"),
            re_path(r'^new/article$', views.new_article, name='new-article'),
            re_path(r'password_reset', views.password_reset_request, name="password_reset")
            ]
if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)            
