import csv
from django.core.management.base import BaseCommand
from django.db import transaction
from unicompass_app.models import AcademicProgram, Scholarship, UniUni

class Command(BaseCommand):
    help = 'Populate AcademicProgram and Scholarship models from CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to the CSV file')
        parser.add_argument('university_id', type=int, help='ID of the University')
        parser.add_argument('year', type=int, help='Year of the scholarships')

    @transaction.atomic
    def handle(self, *args, **options):
        csv_file = options['csv_file']
        university_id = options['university_id']
        year = options['year']

        try:
            university = UniUni.objects.get(id=university_id)
        except UniUni.DoesNotExist:
            self.stderr.write(self.style.ERROR(f'University with id {university_id} does not exist'))
            return

        with open(csv_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Create or update AcademicProgram
                program, created = AcademicProgram.objects.update_or_create(
                    code=row['code'],
                    defaults={'name': row['program']}
                )
                
                # Create or update Scholarship
                Scholarship.objects.update_or_create(
                    university=university,
                    academic_program=program,
                    year=year,
                    defaults={
                        'minimum_score': int(row['min_score']),
                        'available_grants': int(row['available_grants'])
                    }
                )

        self.stdout.write(self.style.SUCCESS('Successfully populated models from CSV'))