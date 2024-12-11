from io import BytesIO
import pandas as pd
from .models import Recipe, Ingredient

def handle_bulk_upload(file):
    data = pd.read_excel(file)
    for _, row in data.iterrows():
        ingredients = []
        for ingredient_name in row['Ingredients'].split(','):
            ingredient, _ = Ingredient.objects.get_or_create(name=ingredient_name.strip())
            ingredients.append(ingredient)

        recipe = Recipe.objects.create(
            title=row['Title'],
            description=row['Description'],
            prep_duration=row['Prep Duration'],
            cook_duration=row['Cook Duration'],
            instructions=row['Instructions']
        )
        recipe.ingredients.set(ingredients)
        recipe.save()

from xhtml2pdf import pisa
from django.template.loader import render_to_string

def generate_pdf(recipe):
    html_string = render_to_string('recipe_pdf.html', {'recipe': recipe})
    pdf_buffer = BytesIO()
    pisa.CreatePDF(BytesIO(html_string.encode('utf-8')), dest=pdf_buffer)
    pdf_buffer.seek(0)
    return pdf_buffer
