import csv
from django.core.management.base import BaseCommand
from django.db import transaction
from unicompass_app.models import AcademicProgram, Scholarship, UniUni

class Command(BaseCommand):
    help = 'Populate UniUni, AcademicProgram, and Scholarship models from CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to the CSV file')
        parser.add_argument('year', type=int, help='Year of the scholarships')

    @transaction.atomic
    def handle(self, *args, **options):
        csv_file = options['csv_file']
        year = options['year']

        with open(csv_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                try:
                    # Validate and convert fields to integers
                    min_score = int(row['min_score'])
                    available_grants = int(row['available_grants'])
                except ValueError as e:
                    self.stderr.write(
                        f"Skipping row due to invalid data: {row}. Error: {str(e)}"
                    )
                    continue  # Skip this row if there's invalid data

                # Get or create University
                university, _ = UniUni.objects.get_or_create(
                    the_title=row['university_name'],
                    defaults={'the_rank': '0'}
                )

                # Get or create AcademicProgram
                program, _ = AcademicProgram.objects.get_or_create(
                    code=row['code'],
                    defaults={'name': row['program']}
                )

                # Create or update Scholarship
                Scholarship.objects.update_or_create(
                    university=university,
                    academic_program=program,
                    year=year,
                    defaults={
                        'minimum_score': min_score,
                        'available_grants': available_grants,
                    }
                )

        self.stdout.write(self.style.SUCCESS('Successfully populated models from CSV'))
