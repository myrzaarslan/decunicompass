import json
import requests
from django.core.management.base import BaseCommand
from django.db import transaction
from unicompass_app.models import UniUni  # Replace 'your_app' with your actual app name

class Command(BaseCommand):
    help = 'Update university scores from THE and QS rankings'

    def handle(self, *args, **options):
        self.stdout.write('Fetching THE rankings...')
        the_data = self.fetch_the_rankings()
        
        self.stdout.write('Fetching QS rankings...')
        qs_data = self.fetch_qs_rankings()
        
        self.stdout.write('Updating university scores...')
        self.update_university_scores(the_data, qs_data)
        
        self.stdout.write(self.style.SUCCESS('Successfully updated university scores'))

    def fetch_the_rankings(self):
        url = 'https://www.timeshighereducation.com/sites/default/files/the_data_rankings/world_university_rankings_2024_0__91239a4509dc50911f1949984e3fb8c5.json'
        response = requests.get(url)
        data = json.loads(response.text)
        return [uni for uni in data['data'] if uni['location'] == 'Kazakhstan']

    def fetch_qs_rankings(self):
        url = 'https://www.topuniversities.com/rankings/endpoint?nid=3990755&page=0&items_per_page=21&tab=indicators&region=&countries=&cities=&search=&star=&sort_by=&order_by=&program_type=&scholarship=&fee=&english_score=&academic_score=&mix_student=&loggedincache='
        response = requests.get(url)
        return json.loads(response.text)['result']

    @transaction.atomic
    def update_university_scores(self, the_data, qs_data):
        for uni in the_data:
            try:
                db_uni = UniUni.objects.get(the_title=uni['name'])
                db_uni.the_overall_score = uni['scores_overall']
                db_uni.save()
                self.stdout.write(f"Updated THE score for {uni['name']}")
            except UniUni.DoesNotExist:
                self.stdout.write(f"No matching university found for THE: {uni['name']}")

        for uni in qs_data:
            try:
                db_uni = UniUni.objects.get(qs_title=uni['title'])
                db_uni.qs_overall_score = uni['overall_score']
                db_uni.save()
                self.stdout.write(f"Updated QS score for {uni['title']}")
            except UniUni.DoesNotExist:
                self.stdout.write(f"No matching university found for QS: {uni['title']}")