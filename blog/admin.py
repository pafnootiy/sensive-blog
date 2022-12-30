from django.contrib import admin
from  .models import Post, Tag, Comment

 
class CommentAdmin(admin.ModelAdmin):
    raw_id_fields = ("text",)
    list_display = ('post', 'author')

 
class PostAdmin(admin.ModelAdmin):
    raw_id_fields = ("title","text")
    list_display = ('text', 'author')
 

    

admin.site.register(Post)
admin.site.register(Tag)
admin.site.register(Comment)
