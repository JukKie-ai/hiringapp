from multiprocessing import context
from urllib.request import Request
from django.http import HttpResponseRedirect
from django.urls import reverse
from re import template
from django.shortcuts import redirect, render
from django.views import View
from django.db.models import F

from .filters import TeamFilter

from team.forms import UserForm
from team.models import Admin, RequestTeam, Student, Team, User

# Create your views here.
class indexView(View):
    template_name="team/index.html"

    def get(self, request):
        return render(request, self.template_name)

class registerView(View):
    template_name = "team/register.html"

    def get(self, request):
        return render(request, self.template_name)
    
    def post(self, request):
        formUser = UserForm(request.POST)

        user = formUser.save(commit=False)
        user.save()
        return redirect(reverse('team:login'))

class loginView(View):
    template_name="team/login.html"

    def get(self, request):
        return render(request, self.template_name)
    
    def post(self, request):
        uname = request.POST.get('username')
        pwd = request.POST.get('password')

        if User.objects.filter(pk=uname):
            account = User.objects.get(pk=uname)
            
            if account.password == pwd:
                return redirect(reverse('team:teamTableView', kwargs={'user': uname}))
            else:
                return render(request, self.template_name)
        else:
            account = Admin.objects.get(pk=uname)

            if account.password == pwd:
                return redirect(reverse('team:admin', kwargs={'user': uname}))
            else:
                return render(request, self.template_name)

        return render(request, self.template_name)

class adminView(View):
    template_name="team/adminView.html"

    def get(self, request, user):
        team = Team.objects.all()

        myFilter = TeamFilter(request.GET, queryset=team)
        team = myFilter.qs

        return render(request, self.template_name, {'user':user, 'team': team, 'myFilter': myFilter})

class createTeamView(View):
    template_name="team/createTeam.html"

    def get(self, request, user):
        return render(request, self.template_name, {'user': user})
    
    def post(self, request, user):
        description = request.POST.get('description')
        max_members = request.POST.get('max_members')
        section = request.POST.get('section')
        founder = User.objects.get(pk=user)

        founder.status = True

        createTeam = Team(founder=founder, description=description, section=section, members=0, max_members=max_members)

        founder.save()
        createTeam.save()

        return redirect(reverse('team:teamTableView', kwargs={'user': user}))

class editTeamView(View):
    template_name="team/editTeam.html"

    def get(self, request, user):
        team = Team.objects.get(founder=user)
        return render(request, self.template_name, {'user': user, 'team':team})
    
    def post(self, request, user):
        teamID = Team.objects.get(founder=user)
        description = request.POST.get('description')
        max_members = request.POST.get('max_members')
        section = request.POST.get('section')
        #founder = User.objects.get(pk=user)

        Team.objects.filter(founder=user).update(description=description, section=section, max_members=max_members)

        return redirect(reverse('team:teamTableView', kwargs={'user': user}))

class teamTableView(View):
    template_name="team/team.html"

    def get(self, request, user):
        teamList = Team.objects.all()
        loggedUser = User.objects.get(pk=user)

        myFilter = TeamFilter(request.GET, queryset=teamList)
        teamList = myFilter.qs

        if Team.objects.filter(founder=user):
            team = Team.objects.get(founder=user)
            current_members = Team.objects.values_list('members').get(founder=user)
            max_members = Team.objects.values_list('max_members').get(founder=user)

            if RequestTeam.objects.filter(teamID=team.teamID).count() != 0:
                req = RequestTeam.objects.filter(teamID=team.teamID)

                return render(request, self.template_name, {'teamList': teamList, 'user':user, 'team': team, 'current_members': current_members, 'max_members': max_members, 'loggedUser': loggedUser, 'myFilter':myFilter, 'req': req})
            else:
                return render(request, self.template_name, {'teamList': teamList, 'user':user, 'team': team, 'current_members': current_members, 'max_members': max_members,  'loggedUser': loggedUser, 'myFilter':myFilter})
        elif Student.objects.filter(username=loggedUser).count() != 0:
            student = Student.objects.get(username=loggedUser)
            members = Student.objects.filter(team=student.team.teamID)
            return render(request, self.template_name, {'teamList': teamList, 'user':user, 'loggedUser': loggedUser, 'student': student, 'members':members, 'myFilter':myFilter})
        else:
            return render(request, self.template_name, {'teamList': teamList, 'user':user, 'loggedUser': loggedUser, 'myFilter':myFilter})

