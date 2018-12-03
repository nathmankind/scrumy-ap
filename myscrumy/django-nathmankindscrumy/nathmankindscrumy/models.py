from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django import forms


# Create your models here.
class GoalStatus(models.Model):
    status_name = models.CharField(max_length=100)

    def __str__(self):
        return self.status_name


class ScrumyGoals(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    goal_status = models.ForeignKey(GoalStatus, on_delete=models.PROTECT, related_name='nathmankindscrumy')
    goal_name = models.CharField(max_length=200)
    goal_id = models.IntegerField(default=0)
    created_by = models.CharField(max_length=100)
    moved_by = models.CharField(max_length=100)
    owner = models.CharField(max_length=100)

    def __str__(self):
        return 'Goal Name: ' + self.goal_name + \
               ', Created By: ' + self.created_by + ', Status: ' + str(self.goal_status)


class ScrumyHistory(models.Model):
    scrumy_goals = models.ForeignKey(ScrumyGoals, on_delete=models.PROTECT, related_name='goals')
    moved_by = models.CharField(max_length=100)
    created_by = models.CharField(max_length=100)
    moved_from = models.CharField(max_length=100)
    moved_to = models.CharField(max_length=100)
    time_of_action = models.DateTimeField(
        default=timezone.now
    )


class SignUpForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password']

class CreateGoalForm(forms.ModelForm):
    class Meta:
        model = ScrumyGoals
        fields = ['goal_name', 'user']
