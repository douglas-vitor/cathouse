from django.urls import path
from django.urls import include
from django.views.generic.base import RedirectView
from .views import index
from .views import home
from .views import temp
from .views import tomada
from .views import camera
from .views import agendamento
from .views import updatealarm
from .views import dellalarm
from .views import dimmer
from .views import rgb

urlpatterns = [
        path('', RedirectView.as_view(url='login'), name="index"),
        path('home', home, name='home'),
        path('', include('django.contrib.auth.urls')),
        path('temperatura', temp, name='temperatura'),
        path('tomada', tomada, name='tomada'),
        path('camera', camera, name='câmera'),
        path('agendamento', agendamento, name='agendamento'),
	path('updatealarm/<int:id>', updatealarm, name='update alarm'),
        path('deletealarm/<int:id>', dellalarm, name='delete alarm'),
	path('dimmer', dimmer, name='dimmer'),
	path('rgb', rgb, name='rgb'),

]
