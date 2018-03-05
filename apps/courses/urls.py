#encoding=utf8

from django.conf.urls import url

from courses.views import CourseListView, CourseDetailView, CourseInfoView, CourseCommentView, CourseAddCommentView

urlpatterns = [
    #课程列表
    url(r'^list/$', CourseListView.as_view(), name="course_list"),
    url(r'^detail/(?P<course_id>\d+)$', CourseDetailView.as_view(), name="course_detail"),
    url(r'^info/(?P<course_id>\d+)$', CourseInfoView.as_view(), name="course_info"),
    url(r'^comment/(?P<course_id>\d)$', CourseCommentView.as_view(), name="course_comment"),
    url(r'^add_comment', CourseAddCommentView.as_view(), name="course_add_comment")

]
