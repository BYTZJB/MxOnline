#encoding=utf8

from django.conf.urls import url

from courses.views import CourseListView, CourseDetailView

urlpatterns = [
    #课程列表
    url(r'^list/$', CourseListView.as_view(), name="course_list"),
    url(r'^detail/(?P<course_id>\d+)$', CourseDetailView.as_view(), name="course_detail")
]
