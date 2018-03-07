# encoding=utf8
import json

from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.hashers import make_password
from django.core.paginator import PageNotAnInteger
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.db.models import Q
from pure_pagination import Paginator

# Create your views here.
from django.views.generic.base import View

from courses.models import Course
from operation.models import UserCourse, UserFavorite, UserMessage
from organization.models import Teacher, CourseOrg
from utils.email_send import send_register_email
from utils.mixin_utils import LoginRequiredMixin
from .forms import LoginForm, RegisterForm, ForgetForm, UploadImageForm, ModifyPasswordForm, UserInfoForm
from .models import UserProfile, EmailVerifyRecord


class CustomBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class LoginView(View):
    def get(self, request):
        return render(request, "login.html", {})

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = request.POST.get("username", "")
            password = request.POST.get("password", "")
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                return render(request, "index.html")
            else:
                return render(request, "login.html", {"msg": "用户名或者密码错误!"})
        else:
            return render(request, "login.html", {"login_form": login_form})


class RegisterView(View):
    def get(self, request):
        register_form = RegisterForm()
        return render(request, "register.html", {"register_form": register_form})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_name = request.POST.get("email", "")
            if UserProfile.objects.filter(email=user_name):
                return render(request, "register.html", {"msg": "用户已经是已经存在的", "register_form": register_form})
            pass_word = request.POST.get("password", "")
            user_profile = UserProfile()
            user_profile.username = user_name
            user_profile.email = user_name
            user_profile.is_active = False
            user_profile.password = make_password(pass_word)
            user_profile.save()

            send_register_email(user_name, "register")
            return render(request, "login.html")
        else:
            return render(request, "register.html", {"register_form": register_form})


class ActiveUserView(View):
    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()
        return render(request, "login.html")


class ForgetPwdView(View):
    def get(self, request):
        forget_from = ForgetForm()
        return render(request, "forgetpwd.html", {"forget_from": forget_from})

    def post(self, request):
        forget_from = ForgetForm(request.POST)
        if forget_from.is_valid():
            email = request.POST.get("email")
            send_register_email(email, "forget")
            return render(request, "send_success.html")
        else:
            return render(request, "forgetpwd.html", {"forget_form": forget_from})


class ResetPasswordView(View):
    def get(self, request, reset_code):
        all_records = EmailVerifyRecord.objects.filter(code=reset_code)
        if all_records:
            for record in all_records:
                email = record.email
                return render(request, "password_reset.html", {"email": email})
        else:
            return render(request, "reset_password_fail.html")


class ModifyPasswordView(View):
    def post(self, request):
        modify_form = ModifyPasswordForm(request.POST)
        if modify_form.is_valid():
            email = request.POST.get("email", "")
            password1 = request.POST.get("password1", "")
            password2 = request.POST.get("password2", "")
            if password1 != password2:
                return render(request, "password_reset.html", {"email": email, "reg": "两次输入的密码不一致"})
            user = UserProfile.objects.get(email=email)
            user.password = make_password(password2)
            user.save()
            return render(request, "login.html")

class  UserInfoView(LoginRequiredMixin, View):
    """
    用户个人信息
    """
    def get(self, request):
        user = request.user
        return render(request, "usercenter-info.html", {
            "user": user,
        })

    def post(self, request):
        user_info_form = UserInfoForm(request.POST, instance=request.user)
        if user_info_form.is_valid():
            user_info_form.save()
            return HttpResponse(json.dumps({"status":"success"}), content_type="application/json")
        return HttpResponse(json.dumps(user_info_form.errors), content_type="application/json")


class UploadImageView(LoginRequiredMixin, View):
    """
    用户修改头像
    """
    def post(self, request):
        image_form = UploadImageForm(request.POST, request.FILES, instance=request.user)
        if image_form.is_valid():
            image_form.save()
            return HttpResponse(json.dumps({"status":"success"}), content_type='application/json')
        return HttpResponse(json.dumps({"status":"fail"}), content_type='application/json')

