from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from django.core.exceptions import ValidationError

class Salon(models.Model):
    owner = models.ForeignKey(
        'authentication.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='owned_salons'
    )
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    phone = models.CharField(
        max_length=15, 
        validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")]
    )
    email = models.EmailField(null=True, blank=True)
    website = models.URLField(blank=True, null=True)
    country_code = models.CharField(max_length=5, blank=True)
    description = models.TextField(blank=True)
    user = models.OneToOneField(
        'authentication.User', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='profile'
    )
    rating = models.FloatField(
        null=True, 
        blank=True, 
        validators=[MinValueValidator(0), MaxValueValidator(5)]
    )

    class Meta:
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['city']),
            models.Index(fields=['rating']),
        ]

    def __str__(self):
        return self.name

class Service(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    duration = models.IntegerField(help_text="Duration in minutes")
    salon = models.ForeignKey(Salon, on_delete=models.CASCADE, related_name='services')
    
    def __str__(self):
        return self.name
    
class Stylist(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True, null=True, blank=True)
    phone = models.CharField(
        max_length=15, 
        validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")]
    )
    specialties = models.CharField(max_length=200)
    user = models.OneToOneField(
        'authentication.User', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='stylist_profile'
    )
    workplace = models.ForeignKey(Salon, on_delete=models.SET_NULL, null=True, related_name='workplace_stylists')
    years_of_experience = models.IntegerField(validators=[MinValueValidator(0)])
    salon = models.ForeignKey(Salon, on_delete=models.CASCADE, related_name='stylists')

    def clean(self):
        if self.years_of_experience < 0:
            raise ValidationError('Years of experience cannot be negative')

    def __str__(self):
        return self.name
    user = models.OneToOneField(
        'authentication.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='stylist_profile'
    )

    def clean(self):
        if self.user and Stylist.objects.exclude(pk=self.pk).filter(user=self.user).exists():
            raise ValidationError("This user is already associated with another stylist profile.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

class Promotion(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    discount_percentage = models.IntegerField()
    valid_until = models.DateTimeField()

    def __str__(self):
        return self.title