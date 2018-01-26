from django.contrib import admin

from .models import Tournament, Bracket, Seed


class TournamentAdmin(admin.ModelAdmin):
    list_display = ('name', 'num_brackets', 'num_bracket_seeds')

admin.site.register(Tournament, TournamentAdmin)


class BracketAdmin(admin.ModelAdmin):
    list_display = ('display_name', 'name')

admin.site.register(Bracket, BracketAdmin)


class SeedAdmin(admin.ModelAdmin):
    list_display = ('display_name', 'name', 'value')

admin.site.register(Seed, SeedAdmin)

