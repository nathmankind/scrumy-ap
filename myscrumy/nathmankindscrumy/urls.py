from django.urls import include, path
from . import views

app_name = 'nathmankindscrumy'
urlpatterns = [
    path('', views.index, name='index'),

    #path for goal_id
    #path('movegoal/<int:goal_id>', views.move_goal, name='movegoal'),
    path('movegoal/<int:id>', views.move_goal, name='movegoal'),

    #path for add goal
    path('addgoal', views.add_goal, name="add_goal"),

    path('accounts/', include('django.contrib.auth.urls'), name='login'),

    #path for home
    path('home', views.home, name='home'),

    #path for User sign up
    path('signup', views.signup, name='signup'),

    #path for signup success
    path('success', views.success, name='success'),

    #path for error page
    path('error', views.error, name='error'),

    #path for moved goal success page
    path('goal_success', views.move_goal_success, name='goal_success'),

    #path for error page
    path('add_goal_success', views.goal_add, name='add_goal_success')
]
