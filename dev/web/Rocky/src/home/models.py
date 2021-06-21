from django.db import models

# Create your models here.


from django.db import models


class DeviceInfo(models.Model):
    address         =   models.CharField(max_length = 256, blank=True, null=True)
    device_info     =   models.CharField(max_length = 256, blank=True, null=True)
    url             =   models.CharField(max_length = 256, blank=True, null=True)
    is_admin_url    =   models.BooleanField(default = False)
    comments        =   models.CharField(max_length = 256, blank=True, null=True)

    created_on              = models.DateTimeField(auto_now_add=True, null = True, blank  =True)
    updated_on              = models.DateTimeField(auto_now=True, null = True, blank  =True)


    class Meta:
        db_table            = "tbl_device_info"
        verbose_name        = "Device Info"
        verbose_name_plural = "Device Info"

    def __str__(self):
        return f'{self.address} - {self.created_on}'


class SugarDonations(models.Model):
    name 					= models.CharField(max_length = 12, blank=True, null=True)
    contact_number			= models.CharField(max_length = 12, blank=True, null=True)
    amount 					= models.IntegerField(default = 0)

    created_on              = models.DateTimeField(auto_now_add=True, null = True, blank  =True)
    updated_on 			    = models.DateTimeField(auto_now=True, null = True, blank  =True)


    class Meta:
        db_table            = "tbl_sugarcamp"
        verbose_name        = "Sugar Donation Entry"
        verbose_name_plural = "Sugar Donation Entries"

    def __str__(self):
        return f'{self.name} - {self.amount}'


    def sugar_in_grams(self):
    	grams = int((self.amount/43)*1000)
    	if grams > 9999:
    		kgs = grams/1000
    		return f'{kgs} KGs'
    	return f'{grams} grams'

    def total_donation(self):
    	return sum([int((t.amount/43)*1000) for t in SugarDonations.objects.all()])/1000