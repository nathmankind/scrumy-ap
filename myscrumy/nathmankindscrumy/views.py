from django.template import loader
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import Group
from django.contrib.auth import login, authenticate
from .models import GoalStatus
from .models import ScrumyGoals
from .models import CreateGoalForm
from .models import SignUpForm
from .models import ChangeGoalForm, AdminChangeGoalForm, QAChangeGoalForm
from rest_framework import viewsets
from rest_framework.response import Response
from .serializers import UserSerializer, ScrumUserSerializer, ScrumGoalSerializer
from .models import User
from random import randint


# Create your views here.


def index(request):
    current_user = request.user
    w_goals = GoalStatus.objects.get(pk=8)
    daily_goals = GoalStatus.objects.get(pk=9)
    verify_goals = GoalStatus.objects.get(pk=10)
    done_goals = GoalStatus.objects.get(pk=11)
    template = loader.get_template("nathmankindscrumy/home.html")
    context = {'w_goals': w_goals, 'daily_goals': daily_goals,
               'verify_goals': verify_goals, 'done_goals': done_goals,
               'current_user': current_user}
    return HttpResponse(template.render(context, request))
    # output = ScrumyGoals.objects.filter(goal_name="Learn Django")


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            group = form.cleaned_data['group_choices']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()
            user_group = Group.objects.get(id=int(group))
            user_group.user_set.add(user)
            user = authenticate(username=username, password=password)
            login(request, user)

            return redirect('nathmankindscrumy:success')
    else:
        form = SignUpForm()
    return render(request, 'nathmankindscrumy/signup.html', {'form': form})


def move_goal(request, id):
    current_user = request.user
    usr_grp = request.user.groups.all()[0]
    goals = get_object_or_404(ScrumyGoals, pk=id)
    if usr_grp == Group.objects.get(name='Developer') and current_user == goals.user:
        if request.method == 'POST':
            form = ChangeGoalForm(request.POST)
            if form.is_valid():
                selected_status = form.save(commit=False)
                selected = form.cleaned_data['goal_status']
                # get_status = selected_status.goal_status
                choice = GoalStatus.objects.get(id=int(selected))
                goals.goal_status = choice
                goals.save()
                return redirect('nathmankindscrumy:goal_success')
        else:
            form = ChangeGoalForm()

    elif usr_grp == Group.objects.get(name='Admin') or usr_grp == Group.objects.get(name='Owner'):
        if request.method == 'POST':
            form = AdminChangeGoalForm(request.POST)
            if form.is_valid():
                selected_status = form.save(commit=False)
                get_status = selected_status.goal_status
                goals.goal_status = get_status
                goals.save()
                return redirect('nathmankindscrumy:goal_success')
        else:
            form = AdminChangeGoalForm()

    elif usr_grp == Group.objects.get(name='Quality Assurance'):
        if request.method == 'POST':
            form = QAChangeGoalForm(request.POST)
            if form.is_valid():
                selected_status = form.save(commit=False)
                selected = form.cleaned_data['goal_status']
                # get_status = selected_status.goal_status
                choice = GoalStatus.objects.get(id=int(selected))
                goals.goal_status = choice
                goals.save()
                return redirect('nathmankindscrumy:goal_success')
        else:
            form = QAChangeGoalForm()
    else:
        return redirect('nathmankindscrumy:error')
    return render(request, 'nathmankindscrumy/move_goal.html',
                  {'form': form, 'goals': goals, 'current_user': current_user})

    # def move_goal(request, goal_id):
    # goals = get_object_or_404(ScrumyGoals, pk=goal_id)
    # return render(request, 'nathmankindscrumy/exception.html', {'goals': goals})
    # return HttpResponse("You are looking at goal %s." % goal_id)


def add_goal(request):
    current_user = request.user
    usr_grp = request.user.groups.all()[0]
    dev_grp = Group.objects.get(name='Developer')
    if request.method == 'POST':
        form = CreateGoalForm(request.POST)
        if form.is_valid():
            goal = form.save(commit=False)
            goal.user = current_user
            if usr_grp == Group.objects.get(name='Developer'):
                goal.goal_status = GoalStatus.objects.get(id=8)
            else:
                goal.goal_status = GoalStatus.objects.get(id=8)
            goal.save()

            return redirect('nathmankindscrumy:add_goal_success')
    else:
        form = CreateGoalForm()
    return render(request, 'nathmankindscrumy/add_goal.html', {'form': form,
                                                               'current_user': current_user,
                                                               'dev_grp': dev_grp})


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


# ====== VIEWSET =======
class UserViewSet(viewsets.ViewSet):
    def list(self, request):
        queryset = User.objects.all()
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)


class ScrumUserViewSet(viewsets.ViewSet):
    def list(self, request):
        queryset = ScrumyGoals.objects.all()
        serializer = ScrumUserSerializer(queryset, many=True)
        return Response(serializer.data)


class ScrumGoalViewSet(viewsets.ViewSet):
    def list(self, request):
        queryset = ScrumyGoals.objects.all()
        serializer = ScrumGoalSerializer(queryset, many=True)
        return Response(serializer.data)


# ==== VIEWSET ENDS ====== #

def home(request):
    return HttpResponse(ScrumyGoals.objects.filter(goal_name="Learn Django"))


def success(request):
    return render(request, 'nathmankindscrumy/success_page.html', {})


def error(request):
    current_user = request.user
    return render(request, 'nathmankindscrumy/error.html', {'current_user': current_user})


def move_goal_success(request):
    current_user = request.user
    return render(request, 'nathmankindscrumy/move_goal_success.html', {'current_user': current_user})


def goal_add(request):
    current_user = request.user
    return render(request, 'nathmankindscrumy/goal_add.html', {'current_user': current_user})