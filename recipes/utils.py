from io import BytesIO
import base64
import matplotlib.pyplot as plt
import pandas as pd

from .models import Category, Recipe, Tag

# ---------------------------
# Convert QuerySet/ID to readable name
# ---------------------------
def get_category_name_from_id(val):
    try:
        category = Category.objects.get(id=val)
        return category.name
    except Category.DoesNotExist:
        return "Unknown"

def get_tag_name_from_id(val):
    try:
        tag = Tag.objects.get(id=val)
        return tag.name
    except Tag.DoesNotExist:
        return "Unknown"

# ---------------------------
# Helper: Convert matplotlib plot to base64 image
# ---------------------------
def get_graph():
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')
    buffer.close()
    return graph

# ---------------------------
# Generate Chart Based on User Input
# chart_type: '#1'=Bar, '#2'=Pie, '#3'=Line
# recipes_qs: Recipe QuerySet
# ---------------------------
def get_chart(chart_type, recipes_qs):
    plt.switch_backend('AGG')  # render without GUI

    # Prepare DataFrame with computed fields
    data = []
    for recipe in recipes_qs:
        data.append({
            'name': recipe.name,
            'num_ingredients': recipe.recipe_ingredients.count(),
            'num_tags': recipe.tags.count(),
            'created_at': recipe.created_at if hasattr(recipe, 'created_at') else None,
        })

    if not data:
        return None

    df = pd.DataFrame(data)

    fig = plt.figure(figsize=(8, 5))

    if chart_type == '#1':  # Bar chart: x=recipe name, y=number of ingredients
        plt.bar(df['name'], df['num_ingredients'], color='#ff7e5f')
        plt.xlabel("Recipe Name")
        plt.ylabel("Number of Ingredients")
        plt.xticks(rotation=45, ha='right')
        plt.title("Ingredients per Recipe")

    elif chart_type == '#2':  # Pie chart: distribution of recipes per category
        # Count recipes per category
        category_counts = {}
        for recipe in recipes_qs:
            for cat in recipe.categories.all():
                category_counts[cat.name] = category_counts.get(cat.name, 0) + 1
        if not category_counts:
            return None
        labels = list(category_counts.keys())
        counts = list(category_counts.values())
        plt.pie(counts, labels=labels, autopct='%1.1f%%')
        plt.title("Recipe Distribution by Category")

    elif chart_type == '#3':  # Line chart: recipe created_at vs number of tags
        if df['created_at'].isnull().all():
            return None
        plt.plot(df['created_at'], df['num_tags'], marker='o', linestyle='-', color='#ff7e5f')
        plt.xlabel("Created At")
        plt.ylabel("Number of Tags")
        plt.xticks(rotation=45, ha='right')
        plt.title("Tags per Recipe Over Time")
    else:
        return None

    plt.tight_layout()
    chart = get_graph()
    plt.close(fig)  # free memory
    return chart
