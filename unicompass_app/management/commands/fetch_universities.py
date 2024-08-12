import requests
from django.core.management.base import BaseCommand
from unicompass_app.models import THE_University, QS_University

class Command(BaseCommand):
    help = 'Fetch, update, and save universities from THE and TopUniversities'

    def handle(self, *args, **kwargs):
        self.fetch_and_update_the_universities()
        self.fetch_and_update_qs_universities()

    def fetch_and_update_the_universities(self):
        url = 'https://www.timeshighereducation.com/sites/default/files/the_data_rankings/world_university_rankings_2024_0__91239a4509dc50911f1949984e3fb8c5.json'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers)

        print('Status Code:', response.status_code)

        if response.status_code == 200:
            try:
                data = response.json()
            except ValueError:
                self.stdout.write(self.style.ERROR('Response is not valid JSON.'))
                return

            universities = data.get('data', [])

            # Filter out entries with invalid rank values
            def safe_rank(entry):
                try:
                    return int(entry.get('rank', 0).strip())
                except ValueError:
                    return float('inf')  # Use a high value for sorting invalid ranks

            # Sort by rank while handling invalid rank values
            universities_sorted = sorted(universities, key=lambda x: safe_rank(x))

            # Filter universities by location: Kazakhstan
            universities_kazakhstan = [uni for uni in universities_sorted if uni.get('location') == 'Kazakhstan']

            for entry in universities_kazakhstan:
                rank = entry.get('rank')
                name = entry.get('name')
                scores_overall = entry.get('scores_overall')
                nid = entry.get('nid')
                location = entry.get('location')
                subjects_offered = entry.get('subjects_offered')

                # Update existing entry or create a new one
                THE_University.objects.update_or_create(
                    nid=nid,
                    defaults={
                        'rank': rank,
                        'name': name,
                        'scores_overall': scores_overall,
                        'location': location,
                        'subjects_offered': subjects_offered
                    }
                )

            self.stdout.write(self.style.SUCCESS(f'{len(universities_kazakhstan)} universities in Kazakhstan successfully fetched, updated, and saved from THE.'))
        else:
            self.stdout.write(self.style.ERROR(f'Failed to fetch data from THE. Status code: {response.status_code}'))
            self.stdout.write(self.style.ERROR(f'Response Content: {response.text}'))

    def fetch_and_update_qs_universities(self):
        url = 'https://www.topuniversities.com/rankings/endpoint?nid=3990755&page=&items_per_page=15&tab=indicators&region=&countries=kz&cities=&search=&star=&sort_by=rank&order_by=asc&program_type=&scholarship=&fee=&english_score=&academic_score=&mix_student=&loggedincache='
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers)

        print('Status Code:', response.status_code)

        if response.status_code == 200:
            try:
                data = response.json()
            except ValueError:
                self.stdout.write(self.style.ERROR('Response is not valid JSON.'))
                return

            universities = data.get('score_nodes', [])

            for entry in universities:
                rank = entry.get('rank')
                title = entry.get('title')
                overall_score = entry.get('overall_score')
                score_nid = entry.get('score_nid')
                city = entry.get('city')
                country = entry.get('country')

                # Convert overall_score to float if possible, otherwise set to None
                try:
                    overall_score = float(overall_score)
                except ValueError:
                    overall_score = None

                # Update existing entry or create a new one
                QS_University.objects.update_or_create(
                    score_nid=score_nid,
                    defaults={
                        'rank': rank,
                        'title': title,
                        'overall_score': overall_score,
                        'city': city,
                        'country': country
                    }
                )

            self.stdout.write(self.style.SUCCESS(f'{len(universities)} universities successfully fetched, updated, and saved from QS.'))
        else:
            self.stdout.write(self.style.ERROR(f'Failed to fetch data from QS. Status code: {response.status_code}'))
            self.stdout.write(self.style.ERROR(f'Response Content: {response.text}'))
