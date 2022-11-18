from datetime import datetime
from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from .models import BankStatement, WithdrawalRequest, DepositRequest
from .forms import AuditDataForm
from django.http import HttpRequest, HttpResponseRedirect
from rangefilter.filters import DateRangeFilter, DateTimeRangeFilter, NumericRangeFilter



admin.site.site_header = "Audit System Admin"
admin.site.site_title = "Audit System Portal"
admin.site.index_title = "Welcome to Audit System Portal"
# Register your models here.

class BankStatementResource(resources.ModelResource):
    def after_save_instance(self, instance, using_transactions, dry_run):
        # the model instance will have been saved at this point, and will have a pk
        print(instance.id)

    class Meta:
        model = BankStatement
        import_id_fields = ('pk',)
        skip_unchanged = True
        report_skipped = False
        fields = ('pk','date', 'customer', 'amount', 'type')
        export_order = fields
        


@admin.register(BankStatement)
class BankStatementIEAdmin(ImportExportModelAdmin):
    # list_display = BookAdmin._meta.get_all_field_names()
    listDisplay = [field.name for field in BankStatement._meta.get_fields()]
    listDisplay.append("show_average")
    list_display = listDisplay
    list_filter = ("status", 'type', 'date')
    resource_class = BankStatementResource

    def show_average(self, obj):
        result = BankStatement.objects.get(pk=obj.pk)
        return (result.amount/result.pk)
    

class WithdrawalRequestResource(resources.ModelResource):
    def after_save_instance(self, instance, using_transactions, dry_run):
        # the model instance will have been saved at this point, and will have a pk
        print(instance.id)

    class Meta:
        model = WithdrawalRequest
        import_id_fields = ('user_id',)
        skip_unchanged = True
        report_skipped = False
        fields = ('user_id', 'amount', 'customer', 'bank_name', 'date', 'status')


@admin.register(WithdrawalRequest)
class WithdrawalRequestEAdmin(ImportExportModelAdmin):
    # list_display = BookAdmin._meta.get_all_field_names()
    listDisplay = [field.name for field in WithdrawalRequest._meta.get_fields()]
    # listDisplay = []
    listDisplay.append("data_matched")

    list_display = listDisplay
    list_filter = (
        ('audit_date', DateRangeFilter),
        ('amount', NumericRangeFilter),
        'status'
    )
    resource_class = WithdrawalRequestResource

    @admin.display(boolean=True)
    def data_matched(self, obj):
        try:
            nameStatus = []
            number_of_names = str(obj.name).split(" ")

            for names in number_of_names:
                try:
                    print("Try---", names)
                    i = BankStatement.objects.filter(
                        customer__contains=names, amount=obj.amount).count()
                    nameStatus.append(bool(i))
                except Exception as es:
                    print("EXCEPTION", es)
                    nameStatus.append(False)
            print("========================================================")
            print(nameStatus)
            print(number_of_names)
            print("========================================================")
            if len(number_of_names) == len(nameStatus) and not False in nameStatus:
                # matched = DataFix.objects.get(
                #     amount=obj.amount)
                print('nameStatus condition TRUE')
                return True
            else:
                return False

        except Exception as ex:
            return False



class DepositRequestResource(resources.ModelResource):
    def after_save_instance(self, instance, using_transactions, dry_run):
        # the model instance will have been saved at this point, and will have a pk
        print(instance.id)

    class Meta:
        model = DepositRequest
        import_id_fields = ('user_id',)
        skip_unchanged = True
        report_skipped = False
        fields = ('user_id', 'amount', 'customer', 'bank_name', 'date', 'status')

@admin.register(DepositRequest)
class DepositRequestEAdmin(ImportExportModelAdmin):
    # list_display = BookAdmin._meta.get_all_field_names()
    listDisplay = [field.name for field in DepositRequest._meta.get_fields()]
    listDisplay.append("data_matched")
    
    list_display = listDisplay
    list_filter = (
        ('audit_date', DateRangeFilter),
        ('amount', NumericRangeFilter),
        'status'
    )

    # If you would like to add a default range filter
    # method pattern "get_rangefilter_{field_name}_default"
    # def get_rangefilter_created_at_default(self, request):
    #     return (datetime.date.today, datetime.date.today)

    # If you would like to change a title range filter
    # method pattern "get_rangefilter_{field_name}_title"
    # def get_rangefilter_created_at_title(self, request, field_path):
    #     return 'custom title'


    resource_class = DepositRequestResource

    @admin.display(boolean=True)
    def data_matched(self, obj):
        try:
            nameStatus = []
            number_of_names = str(obj.name).split(" ")

            for names in number_of_names:
                try:
                    print("Try---", names)
                    i = BankStatement.objects.filter(
                        customer__contains=names, amount=obj.amount).count()
                    nameStatus.append(bool(i))
                except Exception as es:
                    print("EXCEPTION", es)
                    nameStatus.append(False)
            print("========================================================")
            print(nameStatus)
            print(number_of_names)
            print("========================================================")
            if len(number_of_names) == len(nameStatus) and not False in nameStatus:
                # matched = DataFix.objects.get(
                #     amount=obj.amount)
                print('nameStatus condition TRUE')
                return True
            else:
                return False

        except Exception as ex:
            return False



