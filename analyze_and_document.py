import os
import base64
import openai
import dotenv
import subprocess
import sys

dotenv.load_dotenv()

# Set up your OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

def analyze_screenshot(image_path):
    """Analyzes a single screenshot using OpenAI's Vision API."""
    try:
        print(f"Analyzing {image_path}")
        with open(image_path, "rb") as image_file:
            base64_image = base64.b64encode(image_file.read()).decode("utf-8")
        
        # Determine image format from file extension
        file_ext = os.path.splitext(image_path)[1].lower()
        if file_ext == '.png':
            mime_type = "image/png"
        elif file_ext in ['.jpg', '.jpeg']:
            mime_type = "image/jpeg"
        else:
            mime_type = "image/jpeg"  # default fallback

        prompt = """
        You are a helpful assistant that documents web applications.
        You are given a screenshot of a web application and you need to describe the content of the screenshot.
        You need to describe the content of the screenshot, including key elements, text, and overall layout.
        Be concise but informative.
        """
        prompt += f"""
        Screenshot: {image_path}
        """
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {"type": "image_url", "image_url": {"url": f"data:{mime_type};base64,{base64_image}"}},
                    ],
                }
            ],
            max_tokens=500
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error analyzing {image_path}: {e}"

def get_screenshot_descriptions(screenshot_folder="screenshots"):
    """Crawls a folder of screenshots and returns a list of descriptions."""
    print(f"Getting screenshot descriptions from {screenshot_folder}")
    descriptions = {}
    
    # Check if screenshots folder exists
    if not os.path.exists(screenshot_folder):
        print(f"Error: Screenshots folder '{screenshot_folder}' does not exist!")
        return descriptions
    
    # Check if folder is empty
    files = os.listdir(screenshot_folder)
    if not files:
        print(f"Warning: Screenshots folder '{screenshot_folder}' is empty!")
        return descriptions
    
    for filename in files:
        if filename.endswith(('.png', '.jpg', '.jpeg')):
            image_path = os.path.join(screenshot_folder, filename)
            description = analyze_screenshot(image_path)
            descriptions[filename] = description
            print(f"Analyzed {filename}")
        else:
            print(f"Skipping {filename} (not an image file)")
    
    if not descriptions:
        print("No image files found in the screenshots folder!")
    
    return descriptions

def create_markdown_report(descriptions, output_dir="chapters"):
    """Creates separate Markdown files for each screenshot and description."""
    print(f"Creating markdown report in {output_dir}")
    # Create chapters directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created directory: {output_dir}")
    
    # delete all files in the output directory
    for file in os.listdir(output_dir):
        os.remove(os.path.join(output_dir, file))
    
    # Create individual markdown files for each screenshot
    for filename, description in descriptions.items():
        # Create a clean filename for the markdown file
        base_name = os.path.splitext(filename)[0]  # Remove .png extension
        chapter_file = os.path.join(output_dir, f"{base_name.title()}.md")
        
        with open(chapter_file, "w") as f:
            # Create a descriptive title based on the filename
            # title = base_name.replace('_', ' ').replace('-', ' ').title()
            # f.write(f"# {title}\n\n")
            f.write(f"![Screenshot of {filename}](screenshots/{filename})\n\n")
            f.write(f"## Description\n\n{description}\n\n")
        
        print(f"Created chapter: {chapter_file}")
    
    print(f"Generated {len(descriptions)} chapter files in {output_dir}/")

def create_pdf_report(chapters_dir="chapters", output_file="user_guide.pdf"):
    """Creates a PDF report from chapter markdown files using the markdown_to_html.py script."""
    print(f"Creating PDF report in {output_file}")
    try:
        # Use the markdown_to_html.py script to convert all chapter files to a single PDF
        result = subprocess.run([
            sys.executable, "markdown_to_html.py", 
            "--single", 
            "--pdf", 
            chapters_dir,  # directory containing the chapter markdown files
            "user_guide.html"  # output HTML file
        ], capture_output=True, text=True, check=True)
        
        # The script creates user_guide.html and user_guide.pdf
        if os.path.exists("user_guide.pdf"):
            # Rename to the desired output filename if different
            if output_file != "user_guide.pdf":
                os.rename("user_guide.pdf", output_file)
            print(f"PDF report generated: {output_file}")
        else:
            print("Error: PDF generation failed - no output file created")
            
    except subprocess.CalledProcessError as e:
        print(f"Error running markdown_to_html.py: {e}")
        print(f"stdout: {e.stdout}")
        print(f"stderr: {e.stderr}")
    except Exception as e:
        print(f"Error creating PDF report: {e}")

if __name__ == "__main__":
    descriptions = get_screenshot_descriptions()
    chapters_dir = "chapters"
    create_markdown_report(descriptions, chapters_dir)
    
    # Create PDF report if chapters were created successfully
    if descriptions:
        create_pdf_report(chapters_dir, "user_guide.pdf")
    else:
        print("No screenshots found, skipping PDF generation.")

    print("Done.")