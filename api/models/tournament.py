from django.db import models

class Tournament(models.Model):
    name = models.CharField(max_length=100, primary_key=True)
    num_brackets = models.SmallIntegerField()
    num_bracket_seeds = models.SmallIntegerField()


class Bracket(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    class Meta:
        unique_together = ('tournament', 'name')

    def display_name(self):
        return '{0} : {1}'.format(self.tournament.name, self.name)


class Seed(models.Model):
    bracket = models.ForeignKey(Bracket, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    value = models.SmallIntegerField()

    class Meta:
        unique_together = ('bracket', 'name', 'value')

    def display_name(self):
        return '{0} : {1} : {2} ({3})'.format(self.bracket.tournament.name, self.bracket.name, self.name, self.value)

