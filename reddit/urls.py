from django.urls import path
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from . import views
from .decorators import validate_json_request

# = method_decoratorvalidate_json_request, name='dispatch')(
#     method_decorator(csrf_exempt, name='dispatch')
# )


urlpatterns = [
    path('', views.home , name=''),
    path('admin', views.delete_admin , name='delete admin'),
    path('admin/create', views.create_admin , name='create admin'),
    path('admin/check', views.check_admin , name='check admin'),
    path('admin/genarate_url', views.genarate_admin_url , name='genarate_admin_url'),
    path('admin/adminpanel', views.adminpanel , name='adminpanel'),
    path('save/<str:name>', views.save , name='save'),
    path('get/<str:sub_reddit>/<str:mode>/<int:limit>', views.getallsubs , name='d'),
    path('getall', views.getall , name='getall'),
    path('showallnames', views.show_all , name='show_all'),
    path('show/<str:name>', views.show , name='show'),
    path('posted', views.posted , name='posted'),
    path('remove/<str:name>', views.remove , name='remove'),
    path('removes', views.removes , name='removes'),
    path('check/<str:subreddit>', views.checkSubreddit , name='checkSubreddit'),
    path('reset', views.delete_all , name='delete_all'),
    path('settings', views.settings , name='settings'),
]
