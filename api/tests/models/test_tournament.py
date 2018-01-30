from django.test import TestCase
from api.models import Tournament, Bracket, Seed

class TournamentTest(TestCase):

    tourney_name = 'Test Tournament'
    brackets = ['Bracket A']
    seeds = {'A': 1, 'B': 2}

    tourney_record = None
    bracket_records = None
    seed_records = None

    def setUp(self):
        # Insert a test Tournament
        t_name = self.tourney_name
        num_brackets = len(self.brackets)
        num_bracket_seeds = len(self.seeds)
        Tournament.objects.create(name=t_name, num_brackets=num_brackets, num_bracket_seeds=num_bracket_seeds)
        tourney_record = Tournament.objects.get(name=t_name)

        # Insert bracket records
        for b in self.brackets:
            Bracket.objects.create(tournament=tourney_record, name=b)
        bracket_records = Bracket.objects.filter(tournament=tourney_record)

        # Insert seed recrods
        for b in bracket_records:
            for s, v in self.seeds.items():
                Seed.objects.create(bracket=b, name=s, value=v)

    def test_tournament_values(self):
        t = Tournament.objects.get(name=self.tourney_name)
        self.assertEqual(self.tourney_name, t.name, 'Tournament name does not match inserted')
        self.assertEqual(len(self.brackets), t.num_brackets, 'Bracket count does not match num inserted')
        self.assertEqual(len(self.seeds), t.num_bracket_seeds, 'Seed count does not match num inserted')

    def test_bracket_values(self):
        t = Tournament.objects.get(name=self.tourney_name)
        bracket_records = Bracket.objects.filter(tournament=t)
        self.assertEqual(len(self.brackets), len(bracket_records), 'Bracket count does not match count inserted')

        for r in bracket_records:
            self.assertEqual('{} : {}'.format(self.tourney_name, r.name), r.display_name(), 'Bracket display_name does not match')

    def test_seed_values(self):
        t = Tournament.objects.get(name=self.tourney_name)
        bracket_records = Bracket.objects.filter(tournament=t)
        for b in bracket_records:
            seed_records = Seed.objects.filter(bracket=b)
            self.assertEqual(len(self.seeds), len(seed_records), 'Seed count does not match count inserted')

            for s in seed_records:
                self.assertEqual('{} : {} : {} ({})'.format(self.tourney_name, b.name, s.name, s.value), s.display_name(), 'Seed display_name does not match')
