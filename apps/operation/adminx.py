import xadmin

from .models import UserAsk, UserCourse, UserMessage, UserFavorite, CourseComments

class UserAskAdmin(object):
    list_display = ['name', 'mobile', 'course_name']
    search_fields = ['name', 'mobile', 'course_name']
    list_filter = ['name', 'mobile', 'course_name']

class UserCourseAdmin(object):
    list_display = ['user', 'course' ]
    search_fields = ['user', 'course']
    list_filter = ['user', 'course' ]

class UserMessageAdmin(object):
    list_display = ['user', 'message', 'has_read' ]
    search_fields = ['user', 'message']
    list_filter = ['user', 'message' ]

class UserFavoriteAdmin(object):
    list_display = ['user', 'fav_id', 'fav_type' ]
    search_fields = ['user', 'fav_id', 'fav_type']
    list_filter = ['user', 'fav_id', 'fav_type' ]

class CourseCommentsAdmin(object):
    list_display = ['user', 'course', 'comments' ]
    search_fields = ['user', 'course', 'comments']
    list_filter = ['user', 'course', 'comments' ]

xadmin.site.register(UserAsk, UserAskAdmin)
xadmin.site.register(UserCourse, UserCourseAdmin)
xadmin.site.register(UserMessage, UserMessageAdmin)
xadmin.site.register(UserFavorite, UserFavoriteAdmin)
xadmin.site.register(CourseComments, CourseCommentsAdmin)



