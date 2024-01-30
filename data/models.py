from django.db import models

class Note(models.Model):
    uid = models.CharField(max_length=10,blank=True,null=True)
    text = models.TextField(blank=True,null=True)
    is_viewed = models.BooleanField(default=False,null=False)
    is_forever = models.BooleanField(default=False,null=False)


class Link(models.Model):
    note = models.ForeignKey(Note,on_delete=models.CASCADE,blank=True,null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    link = models.CharField(max_length=255, blank=True, null=True)


class Image(models.Model):
    note = models.ForeignKey(Note,on_delete=models.CASCADE,blank=True,null=True, related_name='images')
    file = models.FileField(upload_to='images',blank=True,null=True)