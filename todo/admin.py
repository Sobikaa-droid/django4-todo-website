from django.contrib import admin
from .models import Todo


class TodoAdmin(admin.ModelAdmin):
    readonly_fields = ('creation_date',)


admin.site.register(Todo, TodoAdmin)  # what models to appear inside of the admin
