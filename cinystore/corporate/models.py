from django.db import models


class Contact(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    Name = models.CharField(max_length=100)
    Email = models.EmailField(max_length=100)
    Subject = models.CharField(max_length=100)
    Message = models.TextField(max_length=5000)
    timestamp_field = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'contact'
        ordering = ['-timestamp_field']

    def __str__(self):
        return '%s - %s' % (self.Name, self.Subject)
