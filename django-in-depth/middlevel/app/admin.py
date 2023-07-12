from django.contrib import admin

from .models import Post, Access, PostPicture, File, FileAccess, Car

admin.site.register(Post)
admin.site.register(Access)
admin.site.register(PostPicture)

admin.site.register(File)
admin.site.register(FileAccess)

admin.site.register(Car)