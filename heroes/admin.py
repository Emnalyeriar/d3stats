from django.contrib import admin

from .models import Hero, HeroHistory, Skill, Rune, Passive, LegendaryPower

admin.site.register(Hero)
admin.site.register(HeroHistory)
admin.site.register(Skill)
admin.site.register(Rune)
admin.site.register(Passive)
admin.site.register(LegendaryPower)
