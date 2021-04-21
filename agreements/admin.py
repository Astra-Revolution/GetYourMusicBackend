from django.contrib import admin
from .models import ContractState, Contract, Qualification

# Register your models here.
admin.site.register(ContractState)
admin.site.register(Contract)
admin.site.register(Qualification)
