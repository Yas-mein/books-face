
from django.contrib import admin
from django.urls import path 
from django.conf.urls.static import static
from django.conf.urls import include


from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from facerecognition import views as vfr
# from Books import views as vb
# from Books.views import ToggleFavoriteBook

# app_name = 'detectobject'


urlpatterns = [
    path('admin/', admin.site.urls), # admin username : admins & pass : admins@api
    
    # path('api/all-books/',vb.BookListAPIView.as_view()),
    # path('api/all-books/<int:pk>',vb.oneBOOK.as_view()),
    # path('api/all-books/<int:pk>/favorit',ToggleFavoriteBook.as_view(), name='toggle_favorite_book'),
    # path('api/favorite-books/', vb.FavoriteBooksList.as_view(), name='favorite_books_list'),
    # # #update all books with their new_position
    # path('api/all-books/<int:pk>/update/', vb.BUpdateAPI.as_view()),
    
    path('api/recognation/',vfr.face_recognition_api ),
    path('api/recognation/cs/',vfr.capture_and_save_image ),
    
    # path('api/detection/', include('detectobject.urls')), 
    # path('api-auth/', include('rest_framework.urls')),

]
