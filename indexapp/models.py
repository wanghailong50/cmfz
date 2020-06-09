# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class DOrderiterm(models.Model):
    shop_bookid = models.ForeignKey('TBook', models.DO_NOTHING, db_column='shop_bookid')
    shop_ordid = models.ForeignKey('TOrder', models.DO_NOTHING, db_column='shop_ordid', blank=True, null=True)
    shop_num = models.IntegerField(blank=True, null=True)
    price=models.DecimalField(max_digits=8,decimal_places=2,null=True)
    uuid=models.TextField(blank=True, null=True)
    users_id=models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'd_orderiterm'






class TAddress(models.Model):
    name = models.CharField(max_length=20, blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    zipcode = models.CharField(max_length=20, blank=True, null=True)
    user = models.ForeignKey('TUser', models.DO_NOTHING, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    telephone = models.CharField(max_length=20, blank=True, null=True)
    class Meta:

        db_table = 't_address'


class TBook(models.Model):
    cate = models.ForeignKey('TCategory', models.DO_NOTHING, blank=True, null=True)
    book_name = models.CharField(max_length=128, blank=True, null=True)
    book_author = models.CharField(max_length=64, blank=True, null=True)
    book_publish = models.CharField(max_length=128, blank=True, null=True)
    publish_time = models.DateField(blank=True, null=True,auto_now_add=True)
    revision = models.IntegerField(blank=True, null=True)
    book_isbn = models.CharField(max_length=64, blank=True, null=True)
    word_count = models.CharField(max_length=64, blank=True, null=True)
    page_count = models.IntegerField(blank=True, null=True)
    open_type = models.CharField(max_length=20, blank=True, null=True)
    book_paper = models.CharField(max_length=64, blank=True, null=True)
    book_wrapper = models.CharField(max_length=64, blank=True, null=True)
    book_category = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    book_price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    book_dprice = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    editor_recommendation = models.TextField(blank=True, null=True)
    content_introduction = models.TextField(blank=True, null=True)
    author_introduction = models.TextField(blank=True, null=True)
    menu = models.TextField(blank=True, null=True)
    media_review = models.TextField(blank=True, null=True)
    digest_image_path = models.TextField(blank=True, null=True)
    product_image_path = models.ImageField(upload_to="pics",blank=True, null=True)
    series_name = models.CharField(max_length=128, blank=True, null=True)
    printing_time = models.DateTimeField(blank=True, null=True,auto_now_add=True)
    impression = models.CharField(max_length=64, blank=True, null=True)
    stock = models.IntegerField(blank=True, null=True)
    shelves_date = models.DateField(blank=True, null=True,auto_now_add=True)
    customer_socre = models.DecimalField(max_digits=2, decimal_places=1, blank=True, null=True)
    book_status = models.IntegerField(blank=True, null=True)
    sales = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 't_book'


class TCategory(models.Model):
    cate_name = models.CharField(max_length=20, blank=True, null=True)
    parent_id = models.IntegerField(blank=True, null=True)
    cate_level = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 't_category'


class TOrder(models.Model):
    t_u = models.ForeignKey('TUser', models.DO_NOTHING, blank=True, null=True)
    t_a = models.ForeignKey(TAddress, models.DO_NOTHING, blank=True, null=True)
    order_id = models.CharField(max_length=100, blank=True, null=True)
    create_date = models.DateTimeField(blank=True, null=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    order_addrid = models.IntegerField(null=True)
    order_uid = models.IntegerField(null=True)
    status = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 't_order'


class TShipping(models.Model):
    user = models.ForeignKey('TUser', models.DO_NOTHING, blank=True, null=True)
    order = models.ForeignKey(TBook, models.DO_NOTHING, blank=True, null=True)
    shop_num = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 't_shipping'


class TUser(models.Model):
    username = models.CharField(max_length=20, blank=True, null=True)
    password = models.CharField(max_length=20, blank=True, null=True)
    user_status = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 't_user'
