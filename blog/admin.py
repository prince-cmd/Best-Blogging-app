from django.contrib import admin

# Register your models here.

from blog.models import Post, BlogComment

admin.site.register(( BlogComment))

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    class Media:
        js= ('tinyInject.js',)

