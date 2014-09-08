import urllib2, urllib
from django.contrib import admin
from quiz.models import Delegate, Printer, Badge

chronotype = {1: 'Extreme lark',
              2: 'Lark',
              3: 'Owl',
              4: 'Extreme owl'}

def print_badge(modeladmin, request, queryset):
    for delegate in queryset.all():
        message = delegate.first_name + ' ' + delegate.last_name + ': ' + chronotype[delegate.quiz_result]
        post_data = [('html', '<html><head><meta charset="utf-8"></head><body><h1>' + message + '</h1></body></html>')]
        result = urllib2.urlopen('http://remote.bergcloud.com/playground/direct_print/P3WPAOFL3FDN', urllib.urlencode(post_data))
        content = result.read()
        if content == 'OK':
            print('Successfully printed badge: ' + message)
        else:
            print('Unexpected response from remote.bergcloud.com:')
            print content
print_badge.short_description = 'Print delegate badge'

class DelegateAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Delegate',                      {'fields': ['first_name', 
                                                      'last_name',
                                                      'organisation',
                                                      'sector',]}),
        ('Quiz',                          {'fields': ['quiz_answers',
                                                      'quiz_result',]}),
        ('Details',                       {'fields': ['created',],
                                           'classes': ['collapse']}),
        ]
    actions = [print_badge]

admin.site.register(Delegate, DelegateAdmin)
admin.site.register(Printer)
admin.site.register(Badge)