from rest_framework.routers import DefaultRouter
from . import views

route = DefaultRouter()

route.register('',views.UserManageBooksViewset,basename='managebook')




urlpatterns = []+route.urls
