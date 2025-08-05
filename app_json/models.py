from django.db import models

class JsonRecord(models.Model):
	name = models.CharField(max_length=50)
	date = models.DateTimeField()

	def __str__(self):
		return f"{self.name} - {self.date}"