# Recipe-Management-System-API


## Overview
This API provides functionalities for managing recipes with two types of users: `Creator` and `Viewer`. 
- **Creators** can create, list, modify, and delete recipes. They can also upload recipes in bulk using an Excel sheet.
- **Viewers** can view recipes, mark them as favorites, and download recipe cards as PDFs.

Each recipe includes:
- Title
- Description
- Ingredients (with name and picture)
- Instructions
- Prep duration
- Cook duration
- Step-by-step pictures
- Thumbnail image

---

## Features
### User Management
- **Register:** Allows users to register.
- **Login:** Allows users to log in.

### Recipe Management
- **Create Recipes:** Creators can create recipes.
- **List Recipes:** Both Creators and Viewers can view recipes.
- **Update Recipes:** Creators can modify existing recipes.
- **Delete Recipes:** Creators can delete recipes.
- **Bulk Upload Recipes:** Creators can upload multiple recipes using an Excel sheet.

### Favorites
- **Mark as Favorite:** Viewers can mark recipes as their favorites.
- **List Favorites:** Viewers can view their favorite recipes.
- **Remove from Favorites:** Viewers can remove recipes from their favorites.

### Generate Recipe Card
- **Download PDF:** Viewers can download recipe cards as PDFs.

---

## API Endpoints

### Authentication
- `POST /register/` - Register a new user.
- `POST /login/` - Log in an existing user.

### Recipes
- `GET /recipes/` - List all recipes.
- `GET /recipes/{id}/` - Get details of a specific recipe.
- `POST /recipes/` - Create a new recipe (Creator only).
- `PUT /recipes/{id}/` - Update an existing recipe (Creator only).
- `DELETE /recipes/{id}/` - Delete a recipe (Creator only).

### Bulk Upload
- `POST /bulk-upload/` - Upload multiple recipes using an Excel file (Creator only).

### Favorites
- `GET /favorites/{recipe_id}/` - Get details of a favorite recipe (Viewer only).
- `POST /favorites/{recipe_id}/` - Mark a recipe as favorite (Viewer only).
- `DELETE /favorites/{recipe_id}/` - Remove a recipe from favorites (Viewer only).

### Generate PDF
- `GET /recipe-pdf/{id}/` - Download a recipe card as a PDF (Viewer only).

---

## Permissions

### Roles
1. **Creator**:
   - Can create, update, delete, and bulk upload recipes.
   - Cannot mark recipes as favorites or download recipe cards.

2. **Viewer**:
   - Can view recipes.
   - Can mark recipes as favorites.
   - Can download recipe cards as PDFs.
   - Cannot create, update, or delete recipes.

### Permissions Implementation
- **`IsViewerPermission`**: Ensures the user has the role `viewer`.
- **`IsCreatorPermission`**: Ensures the user has the role `creator`.

---

## Setup Instructions

### Prerequisites
1. Python 3.8+
2. Django Rest Framework
3. pandas library for Excel file processing
4. ReportLab library for PDF generation
5. Database setup (PostgreSQL preferred)

### Installation
1. Clone the repository:
   ```bash
   git clone <repository_url>
   cd <repository_folder>
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Apply migrations:
   ```bash
   python manage.py migrate
   ```

4. Start the development server:
   ```bash
   python manage.py runserver
   ```

### Bulk Upload File Format
Upload an Excel file with the following columns:
- `title`: Recipe title
- `description`: Recipe description
- `instructions`: Cooking instructions
- `prep_duration`: Preparation duration (in minutes)
- `cook_duration`: Cooking duration (in minutes)
- `ingredients`: Comma-separated list of ingredient names

Example:
| title       | description       | instructions      | prep_duration | cook_duration | ingredients          |
|-------------|-------------------|-------------------|---------------|---------------|----------------------|
| Pancakes    | Tasty pancakes   | Mix, cook, serve  | 10            | 15            | flour, eggs, milk    |

---


## Notes
- Make sure to define the `RecipeUser` model with the `creator` and `viewer` roles.
- Add appropriate validation in the serializers.
- Ensure proper error handling and atomic transactions for bulk uploads.
