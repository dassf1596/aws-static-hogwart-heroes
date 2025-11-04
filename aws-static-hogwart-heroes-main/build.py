import json
import os
import shutil
from jinja2 import Environment, FileSystemLoader

print("Starting static site generation...")

# --- Configuration ---
# Define source folders
DATA_FILE = os.path.join('data', 'heroes.json')
TEMPLATE_FOLDER = 'templates'
STATIC_FOLDER = 'static'

# Define the FINAL output folder
# This folder will contain our complete website
OUTPUT_FOLDER = 'dist' 

def setup_environment():
    """Initializes Jinja2 environment and creates a clean output folder."""
    print(f"Setting up template environment from: {TEMPLATE_FOLDER}")
    # Load templates from the 'templates' folder
    file_loader = FileSystemLoader(TEMPLATE_FOLDER)
    env = Environment(loader=file_loader)
    
    # Clean up the old 'dist' folder if it exists
    if os.path.exists(OUTPUT_FOLDER):
        print(f"Removing old output directory: {OUTPUT_FOLDER}")
        shutil.rmtree(OUTPUT_FOLDER)
        
    # Create a new, empty 'dist' folder
    print(f"Creating new output directory: {OUTPUT_FOLDER}")
    os.makedirs(OUTPUT_FOLDER)
    
    return env

def load_data():
    """Loads heroes data from the local JSON file."""
    print(f"Loading data from: {DATA_FILE}")
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print("Data loaded successfully.")
        return data
    except Exception as e:
        print(f"Error loading data file: {e}")
        exit(1) # Stop the build if data is missing

def render_pages(env, heroes_data):
    """Renders all HTML pages into the 'dist' folder."""
    
    # --- 1. Render index.html ---
    print("Rendering index.html...")
    template_index = env.get_template('index.html')
    # This page doesn't need any dynamic data
    output_index = template_index.render()
    
    # Save the rendered HTML to the 'dist' folder
    with open(os.path.join(OUTPUT_FOLDER, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(output_index)
    print("Saved dist/index.html")

    # --- 2. Render showEntries.html (from db.html) ---
    print("Rendering showEntries.html (from db.html)...")
    template_db = env.get_template('db.html')
    
    # Inject the 'heroes_data' into the template
    output_db = template_db.render(heroes=heroes_data)
    
    # Save the rendered HTML
    with open(os.path.join(OUTPUT_FOLDER, 'showEntries.html'), 'w', encoding='utf-8') as f:
        f.write(output_db)
    print("Saved dist/showEntries.html")

def copy_static_files():
    """Copies all static assets (images) to the 'dist' folder."""
    print(f"Copying static files from {STATIC_FOLDER} to {OUTPUT_FOLDER}...")
    
    # Copy all files from 'static' (e.g., avengers.gif)
    # directly into 'dist'
    for item in os.listdir(STATIC_FOLDER):
        source_path = os.path.join(STATIC_FOLDER, item)
        destination_path = os.path.join(OUTPUT_FOLDER, item)
        if os.path.isfile(source_path):
            shutil.copy2(source_path, destination_path)
    print("Static files copied.")

def main():
    """Main function to run the entire build process."""
    env = setup_environment()
    heroes_data = load_data()
    render_pages(env, heroes_data)
    copy_static_files() # <-- Don't forget to copy images!
    
    print("\nBuild complete!")
    print(f"Your static site is ready in the '{OUTPUT_FOLDER}' folder.")

if __name__ == "__main__":
    main()