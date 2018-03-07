#encoding=utf8

from django.conf.urls import url

from users.views import UserInfoView, UploadImageView, UpdatePwdView, SendEmailCodeView, UpdateEmailView, UserCourseView

urlpatterns = [
    #用户信息
    url(r'^info/', UserInfoView.as_view(), name="info"),
    url(r'^image/upload/$', UploadImageView.as_view(), name="image_upload"),
    url(r'^update/pwd/$', UpdatePwdView.as_view(), name="update_pwd"),
    # 发送邮箱验证码
    url(r'^sendemail_code/$', SendEmailCodeView.as_view(), name="send_email_code"),
    url(r'^update_email/$', UpdateEmailView.as_view(), name="update_email"),
    url(r'^courses/$', UserCourseView.as_view(), name="user_course"),
]
