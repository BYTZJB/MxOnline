#encoding=utf8
import json

from django.core.paginator import PageNotAnInteger
from django.http import HttpResponse
from pure_pagination import Paginator
from django.shortcuts import render
# Create your views here.
from django.views.generic.base import View

from operation.models import UserFavorite, CourseComments, UserCourse
from .models import Course, CourseResource
from utils.mixin_utils import LoginRequiredMixin


class CourseListView(View):
    def get(self, request):
        all_courses = Course.objects.all().order_by("-add_time")
        hot_courses = Course.objects.all().order_by("-click_nums")[:3]
        sort = request.GET.get("sort", "")
        if sort:
            if sort == "students":
                all_courses = all_courses.order_by("-students")
            if sort == "hot":
                all_courses = all_courses.order_by("-click_nums")
        # 对课程进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_courses, 3, request=request )
        courses = p.page(page)
        return render(request, 'course-list.html', {
            "all_courses": courses,
            "sort": sort,
            "hot_courses": hot_courses,
        })

class CourseDetailView(View):
    def get(self, request, course_id):
        course = Course.objects.get(id= int(course_id))
        # 增加课程点击数
        course.click_nums += 1
        course.save()

        has_fav_course = False
        has_fav_org = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id = int(course_id), fav_type=1):
                has_fav_course = True
            if UserFavorite.objects.filter(user=request.user, fav_id = course.course_org.id, fav_type=2):
                has_fav_org = True
        tag = course.tag
        if tag:
            relate_courses = Course.objects.filter(tag = tag)[:1]
        else:
            relate_courses = []
        return render(request, "course-detail.html", {
            "course": course,
            "relate_courses": relate_courses,
            "has_fav_course": has_fav_course,
            "has_fav_org": has_fav_org,
        })

class CourseInfoView(LoginRequiredMixin, View):
    """
    课程章节信息
    """
    def get(self, request, course_id):
        course = Course.objects.get(id = int(course_id))
        all_resources = CourseResource.objects.filter(course=course )

        #查询用户是否已经关联了该课程
        user_courses = UserCourse.objects.filter(user=request.user, course=course)
        if not user_courses:
            user_course = UserCourse(user=request.user, course=course)
            user_course.save()

        user_courses = UserCourse.objects.filter(course=course)
        user_ids = [user_course.user.id for user_course in user_courses]
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        # 取出所有的课程id
        course_ids = [user_course.id for user_course in all_user_courses]
        relate_courses = Course.objects.filter(id__in=course_ids).order_by('-click_nums')[:5]
        return render(request, "course-video.html", {
            "course": course,
            "course_resources": all_resources,
            "relate_courses": relate_courses,
        })

class CourseCommentView(LoginRequiredMixin, View):
    """
    课程评论信息
    """
    def get(self, request, course_id):
        course = Course.objects.get(id = int(course_id))
        all_resources = CourseResource.objects.filter(course=course )
        all_comments = CourseComments.objects.filter(course=course)

        user_courses = UserCourse.objects.filter(course=course)
        user_ids = [user_course.id for user_course in user_courses]
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        # 取出所有的课程id
        course_ids = [user_course.id for user_course in all_user_courses]
        relate_courses = Course.objects.filter(id__in=course_ids).order_by('-click_nums')[:5]
        return render(request, "course-comment.html", {
            "course": course,
            "all_resources": all_resources,
            "all_comments": all_comments,
            "relate_courses": relate_courses,
        })

class CourseAddCommentView(View):
    """
    添加课程评论信息
    """
    def post(self, request):
        if not request.user.is_authenticated():
            return HttpResponse(json.dumps({"status": "fail", "msg": "用户未登录"}), content_type="application/json")
        course_id = int(request.POST.get("course_id"))
        comment = request.POST.get("comments", "")
        if not comment:
            return HttpResponse(json.dumps({"status": "fail", "msg": "评论内容为空"}), content_type="application/json")
        course = Course.objects.get(id = course_id)
        course_comment = CourseComments(user=request.user, course=course, comments=comment)
        course_comment.save()
        return HttpResponse(json.dumps({"status": "success", "msg": "评论添加成功"}), content_type="application/json")


