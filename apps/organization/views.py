# encoding=utf8
import json

from django.core.paginator import PageNotAnInteger
from django.shortcuts import render, render_to_response
from django.views.generic import View
from django.http import HttpResponse
from pure_pagination import Paginator

from courses.models import Course
from operation.models import UserFavorite
from organization.forms import UserAskForm
from .models import CourseOrg, CityDict, Teacher


# Create your views here.

class OrgView(View):
    """
    课程机构列表功能
    """

    def get(self, request):
        # 课程机构
        all_orgs = CourseOrg.objects.all()
        hot_orgs = all_orgs.order_by("-click_nums")[:5]

        # 城市
        all_citys = CityDict.objects.all()

        # 取出筛选城市
        city_id = request.GET.get('city', "")
        if city_id:
            all_orgs = all_orgs.filter(city_id=int(city_id))

        # 类别筛选
        category = request.GET.get('ct', "")
        if category:
            all_orgs = all_orgs.filter(category=category)

        sort = request.GET.get("sort", "")
        if sort:
            if sort == "students":
                all_orgs = all_orgs.order_by("-students")
            elif sort == "courses":
                all_orgs = all_orgs.order_by("-course_nums")

        # 对课程机构进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        # Provide Paginator with the request object for complete querystring generation

        p = Paginator(all_orgs, 5, request=request)

        orgs = p.page(page)
        org_nums = all_orgs.count()

        return render(request, "org-list.html", {
            "all_orgs": orgs,
            "all_citys": all_citys,
            "org_nums": org_nums,
            "city_id": city_id,
            "category": category,
            "hot_orgs": hot_orgs,
            "sort": sort,
        })


class AddUserAskView(View):
    """
    用户添加咨询
    """

    def post(self, request):
        userask_form = UserAskForm(request.POST)
        if userask_form.is_valid():
            user_ask = userask_form.save(commit=True)
            return HttpResponse("{'status': 'success'}", content_type='application/json')
        else:
            return HttpResponse("{'status': 'fail', 'msg':{0}}".format(userask_form.errors), content_type='application/json')


class OrgHomePageView(View):
    """
    机构首页
    """

    def get(self, request, org_id):
        current_page = "home_page"
        course_org = CourseOrg.objects.get(id=int(org_id))
        all_courses = course_org.course_set.all()[:3]
        all_teachers = course_org.teacher_set.all()[:1]
        fav_has = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user = request.user, fav_id=int(org_id), fav_type=2):
                fav_has = True
        return render(request, "org-detail-homepage.html", {
            "org_id": org_id,
            "current_page": current_page,
            "org": course_org,
            "all_courses": all_courses,
            "all_teachers": all_teachers,
            "fav_has": fav_has,
        })

class OrgCourseView(View):
    """
    机构课程列表页
    """

    def get(self, request, org_id):
        current_page = "course_page"
        course_org = CourseOrg.objects.get(id=int(org_id))
        all_courses = course_org.course_set.all()
        fav_has = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user = request.user, fav_id=int(org_id), fav_type=2):
                fav_has = True
        return render(request, "org-detail-course.html", {
            "org_id": org_id,
            "current_page": current_page,
            "org": course_org,
            "all_courses": all_courses,
            "fav_has": fav_has,
        })

class OrgDescView(View):
    """
    机构介绍项
    """

    def get(self, request, org_id):
        current_page = "desc_page"
        course_org = CourseOrg.objects.get(id=int(org_id))
        fav_has = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user = request.user, fav_id=int(org_id), fav_type=2):
                fav_has = True
        return render(request, "org-detail-desc.html", {
            "org_id": org_id,
            "current_page": current_page,
            "org": course_org,
            "fav_has": fav_has,
        })

class OrgTeachersView(View):
    """
    机构教师项
    """
    def get(self, request, org_id):
        current_page = "teachers_page"
        course_org = CourseOrg.objects.get(id=int(org_id))
        teachers = course_org.teacher_set.all()
        fav_has = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user = request.user, fav_id=int(org_id), fav_type=2):
                fav_has = True
        return render(request, "org-detail-teachers.html", {
            "org_id": org_id,
            "current_page": current_page,
            "teachers": teachers,
            "fav_has": fav_has,
        })

class AddFavView(View):
    """
    用户收藏
    """
    def post(self, request):
        fav_id = request.POST.get("fav_id", 0)
        fav_type = request.POST.get("fav_type", 0)

        if not request.user.is_authenticated():
            # 判断用户登录状态
            return HttpResponse(json.dumps({'status': 'fail', 'msg':'用户未登录'}), content_type='application/json')
        exist_records = UserFavorite.objects.filter(user=request.user, fav_id=int(fav_id), fav_type=fav_type)
        if exist_records:
            # 如果记录已经存在, 则表示用户取消收藏
            exist_records.delete()
            return HttpResponse(json.dumps({'status': 'success', 'msg':'收藏'}) , content_type='application/json')
        else:
            user_fav = UserFavorite()
            if int(fav_id) > 0 and int(fav_type) > 0:
                user_fav.user = request.user
                user_fav.fav_id = int(fav_id)
                user_fav.fav_type = int(fav_type)
                user_fav.save()
                return HttpResponse(json.dumps({'status': 'success', 'msg':'已收藏'}), content_type='application/json')
            else:
                return HttpResponse(json.dumps({'status': 'fail', 'msg':'收藏出错'}),  content_type='application/json')

