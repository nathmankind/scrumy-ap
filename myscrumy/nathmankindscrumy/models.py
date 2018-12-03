from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django import forms
from django.contrib.auth.models import Group, Permission


admin_grp = Group.objects.get(pk=2)
dev_grp = Group.objects.get(pk=1)
qa_grp = Group.objects.get(pk=3)
owner_grp = Group.objects.get(pk=4)

# === PERMISSION ===

admin_perm = Permission.objects.all()
dev_perm = Permission.objects.get(name='Can add scrumy goals')
qa_perm = Permission.objects.get(name='Can change goal status')
owner_perm = Permission.objects.get(name='Can add scrumy goals')

# === ASSIGN PERMISSIONS TO GROUPS
# admin_grp.permissions.add(admin_perm)
# dev_grp.permissions.add(dev_perm)
# qa_grp.permissions.add(qa_perm)
# owner_grp.permissions.add(owner_perm)


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
    group_choices = forms.ChoiceField(choices=[(choice.pk, choice) for choice in Group.objects.all()],
                                      widget=forms.RadioSelect)
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password', 'group_choices']

    def save(self, commit=True):
        return super(SignUpForm, self).save(commit=commit)


class CreateGoalForm(forms.ModelForm):
        class Meta:
            model = ScrumyGoals
            fields = ['goal_name', 'goal_id', 'created_by', 'moved_by', 'owner']


class ChangeGoalForm(forms.ModelForm):
    queryset = GoalStatus.objects.all()
    goal_status = forms.ChoiceField(choices=[(choice.pk, choice) for choice in queryset[:2]])

    class Meta:
        model = GoalStatus
        fields = ['goal_status']


class AdminChangeGoalForm(forms.ModelForm):
    class Meta:
        model = ScrumyGoals
        fields = ['goal_status']


class QAChangeGoalForm(forms.ModelForm):
    queryset = GoalStatus.objects.all()
    goal_status = forms.ChoiceField(choices=[(choice.pk, choice) for choice in queryset.order_by('-id')[:2][::-1]])

    class Meta:
        model = GoalStatus
        fields = ['goal_status']


# class OwnerChangeGoalForm(forms.ModelForm):
#     queryset = GoalStatus.objects.all()
#     goal_status = forms.ChoiceField(choices=[(choice.pk, choice) for choice in queryset.order_by('-id')[:2]])
#
#     class Meta:
#         model = GoalStatus
#         fields = ['goal_status']