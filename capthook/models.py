from django.db import models


class Employee(models.Model):
    name = models.CharField(max_length=100)
    hometown = models.CharField(max_length=100)

    def __str__(self):
        return self.name + ', ' + self.hometown

    def serialize_hook(self, hook):
        return {
            'hook': hook.dict(),
            'data': {
                'id': self.id,
                'name': self.name,
                'hometown': self.hometown,
            }
        }

    def serialize_employee(self):
        from rest_hooks.signals import hook_event
        hook_event.send(
            sender=self.__class__,
            action='create',
            instance=self,
        )
        return {
            'hook': hook.dict(),
            'data': {
                'id': self.id,
                'name': self.name,
                'hometown': self.hometown,
            }
        }
