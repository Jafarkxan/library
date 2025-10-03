from django.urls import path
from rest_framework.routers import SimpleRouter
from .views import (BookListCreateApiView, BookDetailUpdateDeleteApiView,
                    BookListApiView,
                    BookDetailApiView,
                    BookDeleteApiView,
                    BookUpdateApiView,
                    BookCreateApiView, BookViewSet, )

router = SimpleRouter()
router.register('books', BookViewSet, basename='books')

urlpatterns = [
    # Best Practise
    # path('books/list/', BookListCreateApiView.as_view()),
    # path('books/detail/<int:pk>/', BookDetailUpdateDeleteApiView.as_view()),
    #
    # # Medium Efficient
    # path('books/', BookListApiView.as_view()),
    # path('books/<int:pk>/', BookDetailApiView.as_view()),
    # path('books/create/', BookCreateApiView.as_view()),
    # path('books/update/<int:pk>/', BookUpdateApiView.as_view()),
    # path('books/delete/<int:pk>/', BookDeleteApiView.as_view()),
]

urlpatterns = urlpatterns + router.urls