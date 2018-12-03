from django.template import loader
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import Group
from .models import GoalStatus
from .models import ScrumyGoals
from .models import CreateGoalForm
from .models import SignUpForm
from .models import User
from random import randint
# Create your views here.


def index(request):
    w_goals = GoalStatus.objects.get(pk=8)
    daily_goals = GoalStatus.objects.get(pk=9)
    verify_goals = GoalStatus.objects.get(pk=10)
    done_goals = GoalStatus.objects.get(pk=11)
    template = loader.get_template("nathmankindscrumy/home.html")
    context = {'w_goals': w_goals, 'daily_goals': daily_goals,
               'verify_goals': verify_goals, 'done_goals': done_goals}
    return HttpResponse(template.render(context, request))
    #output = ScrumyGoals.objects.filter(goal_name="Learn Django")


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()
            dev_group = Group.objects.get(name='Developer')
            dev_group.user_set.add(user)
            return redirect('nathmankindscrumy:success')
    else:
        form = SignUpForm()
    return render(request, 'nathmankindscrumy/signup.html',  {'form': form})


def move_goal(request, goal_id):
    goals = get_object_or_404(ScrumyGoals, pk=goal_id)
    return render(request, 'nathmankindscrumy/exception.html', {'goals': goals})
    # return HttpResponse("You are looking at goal %s." % goal_id)


def add_goal(request):
    if request.method == 'POST':
        form = CreateGoalForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.save()
    else:
        form = CreateGoalForm()
    return render(request, 'nathmankindscrumy/add_goal.html',  {'form': form})
# def add_goal(request):
#     week = GoalStatus.objects.get(id=8)
#     user = User.objects.get(id=4)
#     new_goal = ScrumyGoals.objects.create(goal_name="Keep Learning Django",
#                                           goal_id=randint(1000, 9999),
#                                           created_by="Louis", moved_by="Louis",
#                                           owner="Louis", goal_status=week,
#                                           user=user)
#     new_goal.save()
#     goals = ScrumyGoals.objects.all()
#     output = ','.join([x.goal_name for x in goals])
#     return HttpResponse(output)


def home(request):
    return HttpResponse(ScrumyGoals.objects.filter(goal_name="Learn Django"))


def success(request):
    return render(request, 'nathmankindscrumy/success_page.html', {})