from django.urls import include, path
from . import views

app_name = 'nathmankindscrumy'
urlpatterns = [
    path('', views.index, name='index'),

    #path for goal_id
    path('movegoal/<int:goal_id>', views.move_goal, name='movegoal'),

    #path for add goal
    path('addgoal', views.add_goal, name="add_goal"),

    path('accounts/', include('django.contrib.auth.urls')),

    #path for home
    path('home', views.home, name='home'),

    #path for User sign up
    path('signup', views.signup, name='signup'),

    #path for signup success
    path('success', views.success, name='success')
]
