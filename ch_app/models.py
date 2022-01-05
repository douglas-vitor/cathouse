from django.db import models
from django.core.validators import MinValueValidator
from django.core.validators import MaxValueValidator


class R_wifi(models.Model):
	rw = models.CharField(max_length=15)
	ip = models.CharField(max_length=15)
	type = models.CharField(max_length=10)
	type2 = models.CharField(max_length=10)
	name = models.CharField(max_length=20)

	def __str__(self):
		rwifi_name = self.rw + " - " + self.type + " - " + self.name
		return (rwifi_name)


class Sensor_wifi(models.Model):
	ip = models.CharField(max_length=15)
	name = models.CharField(max_length=40)

	def __str__(self):
                return (self.name)


class Timer(models.Model):
	arm = models.IntegerField()
	time = models.CharField(max_length=5)
	window = models.IntegerField()
	days = models.CharField(max_length=7)
	repeat_timer = models.IntegerField()
	output = models.IntegerField()
	action = models.IntegerField()
	ip = models.CharField(max_length=15)
	name = models.CharField(max_length=10)
	name_for_user = models.CharField(max_length=40)

	def __str__(self):
		timer_name = self.ip + " - " + self.time + " - " + self.name_for_user
		return (timer_name)

class Rgb_temp(models.Model):
	type = models.CharField(max_length=3, default="RGB")
	ip = models.CharField(max_length=15)
	color = models.CharField(max_length=20)
	effect = models.IntegerField(default=0)
	bri = models.IntegerField(default=100)

	def __str__(self):
                return (self.ip)