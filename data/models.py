from django.db import models

class Note(models.Model):
    uid = models.CharField(max_length=20,blank=True,null=True)
    text = models.TextField(blank=True,null=True)
    wallet = models.TextField(blank=True,null=True)
    twitter = models.CharField(max_length=100,blank=True,null=True)
    only_twitter = models.BooleanField(default=False,null=False)
    is_wl = models.BooleanField(default=False,null=False)
    is_viewed = models.BooleanField(default=False,null=False)
    is_forever = models.BooleanField(default=False,null=False)

    def __str__(self):
        return self.uid



class Link(models.Model):
    note = models.ForeignKey(Note,on_delete=models.CASCADE,blank=True,null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    link = models.CharField(max_length=255, blank=True, null=True)


class Image(models.Model):
    note = models.ForeignKey(Note,on_delete=models.CASCADE,blank=True,null=True, related_name='images')
    file = models.FileField(upload_to='images',blank=True,null=True)