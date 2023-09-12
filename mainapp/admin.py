from django.contrib import admin
from .models import profile,Post,likepost,followscount

# Register your models h
admin.site.register(profile)
admin.site.register(Post)
admin.site.register(likepost)
admin.site.register(followscount)