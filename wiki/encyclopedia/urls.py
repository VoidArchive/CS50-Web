from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.show_entry, name="entry"),
    path("search", views.search, name="search"),
    path("random",views.random_entry, name="random"),
    path("newPage",views.new_page,name="newPage"),
    path("edit/<str:title>",views.edit_page,name="editPage")
    

]