class UpdatePwdView(View):
    """
    个人中心修改用户密码
    """
    def post(self, request):
        modify_form = ModifyPasswordForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get("password1", "")
            pwd2 = request.POST.get("password2", "")
            if pwd1 != pwd2:
                return HttpResponse(json.dumps({"status":"fail", "msg": "密码不一致"}), content_type='application/json')
            user = request.user
            user.password = make_password(password=pwd1)
            user.save()
            return HttpResponse(json.dumps({"status":"success"}), content_type='application/json')
        else:
            return HttpResponse(json.dumps({"status":"fail", "msg":"填写错误"}), content_type='application/json')

class SendEmailCodeView(LoginRequiredMixin, View):
    """
    发送邮箱验证码
    """
    def get(self, request):
        email = request.GET.get('email', '')
        if UserProfile.objects.filter(email=email):
            return HttpResponse(json.dumps({"status":"fail","email":"邮箱已经存在"}), content_type="application/json")
        send_register_email(email, send_type="update_email")
        return HttpResponse(json.dumps({"status":"success", "email":"邮件发送成功"}), content_type="application/json")

class UpdateEmailView(LoginRequiredMixin, View):
    """
    修改用户邮箱
    """
    def post(self, request):
        email = request.POST.get("email", "")
        code = request.POST.get("code", "")

        existed_records = EmailVerifyRecord.objects.filter(email=email, code=code , send_type="update_email")
        if existed_records:
            user = request.user
            user.email = email
            user.save()
            return HttpResponse(json.dumps({"status":"success", "email":"邮箱修改成功"}), content_type="application/json")
        else:
            return HttpResponse(json.dumps({"status":"fail","email":"验证码出错"}), content_type="application/json")

class UserCourseView(LoginRequiredMixin, View):
    """
    用户课程
    """
    def get(self, request):
        user_courses = UserCourse.objects.filter(user_id=request.user.id)
        courses_id = [ course.id for course in user_courses]
        courses = Course.objects.filter(id__in=courses_id)
        return render(request, "usercenter-mycourse.html", {
            "courses": courses,
        })

class UserFavCourseView(LoginRequiredMixin, View):
    """
    用户收藏
    """
    def get(self, request):
        fav_courses = UserFavorite.objects.filter(user_id=request.user.id, fav_type=1)
        courses_id = [ fav.fav_id for fav in fav_courses]
        fav_courses = Course.objects.filter(id__in=courses_id)
        return render(request, "usercenter-fav-course.html", {
            "fav_courses": fav_courses,
        })

class UserFavTeacherView(LoginRequiredMixin, View):
    """
    用户收藏教师
    """
    def get(self, request):
        fav_teachers = UserFavorite.objects.filter(user_id=request.user.id, fav_type=3)
        teachers_id = [fav.fav_id for fav in fav_teachers]
        fav_teachers = Teacher.objects.filter(id__in=teachers_id)
        return render(request, "usercenter-fav-teacher.html", {
            "fav_teachers": fav_teachers,
        })

class UserFavOrgView(LoginRequiredMixin, View):
    """
    用户收藏机构
    """
    def get(self, request):
        fav_orgs = UserFavorite.objects.filter(user_id=request.user.id, fav_type=2)
        orgs_id = [fav.fav_id for fav in fav_orgs]
        fav_orgs = CourseOrg.objects.filter(id__in=orgs_id)
        return render(request, "usercenter-fav-org.html", {
            "fav_orgs": fav_orgs,
        })

class UserMessageView(LoginRequiredMixin, View):
    """
    用户消息
    """
    def get(self, request):
        all_messages =  UserMessage.objects.filter(user=request.user.id)
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_messages, 1, request=request)
        messages = p.page(page)
        return render(request, "usercenter-message.html", {
           "messages": messages,
        })

