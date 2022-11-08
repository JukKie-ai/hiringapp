from . import views
from django.urls import path

app_name = 'team'

urlpatterns = [
    path('', views.indexView.as_view(), name="team"),
    path('register', views.registerView.as_view(), name="register"),
    path('login', views.loginView.as_view(), name="login"),
    path('<user>/createTeam', views.createTeamView.as_view(), name="createTeam"),
    path('<user>/editTeam', views.editTeamView.as_view(), name="editTeam"),
    path('<user>/team', views.teamTableView.as_view(), name="teamTableView"),
    path('<user>/teamView/<id>', views.teamView, name="teamView"),
    path('<user>/joinTeam/<id>', views.joinTeamView, name="joinTeam"),
    path('<user>/request', views.requestTeamView.as_view(), name="request"),
    path('<user>/studentList', views.studentListView.as_view(), name="studentList"),
    path('<user>/acceptRequest/<id>', views.acceptRequestView, name="acceptRequest"),
    path('<user>/members', views.memberListView, name="members"),
    path('<user>/kickMember/<id>', views.kickMemberView, name="kickMember"),
    path('<user>/leaveTeam', views.leaveTeamView.as_view(), name="leaveTeam"),
    path('<user>/deleteTeam', views.deleteTeamView.as_view(), name="deleteTeam"),
]
