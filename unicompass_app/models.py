from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    pass

class University(models.Model):
    title = models.CharField(max_length=256)

    def __str__(self):
        return self.title

class THE_University(models.Model):
    rank = models.CharField(max_length=10)
    
    # Subject-Specific Rankings
    rank_arts = models.CharField(max_length=10, blank=True, null=True)  # Arts & Humanities
    rank_eng = models.CharField(max_length=10, blank=True, null=True)   # Engineering
    rank_bus = models.CharField(max_length=10, blank=True, null=True)   # Business & Economics
    rank_law = models.CharField(max_length=10, blank=True, null=True)   # Law
    rank_clin = models.CharField(max_length=10, blank=True, null=True)  # Clinical & Health
    rank_life = models.CharField(max_length=10, blank=True, null=True)  # Life Sciences
    rank_comp = models.CharField(max_length=10, blank=True, null=True)  # Computer Science
    rank_phys = models.CharField(max_length=10, blank=True, null=True)  # Physical Sciences
    rank_edu = models.CharField(max_length=10, blank=True, null=True)   # Education
    rank_psych = models.CharField(max_length=10, blank=True, null=True) # Psychology

    # Other Fields
    title = models.CharField(max_length=255)
    overall_score = models.CharField(max_length=10)
    nid = models.IntegerField()
    location = models.CharField(max_length=255)
    subjects_offered = models.TextField()

    def __str__(self):
        return f"THE ranking; {self.name}; rank: {self.rank}"

class QS_University(models.Model):
    title = models.CharField(max_length=256)
    overall_score = models.FloatField(blank=True, null=True)
    rank = models.PositiveIntegerField(blank=True, null=True)
    nid = models.IntegerField(blank=True, null=True)

    # Arts & Humanities Rankings
    rank_arts_humanities = models.CharField(max_length=10, blank=True, null=True)
    rank_arts = models.CharField(max_length=10, blank=True, null=True)
    rank_linguistics = models.CharField(max_length=10, blank=True, null=True)
    rank_music = models.CharField(max_length=10, blank=True, null=True)
    rank_theology = models.CharField(max_length=10, blank=True, null=True)
    rank_archaeology = models.CharField(max_length=10, blank=True, null=True)
    rank_architecture = models.CharField(max_length=10, blank=True, null=True)
    rank_art_design = models.CharField(max_length=10, blank=True, null=True)
    rank_classics = models.CharField(max_length=10, blank=True, null=True)
    rank_english = models.CharField(max_length=10, blank=True, null=True)
    rank_history = models.CharField(max_length=10, blank=True, null=True)
    rank_art_history = models.CharField(max_length=10, blank=True, null=True)
    rank_modern_languages = models.CharField(max_length=10, blank=True, null=True)
    rank_performing_arts = models.CharField(max_length=10, blank=True, null=True)
    rank_philosophy = models.CharField(max_length=10, blank=True, null=True)

    # Engineering & Technology Rankings
    rank_eng_tech = models.CharField(max_length=10, blank=True, null=True)
    rank_chem_eng = models.CharField(max_length=10, blank=True, null=True)
    rank_civil_eng = models.CharField(max_length=10, blank=True, null=True)
    rank_comp_sci = models.CharField(max_length=10, blank=True, null=True)
    rank_data_sci = models.CharField(max_length=10, blank=True, null=True)
    rank_elec_eng = models.CharField(max_length=10, blank=True, null=True)
    rank_pet_eng = models.CharField(max_length=10, blank=True, null=True)
    rank_mech_eng = models.CharField(max_length=10, blank=True, null=True)
    rank_mining_eng = models.CharField(max_length=10, blank=True, null=True)

    # Natural Sciences Rankings
    rank_nat_sci = models.CharField(max_length=10, blank=True, null=True)
    rank_chemistry = models.CharField(max_length=10, blank=True, null=True)
    rank_earth_marine_sci = models.CharField(max_length=10, blank=True, null=True)
    rank_env_sci = models.CharField(max_length=10, blank=True, null=True)
    rank_geography = models.CharField(max_length=10, blank=True, null=True)
    rank_geology = models.CharField(max_length=10, blank=True, null=True)
    rank_geophysics = models.CharField(max_length=10, blank=True, null=True)
    rank_materials_sci = models.CharField(max_length=10, blank=True, null=True)
    rank_math = models.CharField(max_length=10, blank=True, null=True)
    rank_physics_astronomy = models.CharField(max_length=10, blank=True, null=True)

    # Life Sciences & Medicine Rankings
    rank_life_sci = models.CharField(max_length=10, blank=True, null=True)
    rank_agriculture = models.CharField(max_length=10, blank=True, null=True)
    rank_anatomy = models.CharField(max_length=10, blank=True, null=True)
    rank_bio_sci = models.CharField(max_length=10, blank=True, null=True)
    rank_dentistry = models.CharField(max_length=10, blank=True, null=True)
    rank_medicine = models.CharField(max_length=10, blank=True, null=True)
    rank_pharmacy = models.CharField(max_length=10, blank=True, null=True)
    rank_nursing = models.CharField(max_length=10, blank=True, null=True)
    rank_psychology = models.CharField(max_length=10, blank=True, null=True)
    rank_vet_sci = models.CharField(max_length=10, blank=True, null=True)

    # Location and Unique Fields
    city = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    # ID for scores
    score_nid = models.CharField(max_length=255, unique=True, blank=True, null=True)

    def __str__(self):
        return self.title


    def __str__(self):
        return f"QS ranking; {self.title}; rank: {self.rank}"
