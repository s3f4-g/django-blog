from django.conf import  settings
from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from post.views import blog,index,post,search,post_delete,post_update,post_create

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, ),
    path('blog/', blog,name="post-list" ),
    path('search/', search,name="search" ),
    path('post/<id>/', post, name='post-detail' ),
    path('post/<id>/update/', post_update, name='post-update' ),
    path('post/<id>/delete/', post_delete, name='post-delete' ),
    path('create/', post_create, name="post-create" ),
    path("ckeditor5/", include('django_ckeditor_5.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),

]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


