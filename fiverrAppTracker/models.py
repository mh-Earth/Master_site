from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Orders(models.Model):
    """
    A Django model to represent a client with various attributes.
    """
    isPaid = models.BooleanField(
        default=False,
        help_text="Indicates whether the order has paid."
    )
    isBlocked = models.BooleanField(
        default=False,
        help_text="Indicates whether the client app is blocked"
    )
    disconnect_connection = models.BooleanField(
        default=False,
        help_text="Indicates whether the client's connection has been disconnected."
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="The price or fee associated with the client."
    )
    client_name = models.CharField(
        max_length=255,
        help_text="The name of the client."
    )
    client_url = models.URLField(
        max_length=200,
        help_text="A URL related to the client."
    )
    slug = models.SlugField(
        unique=True,
        help_text="A URL-friendly slug for the client."
    )
    client_review = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(10)],
        help_text="A review score from 0 to 10."
    )
    order_date = models.DateTimeField(
        auto_now_add=True,
        help_text="The date and time the order was placed."
    )
    delivery_date = models.DateTimeField(
        null=True,
        blank=True,
        help_text="The date and time of the order delivery."
    )
    project_description = models.TextField(
        null=True,
        blank=True,
        help_text="A detailed description of the project."
    )

    def __str__(self):
        """String for representing the Model object."""
        return self.client_name

    class Meta:
        verbose_name = "Client"
        verbose_name_plural = "Clients"
        ordering = ["client_name"]
