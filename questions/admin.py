from django.contrib import admin
from .models import Software_Engineer
from .models import Investment_Banking
from .models import Data_Scientist
from .models import DBA
from .models import ML_Engineer
from .models import Hardware_Engineer
from .models import Sales_Trading
from .models import Research
from .models import Quantitative
from .models import Audit
from .models import Answer
from .models import Result
from .models import Record
from .models import Video
from .models import Test_Job_pls_dont_add_shit_into_this_model_thank


# Register your models here.
admin.site.register(Software_Engineer)
admin.site.register(Investment_Banking)
admin.site.register(Data_Scientist)
admin.site.register(DBA)
admin.site.register(ML_Engineer)
admin.site.register(Hardware_Engineer)
admin.site.register(Sales_Trading)
admin.site.register(Research)
admin.site.register(Quantitative)
admin.site.register(Audit)
admin.site.register(Answer)
admin.site.register(Result)
admin.site.register(Record)
admin.site.register(Video)
# for testing purposes!!!!
admin.site.register(Test_Job_pls_dont_add_shit_into_this_model_thank)

