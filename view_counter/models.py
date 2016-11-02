from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User


class Posted_Sale(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	Sale_title = models.CharField(max_length = 50)
	Sale_descript = models.CharField(max_length = 50)
	
class View_Count(models.Model):
	sale = models.ForeignKey(Posted_Sale, on_delete=models.CASCADE)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	class Meta:
		unique_together=('sale', 'user');  #so the view is unique per user! and to get the number of fiew it is enough to do filter(...).count()
		
	def save(self, *args, **kwargs):
		if not View_Count.objects.filter(sale =self.sale, user=self.user).exists():  #fastest way to check if it exists
			super(View_Count, self).save(*args, **kwargs)
		query = View_Count.objects.filter(sale =self.sale)
		counter = len(query)
		usrs = ""
		for i in range(0,counter):
			usrs += str(query[i].user.username)
			if i<counter -1 :
				usrs +=', '
		return {'counter':counter,'viewers':usrs}
	

