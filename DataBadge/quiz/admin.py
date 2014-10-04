import urllib2, urllib
from django.contrib import admin
from quiz.models import Delegate, Printer, Badge

chronotype = {1: 'Extreme lark',
              2: 'Lark',
              3: 'Owl',
              4: 'Extreme owl'}

image = {1: 'extremelarksmall.jpg',
         2: 'larksmall.jpg',
         3: 'owlsmall.jpg',
         4: 'extremeowlsmall.jpg'}

def print_badge(modeladmin, request, queryset):
    for delegate in queryset.all():
        name = delegate.first_name + ' ' + delegate.last_name
        organisation = delegate.organisation
        post_data = [('html', '<html><head><meta charset="utf-8">' +
                    '''<style type="text/css">
body {
background: #fff;
color: #000;
width: 384px;
margin: 0px;
padding: 20px 0px;
}
h1 {
word-wrap: break-word;
text-align: center;
font-family: 'Quicksand';
font-size: 325%;
font-weight: bold;
}
h2 {
word-wrap: break-word;
text-align: center;
font-family: 'Quicksand';
font-size: 250%;
font-weight: normal;
}
h3 {
word-wrap: break-word;
text-align: center;
font-family: 'Latin Modern Mono Prop;
font-size: 125%;
font-weight: normal;
}
</style>''' +
                    '</head><body>' +
                    '<h1>' + name.upper() + '</h1>' +
                    '<h2>' + organisation + '</h2>' +
                    '<img src="http://data-badge.appspot.com/static/quiz/images/{0}"></img>'.format(image[delegate.quiz_result]) +
                    '<h3>made by theotherwayworks.co.uk</h3>' +
                    '</body></html>')]
        print post_data
        result = urllib2.urlopen('http://remote.bergcloud.com/playground/direct_print/P3WPAOFL3FDN', urllib.urlencode(post_data))
        content = result.read()
        if content == 'OK':
            print('Successfully printed badge: ' + name)
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
