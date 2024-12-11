from django.urls import path
from foodrecipes import views

# urlpatterns = [
#     path('recipes/', views.RecipeListCreateView.as_view(), name='recipe-list-create'),
#     path('recipes/<int:pk>/', views.RecipeDetailView.as_view(), name='recipe-detail'),
#     path('recipes/bulk-upload/', views.bulk_upload, name='recipe-bulk-upload'),
#     path('recipes/<int:pk>/download-pdf/', views.download_pdf, name='recipe-download-pdf'),
#     path('favourites/', views.FavouriteRecipeListCreateView.as_view(), name='favourite-list-create'),
#     path('favourites/<int:pk>/', views.FavouriteRecipeDetailView.as_view(), name='favourite-detail'),
# ]


urlpatterns = [
    path('favourites/<int:recipe_id>/', views.FavoriteRecipeAPIView.as_view(), name='favourite-detail'),
    path('recipe-pdf/<int:pk>/', views.RecipePDF.as_view(), name='recipe-pdf'),
    path('recipes/', views.RecipeAPIView.as_view(), name='recipes'),
    path('recipes/<int:pk>', views.RecipeAPIView.as_view(), name='recipes'),
    path('register/', views.RegisterAPIView.as_view(), name='register'),
    path('login/', views.LoginAPIView.as_view(), name='login'),
    path('bulk-upload/', views.BulkUploadRecipes.as_view(), name='bulk-upload'),
]