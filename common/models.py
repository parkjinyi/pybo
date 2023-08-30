from django.db import models

# Create your models here.
from django.db import models
from jsonfield import JSONField
from django.db.models import F, Sum, Count, Case, When
from django.db.models.signals import pre_save
from django.dispatch import receiver
# from .helper import areaHelper
from django.utils import timezone

# Create your models here.

# 면적 계산 헬퍼 함수
def areaHelper(instance):    
    return round_half_up( ((instance.w1_value + instance.w2_value + instance.w3_value) * instance.h_value / Decimal(1000000)),2)


class Month(models.TextChoices):
    january     = '1월'
    febuary     = '2월'
    march       = '3월'
    april       = '4월'
    may         = '5월'
    june        = '6월'
    july        = '7월'
    augus       = '8월'
    september   = '9월'
    october     = ' 10월'
    november    = ' 11월'
    december    = ' 12월'


class CoatCompanyModel(models.Model):
    objects = models.Manager()
    coated_company      = models.CharField(max_length=25, verbose_name='코팅업체')
    def __str__(self):
        return self.coated_company


class ProductList(models.Model):
    objects = models.Manager()
    product = models.CharField(max_length=30, verbose_name='품명')
    
    def __str__(self):
        return self.product
        

class DataOneRow(models.Model):
    # TODO > Validation 추가해야함
    objects = models.Manager()
    product_name = models.ForeignKey(ProductList, on_delete=models.CASCADE,)
    w1_value = models.IntegerField(default=0, verbose_name='w1')
    w2_value = models.IntegerField(default=0, verbose_name='w2')
    w3_value = models.IntegerField(default=0, verbose_name='w3')
    h_value = models.IntegerField(default=0, verbose_name='h')
    
    A_value_quantity = models.IntegerField(default=0, verbose_name='A 수량')
    B_value_quantity = models.IntegerField(default=0, verbose_name='B 수량')
    C_value_quantity = models.IntegerField(default=0, verbose_name='C 수량')

    A_Area = models.DecimalField(verbose_name='A 면적', max_digits=6, decimal_places=2, default=0)
    B_Area = models.DecimalField(verbose_name='B 면적', max_digits=6, decimal_places=2, default=0)
    C_Area = models.DecimalField(verbose_name='C 면적', max_digits=6, decimal_places=2, default=0)

    def __str__(self):
        return f'{self.product_name}/ {self.w1_value}+{self.w2_value}+{self.w3_value} x {self.h_value}'
    

class DetailedData(models.Model):
    objects = models.Manager()
    data_rows = models.ManyToManyField(DataOneRow)
    first_writed = models.DateTimeField(verbose_name='최초작성시간', auto_now_add=True)
    last_modified = models.DateTimeField(verbose_name='마지막변경시간', auto_now=True)
    changes_log = models.CharField(verbose_name='변경내역', max_length=50)

    def __str__(self):
        return str(self.last_modified) + ' / ' + self.changes_log
    
    def sumHelper(self, field):
        val = self.data_rows.values(field).aggregate(Sum(field))
        return val[field+'__sum']

    @property
    def all_rows(self):
        return ', '.join([x.name for x in self.data_rows.all()])

    @property
    def a_value_quantity_sum(self):
        return self.sumHelper('A_value_quantity')

    @property    
    def b_value_quantity_sum(self):
        return self.sumHelper('B_value_quantity')

    @property
    def c_value_quantity_sum(self):
        return self.sumHelper('C_value_quantity')
    
    @property
    def A_Area_sum(self):
        return round(self.sumHelper('A_Area'), 2)
    
    @property
    def B_Area_sum(self):
        return round(self.sumHelper('B_Area'), 2)
    
    @property
    def C_Area_sum(self):
        return round(self.sumHelper('C_Area'), 2)
    
    @property
    def AandC_Area_sum(self):
        return round(self.sumHelper('A_Area') + self.sumHelper('C_Area'), 2)


class TheOneDistrict(models.Model):
    objects = models.Manager()
    # basedata            = models.ForeignKey(BaseData, on_delete=models.CASCADE, )
    category = models.CharField(max_length=20, verbose_name="카테고리", default="기본값")
    company = models.CharField(max_length=20, verbose_name="업체명")
    location_name = models.CharField(max_length=40, verbose_name="현장명")
    district = models.CharField(max_length=20, verbose_name="동")
    detailData = models.ForeignKey(DetailedData, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f'({self.company} . {self.location_name} . {self.district})'


class BaseData(models.Model):
    objects = models.Manager()
    coated_company = models.ForeignKey(CoatCompanyModel, on_delete=models.CASCADE)
    one_district   = models.OneToOneField(TheOneDistrict, on_delete=models.CASCADE, )
    finishing_date = models.DateField(verbose_name='작업시기', default=timezone.now)

    def __str__(self):
        return (self.coated_company.coated_company + '/' 
            + str(self.finishing_date.year) + '년/' + str(self.finishing_date.month) + '월' + ' ' 
            + str(self.finishing_date.day)+ '일/' + str(self.one_district))

    @property
    def worked_date(self):
        return self.finishing_date.day
    
    @property
    def date_strftime(self):
        return f'{self.finishing_date.year}년 {self.finishing_date.month}월 {self.finishing_date.day}일'

    
def get_yearList():
    vals = BaseData.objects.all().values('finishing_date')
    a_list = [ a.get('finishing_date', None).year for a in list(vals) ]
    return list(set(a_list))


# DataOneRow를 저장하기 전 면적을 계산하고 값을 넣음
@receiver(pre_save, sender=DataOneRow)
def post_delete(sender, instance, **kwargs):  
    instance.A_Area = areaHelper(instance) * instance.A_value_quantity
    instance.B_Area = areaHelper(instance) * instance.B_value_quantity
    instance.C_Area = areaHelper(instance) * instance.C_value_quantity
