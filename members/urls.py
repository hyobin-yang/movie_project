# from django.urls import path
# from .views import *

# app_name = 'members'

# urlpatterns = [
#     path('login/', login),
#     path('signup/', signup),
#     path('logout/', logout),
# ]


##

from django.urls import path, include

from .views import NicknameUniqueCheck

app_name = 'members'

urlpatterns = [
    # path('login/', login),
    # path('signup/', signup),
    # path('logout/', logout),
    path('', include('dj_rest_auth.urls')),
    path('signup/', include('dj_rest_auth.registration.urls')),
    # path('uniquecheck/username/', UsernameUniqueCheck.as_view(), name='uniquecheck_username'),
    path('uniquecheck/nickname/', NicknameUniqueCheck.as_view(), name='uniquecheck_nickname'),
]