import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io
import base64

def create_banner(text="Fresh Fruits Market", width=800, height=200, bg_color=(255, 102, 0), text_color=(255, 255, 255)):
    """
    Create a banner image with text for the fruit store
    
    Args:
        text: Text to display on the banner
        width: Width of the banner
        height: Height of the banner
        bg_color: Background color as RGB tuple
        text_color: Text color as RGB tuple
        
    Returns:
        HTML img tag with the banner image
    """
    # Create a new image with the given background color
    image = Image.new('RGB', (width, height), color=bg_color)
    draw = ImageDraw.Draw(image)
    
    # Try to use a nice font, fall back to default if not available
    try:
        font = ImageFont.truetype("arial.ttf", 60)
    except IOError:
        font = ImageFont.load_default()
    
    # Calculate text position to center it
    text_width, text_height = draw.textsize(text, font=font)
    position = ((width - text_width) // 2, (height - text_height) // 2)
    
    # Draw the text
    draw.text(position, text, font=font, fill=text_color)
    
    # Add some fruit icons
    fruits = ["🍎", "🍌", "🍊", "🍓", "🥭", "🍍", "🍇", "🍉"]
    icon_size = 30
    for i, fruit in enumerate(fruits):
        x = (width // (len(fruits) + 1)) * (i + 1)
        y = height - 50
        draw.text((x, y), fruit, font=ImageFont.truetype("arial.ttf", icon_size) if 'font' in locals() else ImageFont.load_default())
    
    # Convert the image to base64 for HTML embedding
    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    img_str = base64.b64encode(buffer.getvalue()).decode()
    
    # Return HTML for the image
    return f'<img src="data:image/png;base64,{img_str}" alt="{text}" width="{width}" height="{height}">'

def display_banner(text="Fresh Fruits Market", width=800, height=200):
    """
    Display the banner in a Streamlit app
    """
    banner_html = create_banner(text, width, height)
    st.markdown(banner_html, unsafe_allow_html=True)

# Example usage:
# display_banner("Welcome to Fresh Fruits Market")