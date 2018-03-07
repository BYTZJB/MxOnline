#encoding=utf8

from django.conf.urls import url

from users.views import UserInfoView, UploadImageView, UpdatePwdView, SendEmailCodeView, UpdateEmailView, \
    UserFavCourseView, UserFavTeacherView, UserFavOrgView, UserMessageView
from users.views import UserCourseView

urlpatterns = [
    #用户信息
    url(r'^info/', UserInfoView.as_view(), name="info"),
    url(r'^image/upload/$', UploadImageView.as_view(), name="image_upload"),
    url(r'^update/pwd/$', UpdatePwdView.as_view(), name="update_pwd"),
    # 发送邮箱验证码
    url(r'^sendemail_code/$', SendEmailCodeView.as_view(), name="send_email_code"),
    #更新用户邮箱
    url(r'^update_email/$', UpdateEmailView.as_view(), name="update_email"),
    #用户课程
    url(r'^courses/$', UserCourseView.as_view(), name="user_course"),
    #用户收藏课程
    url(r'^fav/courses/$', UserFavCourseView.as_view(), name="user_fav_course"),
    #用户收藏教师
    url(r'^fav/teachers/$', UserFavTeacherView.as_view(), name="user_fav_teacher"),
    #用户收藏机构
    url(r'^fav/org/$', UserFavOrgView.as_view(), name="user_fave_org"),
    #用户消息
    url(r'^message/$', UserMessageView.as_view(), name="user_message"),

]
