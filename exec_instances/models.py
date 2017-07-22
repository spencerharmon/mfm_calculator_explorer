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
        return '{0}, {1}'.format(
            self.exec_instance,
            self.element_name
        )

class ElementParseRule(models.Model):
    registered_element = models.ForeignKey('RegisteredElement', on_delete=models.CASCADE)
    element_member_name = models.CharField(max_length=200)
    element_member_position = models.IntegerField()

    def __str__(self):
        return '{0}, {1}, position: {2}'.format(
            self.registered_element,
            self.element_member_name,
            self.element.member_position
        )

class AEPS(models.Model):
    exec_instance = models.ForeignKey('ExecInstance', on_delete=models.CASCADE)
    aeps = models.IntegerField()

    def __str__(self):
        return '{0}, {1}'.format(
            self.exec_instance,
            self.aeps
        )

class LogMessage(models.Model):
    aeps = models.ForeignKey('AEPS',on_delete=models.CASCADE)
    message = models.CharField(max_length=500)
    actual_aeps = models.CharField(max_length=50)

    def __str__(self):
        return '{0}, {1}'.format(
            self.aeps,
            self.actual_aeps
        )

class Site(models.Model):
    aeps = models.ForeignKey('AEPS',on_delete=models.CASCADE)
    x = models.IntegerField()
    y = models.IntegerField()
    val = models.CharField(max_length=24)
    atom_type = models.CharField(max_length=5)

    def __str__(self):
        xy = '{0},{1}'.format(self.x,self.y)
        return '{0}, {1}'.format(
            self.aeps,
            xy
        )

class SiteDetail(models.Model):
    site = models.ForeignKey('Site', on_delete=models.CASCADE)
    atom_member_name = models.CharField(max_length=200)
    atom_member_value = models.CharField(max_length=96)

    def __str__(self):
        return '{0}, {1}: {2}'.format(
            self.site,
            self.atom_member_name,
            self.atom_member_value
        )
