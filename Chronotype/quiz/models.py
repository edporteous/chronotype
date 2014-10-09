import datetime
from django.db import models
from django.utils import timezone

class Delegate(models.Model):
    NOT_SPECIFIED = 'NS'
    THEATRE = 'TH'
    DANCE = 'DA'
    MUSIC = 'MU'
    COMBINED_ARTS = 'CA'
    VISUAL_ARTS = 'VA'
    LITERATURE = 'LI'
    FILM = 'FI'
    CRAFTS = 'CR'
    ARCHITECTURE = 'AR'
    DESIGN = 'DN'
    FASHION = 'FN'
    GAMES = 'GM'
    TV_RADIO = 'TV'
    SOFTWARE_WEB = 'SW'
    HERITAGE = 'HE'
    OTHER = 'OT'
    SECTOR_CHOICES = (
        (NOT_SPECIFIED, ''),
        (THEATRE, 'Theatre'),
        (DANCE, 'Dance'),
        (MUSIC, 'Music'),
        (COMBINED_ARTS, 'Combined arts'),
        (LITERATURE, 'Literature'),
        (FILM, 'Film'),
        (CRAFTS, 'Crafts'),
        (ARCHITECTURE, 'Architecture'),
        (DESIGN, 'Design'),
        (FASHION, 'Fashion'),
        (GAMES, 'Games'),
        (TV_RADIO, 'TV/Radio'),
        (SOFTWARE_WEB, 'Software/Web'),
        (HERITAGE, 'Heritage'),
        (OTHER, 'Other'))
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    organisation = models.CharField(max_length=200)
    sector = models.CharField(max_length=2,
                              choices=SECTOR_CHOICES,
                              default=NOT_SPECIFIED)
    quiz_answers = models.CommaSeparatedIntegerField(max_length=100)
    quiz_result = models.IntegerField(default=0)
    created = models.DateTimeField()
    
    def __unicode__(self):
        return self.first_name + ' ' + self.last_name
    
class Printer(models.Model):
    code = models.CharField(max_length=200)
    
    def __unicode__(self):
        return self.code
    
class Badge(models.Model):
    print_time = models.DateTimeField('date and time printed')
    message = models.CharField(max_length=2048)
    image = models.CharField(max_length=1024)
    delegate = models.ForeignKey(Delegate)
    printer = models.ForeignKey(Printer)
    printed = models.BooleanField(default=False)
    
    def __unicode__(self):
        if self.printed:
            return str(self.delegate) + ' (printed ' + self.print_time.strftime("%H:%M %d-%m-%y") + ')'
        else:
            return str(self.delegate) + ' (not printed)'
        