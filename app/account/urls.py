# coding: utf-8

from tornado.web import url

from .console import views as console_views


handlers = [

    # console
    url(r'/console/account/profile', console_views.MyProfile),
    url(r'/console/account/password', console_views.PasswordReset),
]
