# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse
from django.shortcuts import redirect


class const:
    redirect_403 = "/admin/"
    class ConstError(TypeError): pass
    def __setattr__(self, name, value):
        if self.__dict__.has_key(name):
            raise self.ConstError, "Can't rebind const(%s)" % name
        self.__dict__[name] = value

def method_not_allowed(request):
    response = HttpResponse("This method is not allowed.")
    response.status_code = 405
    return response


def admin_user_confirm(request):
    if 'user_id' not in request.session:
        return False
    else:
        return True
