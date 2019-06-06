from django.contrib import admin


from  .models import High_risk_traffic

admin.site.register(High_risk_traffic)
admin.site.site_header = "web_admin"
admin.site.site_title = "web"