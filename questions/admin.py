from django.contrib import admin
from .models import Software_Engineer
from .models import Investment_Banking
from .models import Answer
from .models import Result

# Register your models here.
admin.site.register(Software_Engineer)
admin.site.register(Investment_Banking)
admin.site.register(Answer)
admin.site.register(Result)

