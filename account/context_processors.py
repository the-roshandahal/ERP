from hrm.models import *
from django.template.context_processors import request
from features.models import Company

def custom_data(request):
    permissions = []
    company=None
    if request.user.is_authenticated:
        logged_in_user = User.objects.get(username=request.user)
        user = Employee.objects.get(user=logged_in_user)
        role=Role.objects.get(role=user.permission)
        permission=Permission.objects.get(role=role)
        company = Company.objects.all().order_by('-created').first()
        

        if permission.create_account or permission.read_account or permission.update_account or permission.delete_account:
            permissions.append('account')
        if permission.create_finance or permission.read_finance or permission.update_finance or permission.delete_finance:
            permissions.append('finance')
        if permission.create_hrm or permission.read_hrm or permission.update_hrm or permission.delete_hrm:
            permissions.append('hrm')
        if permission.create_products or permission.read_products or permission.update_products or permission.delete_products:
            permissions.append('products')
        if permission.create_leads or permission.read_leads or permission.update_leads or permission.delete_leads or permission.manage_leads:
            permissions.append('leads')


        if permission.create_account:
            permissions.append('create_account')
        if permission.read_account:
            permissions.append('read_account')
        if permission.update_account:
            permissions.append('update_account')
        if permission.delete_account:
            permissions.append('delete_account')


        if permission.create_finance:
            permissions.append('create_finance')
        if permission.read_finance:
            permissions.append('read_finance')
        if permission.update_finance:
            permissions.append('update_finance')
        if permission.delete_finance:
            permissions.append('delete_finance')


        if permission.create_leads:
            permissions.append('create_leads')
        if permission.read_leads:
            permissions.append('read_leads')
        if permission.update_leads:
            permissions.append('update_leads')
        if permission.delete_leads:
            permissions.append('delete_leads')
        if permission.manage_leads:
            permissions.append('manage_leads')


        if permission.create_hrm:
            permissions.append('create_hrm')
        if permission.read_hrm:
            permissions.append('read_hrm')
        if permission.update_hrm:
            permissions.append('update_hrm')
        if permission.delete_hrm:
            permissions.append('delete_hrm')


        if permission.create_products:
            permissions.append('create_products')
        if permission.read_products:
            permissions.append('read_products')
        if permission.update_products:
            permissions.append('update_products')
        if permission.delete_products:
            permissions.append('delete_products')
        
        
        if permission.manage_company:
            permissions.append('manage_company')


        return {'permissions': permissions,'company':company}
    else:
        return {'permissions': permissions,'company':company}
    return {'permissions': permissions,'company':company}

# def company_details(request):
#     if request.user.is_authenticated:
        
#         return {}
    # else:
    #     return redirect('home')

# def exclude_processor(request):
#     excluded_templates = ['login.html']

#     if request.resolver_match and request.resolver_match.url_name in excluded_templates:
#         return {}
#     else:
#         return {'custom_data': custom_data(request)}

# def combined_processors(request):
#     return {
#         'custom_data': exclude_processor(request),
#     }


def custom_data_views(request):
    
    views_permissions = []
    if request.user.is_authenticated:
        logged_in_user = User.objects.get(username=request.user)
        user = Employee.objects.get(user=logged_in_user)
        role=Role.objects.get(role=user.permission)
        permission=Permission.objects.get(role=role)

        if permission.create_account or permission.read_account or permission.update_account or permission.delete_account:
            views_permissions.append('account')
        if permission.create_finance or permission.read_finance or permission.update_finance or permission.delete_finance:
            views_permissions.append('finance')
        if permission.create_hrm or permission.read_hrm or permission.update_hrm or permission.delete_hrm:
            views_permissions.append('hrm')
        if permission.create_products or permission.read_products or permission.update_products or permission.delete_products:
            views_permissions.append('products')
        if permission.create_leads or permission.read_leads or permission.update_leads or permission.delete_leads or permission.manage_leads:
            views_permissions.append('leads')


        if permission.create_account:
            views_permissions.append('create_account')
        if permission.read_account:
            views_permissions.append('read_account')
        if permission.update_account:
            views_permissions.append('update_account')
        if permission.delete_account:
            views_permissions.append('delete_account')


        if permission.create_finance:
            views_permissions.append('create_finance')
        if permission.read_finance:
            views_permissions.append('read_finance')
        if permission.update_finance:
            views_permissions.append('update_finance')
        if permission.delete_finance:
            views_permissions.append('delete_finance')


        if permission.create_leads:
            views_permissions.append('create_leads')
        if permission.read_leads:
            views_permissions.append('read_leads')
        if permission.update_leads:
            views_permissions.append('update_leads')
        if permission.delete_leads:
            views_permissions.append('delete_leads')
        if permission.manage_leads:
            views_permissions.append('manage_leads')


        if permission.create_hrm:
            views_permissions.append('create_hrm')
        if permission.read_hrm:
            views_permissions.append('read_hrm')
        if permission.update_hrm:
            views_permissions.append('update_hrm')
        if permission.delete_hrm:
            views_permissions.append('delete_hrm')


        if permission.create_products:
            views_permissions.append('create_products')
        if permission.read_products:
            views_permissions.append('read_products')
        if permission.update_products:
            views_permissions.append('update_products')
        if permission.delete_products:
            views_permissions.append('delete_products')
        
        
        if permission.manage_company:
            views_permissions.append('manage_company')
        
        return views_permissions
    else:
        return views_permissions
