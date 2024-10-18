from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    pass

class UniUni(models.Model):

    # Attributes for Page
    description = models.CharField(max_length=1000, blank=True, null=True)
    link = models.CharField(max_length=256, blank=True, null=True)
    img = models.CharField(max_length=256, blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)

    kz_title = models.CharField(max_length=20, blank=True, null=True)

    the_rank = models.CharField(max_length=10)

    # Subject-Specific Rankings
    the_rank_arts = models.CharField(max_length=10, blank=True, null=True)  # Arts & Humanities
    the_rank_eng = models.CharField(max_length=10, blank=True, null=True)   # Engineering
    the_rank_bus = models.CharField(max_length=10, blank=True, null=True)   # Business & Economics
    the_rank_law = models.CharField(max_length=10, blank=True, null=True)   # Law
    the_rank_clin = models.CharField(max_length=10, blank=True, null=True)  # Clinical & Health
    the_rank_life = models.CharField(max_length=10, blank=True, null=True)  # Life Sciences
    the_rank_comp = models.CharField(max_length=10, blank=True, null=True)  # Computer Science
    the_rank_phys = models.CharField(max_length=10, blank=True, null=True)  # Physical Sciences
    the_rank_edu = models.CharField(max_length=10, blank=True, null=True)   # Education
    the_rank_psych = models.CharField(max_length=10, blank=True, null=True) # Psychology

    # Other Fields
    the_title = models.CharField(max_length=255)
    the_overall_score = models.CharField(max_length=10, blank=True, null=True)
    the_nid = models.IntegerField(null=True, blank=True)
    the_location = models.CharField(max_length=255, blank=True, null=True)
    the_subjects_offered = models.TextField(blank=True, null=True)

    qs_title = models.CharField(max_length=256)
    qs_overall_score = models.FloatField(blank=True, null=True)
    qs_rank = models.PositiveIntegerField(blank=True, null=True)
    qs_nid = models.IntegerField(blank=True, null=True)

    # Arts & Humanities Rankings
    qs_rank_arts_humanities = models.CharField(max_length=10, blank=True, null=True)
    qs_rank_arts = models.CharField(max_length=10, blank=True, null=True)
    qs_rank_linguistics = models.CharField(max_length=10, blank=True, null=True)
    qs_rank_music = models.CharField(max_length=10, blank=True, null=True)
    qs_rank_theology = models.CharField(max_length=10, blank=True, null=True)
    qs_rank_archaeology = models.CharField(max_length=10, blank=True, null=True)
    qs_rank_architecture = models.CharField(max_length=10, blank=True, null=True)
    qs_rank_art_design = models.CharField(max_length=10, blank=True, null=True)
    qs_rank_classics = models.CharField(max_length=10, blank=True, null=True)
    qs_rank_english = models.CharField(max_length=10, blank=True, null=True)
    qs_rank_history = models.CharField(max_length=10, blank=True, null=True)
    qs_rank_art_history = models.CharField(max_length=10, blank=True, null=True)
    qs_rank_modern_languages = models.CharField(max_length=10, blank=True, null=True)
    qs_rank_performing_arts = models.CharField(max_length=10, blank=True, null=True)
    qs_rank_philosophy = models.CharField(max_length=10, blank=True, null=True)

    # Engineering & Technology Rankings
    qs_rank_eng_tech = models.CharField(max_length=10, blank=True, null=True)
    qs_rank_chem_eng = models.CharField(max_length=10, blank=True, null=True)
    qs_rank_civil_eng = models.CharField(max_length=10, blank=True, null=True)
    qs_rank_comp_sci = models.CharField(max_length=10, blank=True, null=True)
    qs_rank_data_sci = models.CharField(max_length=10, blank=True, null=True)
    qs_rank_elec_eng = models.CharField(max_length=10, blank=True, null=True)
    qs_rank_pet_eng = models.CharField(max_length=10, blank=True, null=True)
    qs_rank_mech_eng = models.CharField(max_length=10, blank=True, null=True)
    qs_rank_mining_eng = models.CharField(max_length=10, blank=True, null=True)

    # Natural Sciences Rankings
    qs_rank_nat_sci = models.CharField(max_length=10, blank=True, null=True)
    qs_rank_chemistry = models.CharField(max_length=10, blank=True, null=True)
    qs_rank_earth_marine_sci = models.CharField(max_length=10, blank=True, null=True)
    qs_rank_env_sci = models.CharField(max_length=10, blank=True, null=True)
    qs_rank_geography = models.CharField(max_length=10, blank=True, null=True)
    qs_rank_geology = models.CharField(max_length=10, blank=True, null=True)
    qs_rank_geophysics = models.CharField(max_length=10, blank=True, null=True)
    qs_rank_materials_sci = models.CharField(max_length=10, blank=True, null=True)
    qs_rank_math = models.CharField(max_length=10, blank=True, null=True)
    qs_rank_physics_astronomy = models.CharField(max_length=10, blank=True, null=True)

    # Life Sciences & Medicine Rankings
    qs_rank_life_sci = models.CharField(max_length=10, blank=True, null=True)
    qs_rank_agriculture = models.CharField(max_length=10, blank=True, null=True)
    qs_rank_anatomy = models.CharField(max_length=10, blank=True, null=True)
    qs_rank_bio_sci = models.CharField(max_length=10, blank=True, null=True)
    qs_rank_dentistry = models.CharField(max_length=10, blank=True, null=True)
    qs_rank_medicine = models.CharField(max_length=10, blank=True, null=True)
    qs_rank_pharmacy = models.CharField(max_length=10, blank=True, null=True)
    qs_rank_nursing = models.CharField(max_length=10, blank=True, null=True)
    qs_rank_psychology = models.CharField(max_length=10, blank=True, null=True)
    qs_rank_vet_sci = models.CharField(max_length=10, blank=True, null=True)

    # Location and Unique Fields
    qs_city = models.CharField(max_length=255, blank=True, null=True)
    qs_country = models.CharField(max_length=255, blank=True, null=True)
    # ID for scores
    qs_score_nid = models.CharField(max_length=255, unique=True, blank=True, null=True)

    def get_scholarships(self, year=None):
        scholarships = self.scholarships.all()
        if year:
            scholarships = scholarships.filter(year=year)
        return scholarships.select_related('academic_program').order_by('academic_program__code')
    
    def __str__(self):
        return self.qs_title or self.the_title or self.kz_title

class AcademicProgram(models.Model):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.code} - {self.name}"

class Scholarship(models.Model):
    university = models.ForeignKey('UniUni', on_delete=models.CASCADE, related_name='scholarships')
    academic_program = models.ForeignKey(AcademicProgram, on_delete=models.CASCADE)
    year = models.IntegerField()
    minimum_score = models.IntegerField()
    available_grants = models.IntegerField()

    class Meta:
        unique_together = ('university', 'academic_program', 'year')

    def __str__(self):
        return f"{self.university} - {self.academic_program} ({self.year})"