def teamView(request, id, user):
    team = Team.objects.get(pk=id)
    members = Student.objects.filter(team=team.teamID)

    return render(request, "team/teamView.html", {'team': team, 'user': user, 'members':members})

def adminTeamView(request, id, user):
    team = Team.objects.get(pk=id)
    members = Student.objects.filter(team=team.teamID)

    return render(request, "team/adminTeamView.html", {'team': team, 'user': user, 'members':members})

def deleteAdminTeamView(request, id, user):
    team = Team.objects.get(pk=id)
    members = Student.objects.filter(team=team.teamID)

    if request.method == 'POST':
        Team.objects.get(pk=id).delete()

        return redirect(reverse('team:admin', kwargs={'user': user}))

    return render(request, 'team/deleteAdminTeamView.html', {'user':user, 'team':team, 'members':members})


def joinTeamView(request, id, user):
    team = Team.objects.get(pk=id)
    username = User.objects.get(pk=user)

    context = {'user': user, 'team':team, 'username': username}

    if request.method == 'POST':
        reason = request.POST.get('reason')

        requestForm = RequestTeam(username=username, teamID=team, reason=reason)

        requestForm.save()
        return redirect(reverse('team:teamTableView', kwargs={'user': user}))

    return render(request, 'team/joinTeam.html', context)

class requestTeamView(View):
    template_name="team/request.html"

    def get(self, request, user):
        team = Team.objects.get(founder=user)

        if RequestTeam.objects.all().count() == 0:
            return render(request, "team/norequest.html", {'team': team, 'user':user})
        else:
            teamID = RequestTeam.objects.filter(teamID=team.teamID)

            return render(request, self.template_name, {'team': team, 'user':user, 'teamID':teamID})

class studentListView(View):
    template_name="team/studentList.html"

    def get(self, request, user):
        team = Team.objects.all()
        student = Student.objects.all()
        noteam = User.objects.filter(status=False)
        return render(request, self.template_name, {'team':team, 'student': student, 'user':user, 'noteam':noteam})

def acceptRequestView(request, id, user):
    req = RequestTeam.objects.get(pk=id)

    context = {'user': user, 'req':req}

    if request.method == 'POST':
        requestForm = Student(username=req.username, team=req.teamID)
        User.objects.filter(pk=req.username.username).update(status=True)
        Team.objects.filter(teamID=req.teamID.teamID).update(members=F('members')+1)
        
        requestForm.save()
        RequestTeam.objects.filter(pk=id).delete()
        RequestTeam.objects.filter(username=req.username).delete()
        return redirect(reverse('team:teamTableView', kwargs={'user': user}))

    return render(request, 'team/acceptRequest.html', context)

def memberListView(request, user):
    team = Team.objects.get(founder=user)
    members = Student.objects.filter(team=team.teamID)

    return render(request, "team/memberList.html", {'user': user, 'team': team, 'members': members})

def kickMemberView(request, id, user):
    team = Student.objects.get(pk=id)

    context = {'user':user, 'team':team}

    if request.method == 'POST':
        User.objects.filter(pk=team.username.username).update(status=False)
        Team.objects.filter(teamID=team.team.teamID).update(members=F('members')-1)

        Student.objects.get(pk=id).delete()

        return render(request, 'team/memberList.html', context)
    
    return render(request, 'team/kickMember.html', context)

class leaveTeamView(View):
    template_name="team/leaveTeam.html"

    def get(self, request, user):
        team = Team.objects.get(founder=user)

        if Student.objects.filter(team=team.teamID).count() != 0:
            student = Student.objects.filter(team=team.teamID)

            return render(request, self.template_name, {'user':user, 'student':student})
        else:
            return redirect(reverse('team:deleteTeam', kwargs={'user': user}))
    
    def post(self, request, user):
        team = Team.objects.get(founder=user)
        studentID = request.POST.get('studentList')
        newLeader = User.objects.get(pk=studentID)

        User.objects.filter(pk=user).update(status=False)
        Team.objects.filter(founder=user).update(founder=newLeader.username)
        Student.objects.get(username=newLeader.username).delete()
        Team.objects.filter(teamID=team.teamID).update(members=F('members')-1)
        

        return redirect(reverse('team:teamTableView', kwargs={'user': user}))

class deleteTeamView(View):
    template_name="team/deleteTeam.html"

    def get(self, request, user):
        return render(request, self.template_name, {'user':user})
    
    def post(self, request, user):

        Team.objects.get(founder=user).delete()
        User.objects.filter(pk=user).update(status=False)

        return redirect(reverse('team:teamTableView', kwargs={'user': user}))