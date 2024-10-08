from django.contrib import admin
from .models import Address, LawyerDetails, LawyerDocuments, Lawyerdataset, Booking

class AddressAdmin(admin.ModelAdmin):
    list_display = ('user', 'location', 'district', 'province')

admin.site.register(Address, AddressAdmin)

class LawyerDetailsAdmin(admin.ModelAdmin):
    list_display = ('user', 'bar_license', 'status')
    list_filter = ('status',)
    search_fields = ('user__username', 'bar_license')
    actions = ['approve_lawyers', 'reject_lawyers']

    
    def approve_lawyers(self, request, queryset):
        queryset.update(status='approved')

    def reject_lawyers(self, request, queryset):
        queryset.update(status='rejected')

admin.site.register(LawyerDetails, LawyerDetailsAdmin)

class LawyerDocumentsAdmin(admin.ModelAdmin):
    list_display = ('user', 'license_certificate', 'citizenship_document', 'personal_photos')

admin.site.register(LawyerDocuments, LawyerDocumentsAdmin)

class LawyerdatasetAdmin(admin.ModelAdmin):
    list_display = ('name', 'experiece', 'average_case_completion_days', 'bar_license','rating', 'province')

admin.site.register(Lawyerdataset)
admin.site.register(Booking)