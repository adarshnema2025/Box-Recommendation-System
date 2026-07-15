from django.db import models


class Box(models.Model):
    """
    Maps to the existing `box` table:

    CREATE TABLE box (
        id SERIAL PRIMARY KEY,
        serial_no VARCHAR(20) UNIQUE NOT NULL,
        name VARCHAR(100) NOT NULL,
        internal_length NUMERIC(10,2) NOT NULL,
        internal_width NUMERIC(10,2) NOT NULL,
        internal_height NUMERIC(10,2) NOT NULL,
        max_weight_capacity NUMERIC(10,2) NOT NULL,
        cost NUMERIC(10,2) NOT NULL
    );
    """
    serial_no = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    internal_length = models.DecimalField(max_digits=10, decimal_places=2)
    internal_width = models.DecimalField(max_digits=10, decimal_places=2)
    internal_height = models.DecimalField(max_digits=10, decimal_places=2)
    max_weight_capacity = models.DecimalField(max_digits=10, decimal_places=2)
    cost = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'box'
        ordering = ['cost']

    def __str__(self):
        return f'{self.serial_no} - {self.name}'

    @property
    def volume(self):
        """Internal volume of the box (length * width * height)."""
        return self.internal_length * self.internal_width * self.internal_height