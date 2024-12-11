from rest_framework import serializers
from .models import Recipe, Ingredient, Favorite, RecipeUser
from rest_framework import serializers
from .models import Recipe, Ingredient

class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ['id', 'name', 'picture']

class RecipeSerializer(serializers.ModelSerializer):
    # Including ingredients as a nested serializer
    ingredients = IngredientSerializer(many=True)

    class Meta:
        model = Recipe
        # Add 'ingredients' to the fields list
        fields = ['title', 'description', 'instructions', 
                  'prep_duration', 'cook_duration', 'thumbnail_image', 
                  'created_at', 'updated_at', 'ingredients']  # Include 'ingredients'

    def create(self, validated_data):
        # Extract ingredients data from validated_data
        ingredients_data = validated_data.pop('ingredients', [])  # Get the ingredients list
        recipe = Recipe.objects.create(**validated_data)  # Create the recipe instance

        # Add ingredients to the recipe
        for ingredient_data in ingredients_data:
            ingredient, created = Ingredient.objects.get_or_create(**ingredient_data)  # Get or create each ingredient
            recipe.ingredients.add(ingredient)  # Add ingredient to the many-to-many relationship

        return recipe



class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipeUser
        fields = ['id', 'user_name','user_id', 'user_email', 'user_mobile', 'role', 'is_active']

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = RecipeUser
        fields = ['user_name','user_id', 'user_email', 'user_mobile', 'role', 'password']

    def create(self, validated_data):
        user = RecipeUser.objects.create(
            user_id = validated_data['user_id'],
            user_name=validated_data['user_name'],
            user_email=validated_data.get('user_email'),
            user_mobile=validated_data.get('user_mobile'),
            role=validated_data['role'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

from rest_framework_simplejwt.tokens import RefreshToken
class LoginSerializer(serializers.Serializer):
    user_id = serializers.CharField(required=True)  # Change this to 'username'
    password = serializers.CharField(write_only=True)
    token = serializers.CharField(read_only=True)

    def validate(self, data):
        # Get user by username
        user = RecipeUser.objects.filter(user_id=data['user_id']).first()  # Assuming `user_id` is the username field
        if user and user.check_password(data['password']) and user.is_active:
            refresh = RefreshToken.for_user(user)
            return {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                'user_role': user.role  # Assuming you need the user's role
            }
        else:
            raise serializers.ValidationError("Invalid credentials or inactive account")
