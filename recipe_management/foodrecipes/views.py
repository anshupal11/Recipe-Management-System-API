from .models import Recipe, Ingredient, Favorite, RecipeUser
from .serializers import RegisterSerializer,LoginSerializer,FavoriteSerializer,RecipeSerializer
import pandas as pd
from rest_framework.views import APIView
from django.db import transaction
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated,BasePermission
from .models import Recipe, Favorite
from rest_framework import serializers
from reportlab.pdfgen import canvas
from django.http import HttpResponse

# Create a new User
class RegisterAPIView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# User Login 
class LoginAPIView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# permission only view by viewer
class IsViewerPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'viewer'

# permission only view by Creator 
class IsCreatorPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'creator' # define in models
    

# Generate PDF
class RecipePDF(APIView):
    permission_classes = [IsAuthenticated,IsViewerPermission]
    def get(self, request, pk):
        recipe = Recipe.objects.get(pk=pk)
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{recipe.title}.pdf"'

        pdf = canvas.Canvas(response)
        pdf.drawString(100, 800, recipe.title)
        pdf.drawString(100, 780, recipe.description)

        pdf.save()
        return response



    
class FavoriteRecipeAPIView(APIView):
    permission_classes = [IsAuthenticated,IsViewerPermission] # only done by Viewer


    def get(self, request,recipe_id):
        favorite = Favorite.objects.filter(user=request.user, recipe=recipe_id)
        serializer = FavoriteSerializer(favorite, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, recipe_id):
        try:
            recipe = Recipe.objects.get(pk=recipe_id)
            if Favorite.objects.filter(user=request.user, recipe=recipe).exists():
                raise serializers.ValidationError("Recipe is already marked as favorite")
            else:
                favorite = Favorite.objects.create(user=request.user, recipe=recipe)
                serializer = FavoriteSerializer(favorite)
                return Response({"message": "Recipe added in favorites successfully","data":serializer.data}, status=status.HTTP_201_CREATED)
        except Recipe.DoesNotExist:
            return Response({"error": "Recipe not found"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, recipe_id):
        try:
            recipe = Recipe.objects.get(pk=recipe_id)
            favorite = Favorite.objects.get(user=request.user, recipe=recipe)
            favorite.delete()
            return Response({"message": "Recipe removed from favorites successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Recipe.DoesNotExist:
            return Response({"error": "Recipe not found"}, status=status.HTTP_404_NOT_FOUND)
        except Favorite.DoesNotExist:
            return Response({"error": "Recipe is not in favorites"}, status=status.HTTP_404_NOT_FOUND)






# add buld Recipe by excel sheet

class BulkUploadRecipes(APIView):
    permission_classes = [IsAuthenticated,IsCreatorPermission]

    def post(self, request):
        file = request.FILES['file']
        try:
            df = pd.read_excel(file)

            with transaction.atomic():
                for _, row in df.iterrows():
                    recipe_data = {
                        "title": row["title"],
                        "description": row["description"],
                        "instructions": row["instructions"],
                        "prep_duration": row["prep_duration"],
                        "cook_duration": row["cook_duration"]
                    }
                    user = RecipeUser.objects.get(id=request.user.id)
                    recipe = Recipe.objects.create(creator=user, **recipe_data)
                    
                    # Add ingredients
                    ingredients = row["ingredients"].split(",")
                    for ingredient_name in ingredients:
                        ingredient, created = Ingredient.objects.get_or_create(name=ingredient_name.strip())
                        recipe.ingredients.add(ingredient)

            return Response({"message": "Recipes uploaded successfully!"}, status=201)

        except Exception as e:
            return Response({"error": str(e)}, status=400)






class RecipeAPIView(APIView):
    def get_permissions(self):
        # Use different permissions for different HTTP methods
        if self.request.method in ['POST', 'PUT', 'DELETE']:
            # For POST, PUT, and DELETE, user must be authenticated and have 'creator' role
            return [IsAuthenticated(), IsCreatorPermission()]
        else:
            # For GET, user just needs to be authenticated
            return [IsAuthenticated()]

    def get(self, request, pk=None):
        if pk:
            try:
                recipe = Recipe.objects.get(pk=pk)
                serializer = RecipeSerializer(recipe)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Recipe.DoesNotExist:
                return Response({"error": "Recipe not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            recipes = Recipe.objects.all()
            serializer = RecipeSerializer(recipes, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = RecipeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(creator=request.user)  # Assuming the creator is the authenticated user
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        try:
            recipe = Recipe.objects.get(pk=pk)
            serializer = RecipeSerializer(recipe, data=request.data, partial=True)  # Allow partial updates
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Recipe.DoesNotExist:
            return Response({"error": "Recipe not found"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        try:
            recipe = Recipe.objects.get(pk=pk)
            recipe.delete()
            return Response({"message": "Recipe deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Recipe.DoesNotExist:
            return Response({"error": "Recipe not found"}, status=status.HTTP_404_NOT_FOUND)
