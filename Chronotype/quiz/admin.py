from django.contrib import admin
from quiz.models import Delegate, Printer
from quiz import controller

chronotype = {1: 'Extreme lark',
              2: 'Lark',
              3: 'Owl',
              4: 'Extreme owl'}

def admin_print_badges(modeladmin, request, queryset):
    """Processes the admin option to print selected badges"""
    for delegate in queryset.all():
        controller.print_badge(delegate)
admin_print_badges.short_description = 'Print delegate badge'

class DelegateAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Delegate',                      {'fields': ['first_name',
                                                      'last_name',
                                                      'organisation',
                                                      'sector',]}),
        ('Quiz',                          {'fields': ['quiz_answers',
                                                      'quiz_result',]}),
        ('Details',                       {'fields': ['created','printed',]}),
        ]
    actions = [admin_print_badges]

admin.site.register(Delegate, DelegateAdmin)
admin.site.register(Printer)

