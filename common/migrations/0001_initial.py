# Generated by Django 4.0.3 on 2023-08-05 04:50

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CoatCompanyModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('coated_company', models.CharField(max_length=25, verbose_name='코팅업체')),
            ],
        ),
        migrations.CreateModel(
            name='DataOneRow',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('w1_value', models.IntegerField(default=0, verbose_name='w1')),
                ('w2_value', models.IntegerField(default=0, verbose_name='w2')),
                ('w3_value', models.IntegerField(default=0, verbose_name='w3')),
                ('h_value', models.IntegerField(default=0, verbose_name='h')),
                ('A_value_quantity', models.IntegerField(default=0, verbose_name='A 수량')),
                ('B_value_quantity', models.IntegerField(default=0, verbose_name='B 수량')),
                ('C_value_quantity', models.IntegerField(default=0, verbose_name='C 수량')),
                ('A_Area', models.DecimalField(decimal_places=2, default=0, max_digits=6, verbose_name='A 면적')),
                ('B_Area', models.DecimalField(decimal_places=2, default=0, max_digits=6, verbose_name='B 면적')),
                ('C_Area', models.DecimalField(decimal_places=2, default=0, max_digits=6, verbose_name='C 면적')),
            ],
        ),
        migrations.CreateModel(
            name='DetailedData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_writed', models.DateTimeField(auto_now_add=True, verbose_name='최초작성시간')),
                ('last_modified', models.DateTimeField(auto_now=True, verbose_name='마지막변경시간')),
                ('changes_log', models.CharField(max_length=50, verbose_name='변경내역')),
                ('data_rows', models.ManyToManyField(to='common.dataonerow')),
            ],
        ),
        migrations.CreateModel(
            name='ProductList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product', models.CharField(max_length=30, verbose_name='품명')),
            ],
        ),
        migrations.CreateModel(
            name='TheOneDistrict',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(default='기본값', max_length=20, verbose_name='카테고리')),
                ('company', models.CharField(max_length=20, verbose_name='업체명')),
                ('location_name', models.CharField(max_length=40, verbose_name='현장명')),
                ('district', models.CharField(max_length=20, verbose_name='동')),
                ('detailData', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='common.detaileddata')),
            ],
        ),
        migrations.AddField(
            model_name='dataonerow',
            name='product_name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='common.productlist'),
        ),
        migrations.CreateModel(
            name='BaseData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('finishing_date', models.DateField(default=django.utils.timezone.now, verbose_name='작업시기')),
                ('coated_company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='common.coatcompanymodel')),
                ('one_district', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='common.theonedistrict')),
            ],
        ),
    ]