#encoding=utf8

from django.conf.urls import url

from courses.views import CourseListView

urlpatterns = [
    #课程列表
    url(r'^list/$', CourseListView.as_view(), name="course_list") ## ToDo

]
