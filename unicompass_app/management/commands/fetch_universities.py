import requests
from django.core.management.base import BaseCommand
from unicompass_app.models import THE_University, QS_University

class Command(BaseCommand):
    help = 'Fetch, update, and save subject-specific university rankings from THE'

    # URLs for subject-specific rankings
    THE_RANKING_URLS = {
        'the_rank': 'https://www.timeshighereducation.com/sites/default/files/the_data_rankings/world_university_rankings_2024_0__91239a4509dc50911f1949984e3fb8c5.json',
        'rank_arts': 'https://www.timeshighereducation.com/sites/default/files/the_data_rankings/arts_humanities_rankings_2024_0__ccb001eff81d1137b1111a3a20ef5f32.json',
        'rank_bus': 'https://www.timeshighereducation.com/sites/default/files/the_data_rankings/business_economics_rankings_2024_0__b3c196ad15cc3a840eea0e69a6b22323.json',
        'rank_psych': 'https://www.timeshighereducation.com/sites/default/files/the_data_rankings/psychology_rankings_2024_0__a17810e20dbbfc018c4436a051eca33d.json',
        'rank_life': 'https://www.timeshighereducation.com/sites/default/files/the_data_rankings/life_sciences_rankings_2024_0__891eecb7ad740bbf1497885899ac2eef.json',
        'rank_law': 'https://www.timeshighereducation.com/sites/default/files/the_data_rankings/law_rankings_2024_0__52d627e653b5e2db67688d415fb54533.json',
        'rank_edu': 'https://www.timeshighereducation.com/sites/default/files/the_data_rankings/education_rankings_2024_0__5f2a8c685e8d7ac407b330777634adde.json',
        'rank_comp': 'https://www.timeshighereducation.com/sites/default/files/the_data_rankings/computer_science_rankings_2024_0__fe5e1ecb8de7d97cac3213b7d3f5b05f.json',
        'rank_clin': 'https://www.timeshighereducation.com/sites/default/files/the_data_rankings/clinical_pre_clinical_health_ran_2024_0__b8881c632a7135c802c13201dc21d78b.json',
        'rank_phys': 'https://www.timeshighereducation.com/sites/default/files/the_data_rankings/physical_sciences_rankings_2024_0__10810ad22bbdaa7c2f980efc335f94f2.json',
    }

    QS_RANKING_URL_KEYS = {
        "qs_rank": '3897789',
        "rank_eng_tech": '3948167',
        "rank_chem_eng" : '3948189',
        "rank_civil_eng": '3948190',
        "rank_comp_sci" : '3948183',
        "rank_data_sci" : '3948222',
        "rank_elec_eng" : '3948191',
        "rank_pet_eng": '3948198',
        "rank_mech_eng": '3948192',
        "rank_mining_eng": '3948193',
        "rank_nat_sci": '3948169',
        "rank_chemistry": '3948180',
        "rank_earth_marine_sci": '3948186',
        "rank_env_sci": '3948196',
        "rank_geography": '3948199',
        "rank_geology": '3948197',
        "rank_geophysics": '3948195',
        "rank_materials_sci": '3948218',
        "rank_math": '3948216',
        "rank_physics_astronomy": '3948210',
        "rank_life_sci": '3948168',
        "rank_agriculture": '3948172',
        "rank_anatomy": '3948173',
        "rank_bio_sci": '3948178',
        "rank_dentistry": '3948184',
        "rank_medicine": '3948217',
        "rank_pharmacy": '3948213',
        "rank_nursing": '3948223',
        "rank_psychology": '3948207',
        "rank_vet_sci": '3948200',
        "rank_arts_humanities": '3948166',
        "rank_linguistics": '3948214',
        "rank_music": '3948226',
        "rank_theology": '3948201',
        "rank_archaeology": '3948175',
        "rank_architecture": '3948176',
        "rank_art_design": '3948177',
        "rank_classics": '3948181',
        "rank_english": '3948194',
        "rank_history": '3948202',
        "rank_art_history": '3948220',
        "rank_modern_languages": '3948219',
        "rank_performing_arts": '3948215',
        "rank_philosophy": '3948211',
    }

    def handle(self, *args, **kwargs):
        for subject_field, url in self.THE_RANKING_URLS.items():
            self.fetch_and_update_the_subject_rankings(subject_field, url)
        for subject_field, qs_key in self.QS_RANKING_URL_KEYS.items():
            self.fetch_and_update_qs_subject_rankings(subject_field, qs_key)

    def fetch_and_update_the_subject_rankings(self, subject_field, url):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            try:
                data = response.json()
            except ValueError:
                self.stdout.write(self.style.ERROR(f'Invalid JSON response for {subject_field}.'))
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
                nid = entry.get('nid')

                if rank and nid:
                    THE_University.objects.update_or_create(
                        nid=nid,
                        defaults={
                            'name': name,
                            subject_field: rank
                        }
                    )

            self.stdout.write(self.style.SUCCESS(f'Successfully fetched, updated, and saved from THE rankings for {subject_field}.'))
        else:
            self.stdout.write(self.style.ERROR(f'Failed to fetch data from {url}. Status code: {response.status_code}'))

    def fetch_and_update_qs_subject_rankings(self, subject_field, qs_key):
        # Construct the QS URL with the key
        url = f'https://www.topuniversities.com/rankings/endpoint?nid={qs_key}&page=&items_per_page=15&tab=indicators&region=&countries=kz&cities=&search=&star=&sort_by=rank&order_by=asc&program_type=&scholarship=&fee=&english_score=&academic_score=&mix_student=&loggedincache='
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            try:
                data = response.json()
            except ValueError:
                self.stdout.write(self.style.ERROR(f'Invalid JSON response for {subject_field}.'))
                return

            universities = data.get('score_nodes', [])

            # Sort by rank key (ensure rank is present and valid)
            universities_sorted = sorted(universities, key=lambda x: int(x.get('rank', 0)) if x.get('rank') else float('inf'))
            
            universities_kazakhstan = [uni for uni in universities_sorted if uni.get('country') == 'Kazakhstan']

            for entry in universities_kazakhstan:
                rank = entry.get('rank')
                title = entry.get('title')
                overall_score = entry.get('overall_score')
                nid = entry.get('nid')
                score_nid = entry.get('score_nid')
                city = entry.get('city')
                country = entry.get('country')

                # Convert overall_score to float if possible
                try:
                    overall_score = float(overall_score)
                except ValueError:
                    overall_score = None

                # Update or create a QS_University entry
                if rank and score_nid:
                    QS_University.objects.update_or_create(
                        nid=nid,
                        defaults={
                            'title': title,
                            str(subject_field): rank,
                            'overall_score': overall_score,
                            'city': city,
                            'country': country
                        }
                    )

            self.stdout.write(self.style.SUCCESS(f'Successfully fetched, updated, and saved from QS rankings for {subject_field}.'))
        else:
            self.stdout.write(self.style.ERROR(f'Failed to fetch data from QS. Status code: {response.status_code}'))
            self.stdout.write(self.style.ERROR(f'Response Content: {response.text}'))
