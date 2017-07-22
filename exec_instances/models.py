from django.db import models

class ExecInstance(models.Model):
    title = models.CharField(max_length=100,default='[no title]') 
    grid_size = models.IntegerField(default=0)

    def __str__(self):
        return self.title

class RegisteredElement(models.Model):
    exec_instance = models.ForeignKey('ExecInstance', on_delete=models.CASCADE)
    element_id = models.CharField(max_length=5)
    element_name = models.CharField(max_length=100)

    def __str__(self):
       return self.exec_instance + ", " + self.element_name

class ElementParseRule(models.Model):
    registered_element = models.ForeignKey('RegisteredElement', on_delete=models.CASCADE)
    element_member_name = models.CharField(max_length=200)
    element_member_position = models.IntegerField()

    def __str__(self):
        return self.registered_element + ", " + self.element_member_name + ", position: " + self.element.member_position

class AEPS(models.Model):
    exec_instance = models.ForeignKey('ExecInstance', on_delete=models.CASCADE)
    aeps = models.IntegerField()

    def __str__(self):
        return self.exec_instance + ", " + self.aeps

class Site(models.Model):
    aeps = models.ForeignKey('AEPS',on_delete=models.CASCADE)
    x = models.IntegerField()
    y = models.IntegerField()
    val = models.CharField(max_length=24)
    atom_type = models.CharField(max_length=5)

    def __str__(self):
        xy = str(self.x), str(self.y)
        return self.aeps + ", " + self.xy

class SiteDetail(models.Model):
    site = models.ForeignKey('Site', on_delete=models.CASCADE)
    atom_member_name = models.CharField(max_length=200)
    atom_member_value = models.CharField(max_length=96)

    def __str__(self):
        return self.site + ", " + self.atom_member_name + ": " + self.atom_member_value
