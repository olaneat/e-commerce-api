from rest_framework.permissions import BasePermission

class IsloggedInOrAdmin(BasePermission):
	def has_object_permission(self, request, obj, view):
		return obj == request.user or request.user.is_staff

class AdminUser(BasePermission):
	def has_permission(self, view, request):
		return request.user or request.user.is_staff


	def has_object_permission(self, request, view, obj):
		return request.user or request.user.is_staff

		