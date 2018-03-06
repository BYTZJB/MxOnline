#encoding=utf8

from django.conf.urls import url
from .views import OrgView, AddUserAskView, OrgHomePageView, OrgCourseView, OrgDescView, OrgTeachersView, \
    OrgTeacherListView, OrgTeacherDetailView, AddFavView

urlpatterns = [
    #课程机构列表页
    url(r'^list/$', OrgView.as_view(), name="org_list"),

    url(r'^add_ask/$', AddUserAskView.as_view(), name="add_ask"),
    url(r'^add_fav/$', AddFavView.as_view(), name="add_fav"),
    url(r'^home/(?P<org_id>\d+)$', OrgHomePageView.as_view(), name="home_page"),
    url(r'^course/(?P<org_id>\d+)$', OrgCourseView.as_view(), name="course_page"),
    url(r'^desc/(?P<org_id>\d+)$', OrgDescView.as_view(), name="desc_page"),
    url(r'^org_teacher/(?P<org_id>\d+)$', OrgTeachersView.as_view(), name="teachers_page"),

    #教师展示列表
    url(r'^teacher/list/$', OrgTeacherListView.as_view(), name="teachers_list"),
    #教师详情页面
    url(r'^teacher/detail/(?P<teacher_id>\d+)$', OrgTeacherDetailView.as_view(), name="teacher_detail"),
]