from rest_framework import permissions


class IsTeacher(permissions.BasePermission):
    message = 'Only teachers can do this.'

    def has_permission(self, request, view):
        return request.user.role == 'teacher'


class IsStudent(permissions.BasePermission):
    message = 'Only students can do this.'

    def has_permission(self, request, view):
        return request.user.role == 'student'


class IsStudentOrTeacher(permissions.BasePermission):
    message = 'Neither teacher nor student.. who are you?'

    def has_permission(self, request, view):
        return request.user.role == 'student' or 'teacher'


class IsCreatorOrReadOnly(permissions.BasePermission):
    message = "Forbidden. Only for course creator."

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user.id
