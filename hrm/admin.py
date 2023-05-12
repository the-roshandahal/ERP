from django.contrib import admin
from .models import *
# Register your models here.


admin.site.register(Salary)
admin.site.register(Leave)
admin.site.register(LeaveDate)
admin.site.register(Department)
admin.site.register(Designation)
admin.site.register(MonthSetup)
admin.site.register(YearSetup)
admin.site.register(Holidays)
admin.site.register(Employee)
admin.site.register(LogSheet)


admin.site.register(DeviceAttendance)
admin.site.register(DeviceAttendanceUser)
admin.site.register(DeviceData)