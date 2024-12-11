# models.py (RecipeUser Model)
from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin
    )
# class RecipeUser(models.Model):

#     username = models.CharField(max_length=255)
#     email = models.EmailField(unique=True)
#     password = models.CharField(max_length=255)
#     role = models.CharField(choices=ROLE_CHOICES, max_length=10)
#     date_joined = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.username
# models.py (Recipe Model)


from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager, Group, Permission
ROLE_CHOICES = [
        ('creator', 'Creator'),
        ('viewer', 'Viewer'),
    ]
# class RecipeUser(AbstractBaseUser, PermissionsMixin):
#     id = models.BigAutoField(primary_key=True)
#     user_name = models.CharField(max_length=100, null=False)
#     user_id = models.CharField(max_length=100, null=False, unique=True)  # Updated to username
#     user_mobile = models.CharField(max_length=50, null=True, blank=True)
#     user_email = models.EmailField(verbose_name='email address', max_length=50, null=True, blank=True)
#     is_active = models.BooleanField(default=True)
#     is_admin = models.BooleanField(default=False)
#     role = models.CharField(choices=ROLE_CHOICES, max_length=10)
    
#     groups = models.ManyToManyField(
#         Group,
#         related_name="recipe_user_groups",  # Set a unique related name
#         blank=True,
#         verbose_name="groups",
#         help_text="The groups this user belongs to."
#     )
#     user_permissions = models.ManyToManyField(
#         Permission,
#         related_name="recipe_user_permissions",  # Set a unique related name
#         blank=True,
#         verbose_name="user permissions",
#         help_text="Specific permissions for this user."
#     )

#     class Meta:
#         db_table = "RecipeUser"

#     USERNAME_FIELD = 'user_id' 
#     REQUIRED_FIELDS = ['user_email', 'user_name']

#     def __str__(self):
#         return f"{self.id} - {self.user_name}"

from django.db import models

class RecipeUserManager(BaseUserManager):
    def create_user(self, user_id,user_email, user_name, password, **extra_fields):
        """
        Creates and saves a User with the given userId, firstname and password.
        """
        if not user_id:
            raise ValueError('Users must have a user ID')

        user = self.model(
            user_id=user_id,
            user_email=user_email,
            user_name=user_name,
            password=password,
            **extra_fields,
        )

        user.set_password(password)
        user.is_user_admin = True
        user.save(using=self._db)
        return user

    def create_superuser(self, user_id, user_email, user_name, password,  **extra_fields):
        """
        Creates and saves a superuser with the userId, firstname and password.
        """
        user = self.create_user(
            user_id,
            user_email,
            user_name,
            password=password,
            **extra_fields,
        )
        user.is_admin = True
 
        user.save(using=self._db)
        return user

# """ sesipl Users """

class RecipeUser(AbstractBaseUser, PermissionsMixin):
    id = models.BigAutoField(primary_key=True)
    user_id = models.CharField(max_length=255, null=False, unique = True)
    user_name = models.CharField(max_length=100, null=False)
    user_mobile = models.CharField(max_length=50, null=True, blank=True)
    user_email = models.EmailField(verbose_name='email address', max_length=50, null=True,blank=True)
    is_user_admin = models.BooleanField(verbose_name='sesipl admin', default=False)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    role = models.CharField(choices=ROLE_CHOICES, max_length=10)
   
    class Meta:
        db_table = "RecipeUser"

    objects = RecipeUserManager()

    USERNAME_FIELD =  'user_id' 
    REQUIRED_FIELDS = ['user_email', 'user_name']

    def __str__(self):
        return "{}".format(self.user_name)
    
    
    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_user_admin

    @property
    def is_superuser(self):
        "Is the user a superuser?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

   
class Ingredient(models.Model):
    name = models.CharField(max_length=255)
    picture = models.ImageField(upload_to='ingredients/',null=True,blank=True)
    
    def __str__(self):
        return self.name

class Recipe(models.Model):
    creator = models.ForeignKey(RecipeUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    ingredients = models.ManyToManyField(Ingredient)
    instructions = models.TextField()
    prep_duration = models.IntegerField()  # Duration in minutes
    cook_duration = models.IntegerField()  # Duration in minutes
    thumbnail_image = models.ImageField(upload_to='recipes/thumbnails/',null=True,blank=True)
    step_by_step_images = models.ManyToManyField('StepImage')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class StepImage(models.Model):
    step_number = models.IntegerField()
    image = models.ImageField(upload_to='recipes/steps/')

    def __str__(self):
        return f"Step {self.step_number}"

class Favorite(models.Model):
    user = models.ForeignKey(RecipeUser, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'recipe') 
    def __str__(self):
        return f"{self.user.user_id} favorited {self.recipe.title}"
