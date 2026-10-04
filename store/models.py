from django.db import models

# Create your models here.
class Mudhakkira(models.Model):
    # Matches the real class structure: Raudha, Primary 1-6, Secondary 1-6
    LEVEL_CHOICES = [
    ('raudha', 'Raudha'),
    ('primary_1', 'Primary 1'),
    ('primary_2', 'Primary 2'),
    ('primary_3', 'Primary 3'),
    ('primary_4', 'Primary 4'),
    ('primary_5', 'Primary 5'),
    ('primary_6', 'Primary 6'),
    ('secondary_1', "Secondary 1 (Awwal I'daad)"),
    ('secondary_2', "Secondary 2 (Thaani I'daad)"),
    ('secondary_3', "Secondary 3 (Thaalitha I'daad)"),
    ('secondary_4', "Secondary 4 (Awwal Thanawi)"),
    ('secondary_5', "Secondary 5 (Thaani Thanawi)"),
    ('secondary_6', "Secondary 6 (Thaalitha Thanawi)"),
]
    title = models.CharField(max_length=200)
    subject = models.CharField(max_length=100)
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    file = models.FileField(upload_to='mudhakkirat/')
    created_at=models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return f"{self.title} ({self.subject} - {self.level})"

  # This represents a single purchase request from a student.
# It starts as "pending" until you manually verify the mobile
# money payment, then you mark it "paid".
class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
    ]

    # Which mudhakkira they want to buy
    mudhakkira = models.ForeignKey(Mudhakkira, on_delete=models.CASCADE)

    # Buyer's details, typed in by them on the order form
    buyer_name = models.CharField(max_length=100)
    buyer_phone = models.CharField(max_length=20)
    payment_reference = models.CharField(max_length=100)

    # Starts as "pending" automatically until you approve it
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    # This will hold the auto-generated watermarked PDF once approved
    watermarked_file = models.FileField(upload_to='watermarked/', blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.buyer_name} - {self.mudhakkira.title} ({self.status})"      