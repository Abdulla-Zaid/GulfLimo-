# convert_logo.py
import base64

def image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
        return f"data:image/png;base64,{encoded_string}"

# Replace with your actual logo path
logo_path = "main_app/static/images/background.png"
output_file = "main_app/static/images/background_base64.txt"  # Name of the output text file

try:
    logo_base64 = image_to_base64(logo_path)
    
    # Save to text file
    with open(output_file, "w") as file:
        file.write(logo_base64)
    
    print(f"Base64 string has been saved to {output_file}")
    
except FileNotFoundError:
    print("Logo file not found. Please check the path.")
except Exception as e:
    print(f"An error occurred: {e}")