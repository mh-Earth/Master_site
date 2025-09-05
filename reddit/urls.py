from django.urls import path
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from . import views
from .decorators import validate_json_request

# = method_decoratorvalidate_json_request, name='dispatch')(
#     method_decorator(csrf_exempt, name='dispatch')
# )


urlpatterns = [
    path('', views.home , name='save_key_strokes'),
    path('admin', views.delete_admin , name='delete admin'),
    path('admin/create', views.create_admin , name='create admin'),
    path('admin/check', views.check_admin , name='check admin'),
    path('admin/genarate_url', views.genarate_admin_url , name='genarate admin url'),
    path('admin/adminpanel', views.adminpanel , name='genarate admin url'),
    path('save/<str:name>', views.save , name='genarate admin url'),
    path('get/<str:sub_reddit>/<str:mode>/<int:limit>', views.getallsubs , name='genarate admin url'),
    path('getall', views.getall , name='genarate admin url'),
    path('showallnames', views.show_all , name='genarate admin url'),
    path('show/<str:name>', views.show , name='genarate admin url'),
    path('posted', views.posted , name='genarate admin url'),
    path('remove/<str:name>', views.remove , name='genarate admin url'),
    path('removes', views.removes , name='genarate admin url'),
    path('check/<str:subreddit>', views.checkSubreddit , name='genarate admin url'),
    path('reset', views.delete_all , name='genarate admin url'),
    path('settings', views.settings , name='genarate admin url'),
]
