from django.db import models

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
    printed = models.BooleanField()
        
    def __unicode__(self):
        return self.first_name + ' ' + self.last_name
    
class Printer(models.Model):
    url = models.CharField(max_length=200)
    
    def __unicode__(self):
        return self.code
    
        