from django.contrib import admin

from ch_app import models


admin.site.register(models.R_wifi)
admin.site.register(models.Sensor_wifi)
admin.site.register(models.Timer)

