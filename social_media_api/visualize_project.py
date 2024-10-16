import os
from graphviz import Digraph
from django.apps import apps
from django.conf import settings
from django.urls import get_resolver

# Function to visualize directory structure
def visualize_directory_structure(root_dir):
    dot = Digraph(comment='Directory Structure')

    for root, dirs, files in os.walk(root_dir):
        root_basename = os.path.basename(root) or root_dir
        dot.node(root_basename, root_basename)

        for dir_name in dirs:
            dot.node(dir_name, dir_name)
            dot.edge(root_basename, dir_name)

        for file_name in files:
            dot.node(file_name, file_name)
            dot.edge(root_basename, file_name)

    dot.render('directory_structure', format='png', view=True)


# Function to visualize Django models and relationships
def visualize_model_relationships():
    dot = Digraph(comment='Django Model Relationships')

    # Loop through all the models in your project
    for model in apps.get_models():
        model_name = model.__name__
        fields = [f.name for f in model._meta.get_fields()]

        # Add node for each model
        dot.node(model_name, model_name)

        # Add field relationships (ForeignKey, OneToOne, etc.)
        for field in model._meta.get_fields():
            if field.is_relation and field.related_model is not None:
                related_model = field.related_model.__name__
                dot.edge(model_name, related_model, label=field.name)

    dot.render('model_relationships', format='png', view=True)


# Function to visualize View-Model and Serializer-Model relationships
def visualize_view_model_serializer_relationships():
    dot = Digraph(comment='View-Model-Serializer Relationships')

    # Manually map views to models and serializers based on your project
    # You should extend this as per your actual views and serializers

    # Example for User views
    dot.node('UserCreateView', 'UserCreateView')
    dot.node('UserSerializer', 'UserSerializer')
    dot.node('UserModel', 'User')

    dot.edge('UserCreateView', 'UserSerializer', label='uses')
    dot.edge('UserSerializer', 'UserModel', label='serializes')

    # Example for Post views
    dot.node('PostCreateView', 'PostCreateView')
    dot.node('PostSerializer', 'PostSerializer')
    dot.node('PostModel', 'Post')

    dot.edge('PostCreateView', 'PostSerializer', label='uses')
    dot.edge('PostSerializer', 'PostModel', label='serializes')

    dot.render('view_model_serializer_relationships', format='png', view=True)


# Function to visualize URL-View mappings
def visualize_url_view_mappings():
    dot = Digraph(comment='URL-View Mappings')

    # Control the size and aspect ratio of the graph
    dot.attr(size="10,10", ratio="auto", splines="true")

    # Get the URL resolver for your project
    resolver = get_resolver()

    def process_urls(urls, parent_name=None):
        for url in urls:
            if hasattr(url, 'url_patterns'):
                # Recursively process included URLs
                process_urls(url.url_patterns, parent_name=url.pattern.regex.pattern)
            else:
                # Get the view name
                view_name = str(url.callback).split(' ')[1]

                # Add node for each view
                dot.node(view_name, view_name)

                # Add edge from URL pattern to view
                if parent_name:
                    dot.node(parent_name, parent_name)
                    dot.edge(parent_name, view_name, label=url.pattern.regex.pattern)
                else:
                    dot.edge(url.pattern.regex.pattern, view_name)

    process_urls(resolver.url_patterns)

    # Render the PNG file with improved layout settings
    dot.render('url_view_mappings', format='png', view=True)



# Main function to call all visualizations
def run_visualizations():
    # Specify the root directory for your project
    project_root = 'social_media_api'

    # Create directory structure visualization
    print("Generating directory structure...")
    visualize_directory_structure(project_root)

    # Create model relationships visualization
    print("Generating model relationships...")
    visualize_model_relationships()

    # Create view-model-serializer relationships visualization
    print("Generating view-model-serializer relationships...")
    visualize_view_model_serializer_relationships()

    # Create URL-View mappings visualization
    print("Generating URL-View mappings...")
    visualize_url_view_mappings()


# Run the visualizations
if __name__ == "__main__":
    # Set up Django settings for model introspection
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'social_media_api.settings')
    import django
    django.setup()

    run_visualizations()
