from django.db import models
 
from django.contrib.auth.models import User
from . import utils
from django.db.models.signals import pre_save, post_save
from vehicles.models import Vehicles, TOLL_CHARGE
from tollgate.models import Tollgates, TollgateLogs



TTYPE_CHOICES = (
                    (0, 'Add Money'),
                    (1, 'Toll Charge'),
    )
TTYPE_CHOICES_DICT = {}
for v in TTYPE_CHOICES:
    TTYPE_CHOICES_DICT[str(v[0])] = v[1]


class UserProfile(models.Model):
    user                    = models.OneToOneField(User, on_delete=models.CASCADE, related_name = 'userprofile')
    otp                     = models.PositiveIntegerField(blank=True, null=True)
    otp_datetime            = models.DateTimeField(blank=True, null=True)
    profile_pic             = models.ImageField(blank=True, null=True)
    contact_number 			= models.CharField(max_length = 12, blank=True, null=True)
    email 					= models.CharField(max_length = 120, blank=True, null=True)
    wallet_balance          = models.IntegerField(default = 0)
    is_verified 			= models.BooleanField(default = False)

    created_on              = models.DateTimeField(auto_now_add=True, null = True, blank  =True)
    updated_on 			    = models.DateTimeField(auto_now=True, null = True, blank  =True)


    class Meta:
        db_table            = "tbl_userprofile"
        verbose_name        = "UserProfile"
        verbose_name_plural = "User Profiles"

    def __str__(self):
        return f'{self.user.id} - {self.user.username}'


class WalletTransactions(models.Model):
    transaction_id          = models.CharField(max_length = 128, null = True, blank  =True)
    user                    = models.ForeignKey(User, on_delete=models.CASCADE, related_name = 'wallet')
    amount                  = models.IntegerField(default = 0)
    ttype                   = models.IntegerField(choices = TTYPE_CHOICES, null = True, blank  =True)

    created_on              = models.DateTimeField(auto_now_add=True, null = True, blank  =True)
    updated_on              = models.DateTimeField(auto_now=True, null = True, blank  =True)

    class Meta:
        db_table            = "tbl_wallet_transactions"
        verbose_name        = "Wallet Transaction"
        verbose_name_plural = "Wallet Transactions"

    def __str__(self):
        return f'{self.transaction_id}'


def transaction_pre_save(sender, instance, *args, **kwargs):
    instance.transaction_id = utils.get_transaction_id() 
    user = instance.user
    if instance.ttype == 0:
        user.userprofile.wallet_balance +=  instance.amount
    else:
        user.userprofile.wallet_balance -=  instance.amount
    user.userprofile.save()

    

pre_save.connect(transaction_pre_save, sender = WalletTransactions)



class TollBillings(models.Model):
    ticket_number           =   models.CharField(max_length = 128, null=True, blank=True)
    vehicle                 =   models.ForeignKey(Vehicles, on_delete=models.CASCADE, related_name = 'toll_bill')
    tollgate_in             =   models.ForeignKey(TollgateLogs, on_delete=models.CASCADE, related_name = 'in_toll_bill', null=True, blank=True)
    tollgate_out            =   models.ForeignKey(TollgateLogs, on_delete=models.CASCADE, related_name = 'out_toll_bill', null=True, blank=True)
    transaction             =   models.OneToOneField(WalletTransactions, on_delete=models.CASCADE, related_name = 'toll_bill', null=True, blank=True)
    amount                  =   models.IntegerField(default = 0)
    distance                =   models.FloatField(default = 0)

    created_on              =   models.DateTimeField(auto_now_add=True, null = True, blank  =True)
    updated_on              =   models.DateTimeField(auto_now=True, null = True, blank  =True)

    class Meta:
        db_table            = "tbl_toll_billing"
        verbose_name        = "Toll Billing"
        verbose_name_plural = "Toll Billings"

    def __str__(self):
        return f'{self.vehicle} - {self.tollgate_in} -- {self.amount}'


def billing_pre_save(sender, instance, *args, **kwargs):
    #CALCULATE AMOUNT
    if not TollBillings.objects.filter(id = instance.id).exists():
        origin      = (float(instance.tollgate_in.tollgate.latitude), float(instance.tollgate_in.tollgate.longitude))
        destination = (float(instance.tollgate_out.tollgate.latitude), float(instance.tollgate_out.tollgate.longitude))
        distance        =   utils.get_distance(origin, destination)  #get_distance()   # in metres
        # print(f'DISTANCE: {distance}')
        bill_amount     =   TOLL_CHARGE[str(instance.vehicle.vtype)]*distance

        #TRANSACTION
        transaction = WalletTransactions.objects.create(
                                                            user    =   instance.vehicle.user,
                                                            ttype   =   1,
                                                            amount  =   max(bill_amount  , instance.tollgate_in.tollgate.min_charge)
                                                    )

        instance.distance       =   distance
        instance.amount         =   max(bill_amount  , instance.tollgate_in.tollgate.min_charge)
        instance.ticket_number  =   utils.get_ticket_number()  
        instance.transaction    =   transaction
        # print("SENDIND MESSAGE")
        utils.send_toll_bill_sms(instance)


def billing_post_save(sender, instance, *args, **kwargs):
    utils.send_toll_bill_sms(instance)

    
# post_save.connect(billing_post_save, sender = TollBillings)
pre_save.connect(billing_pre_save, sender = TollBillings)

















