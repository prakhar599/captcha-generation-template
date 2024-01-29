from PIL import Image, ImageDraw, ImageFont
import random
import string
from flask import Flask, send_file

app = Flask(__name__)

# Generate a random string for the CAPTCHA
def generate_captcha_text():
    captcha_length = 6
    captcha_characters = string.ascii_letters + string.digits
    captcha_text = ''.join(random.choice(captcha_characters) for _ in range(captcha_length))
    return captcha_text

# Create a CAPTCHA image
def create_captcha_image(text):
    image_width = 200
    image_height = 80
    image = Image.new('RGB', (image_width, image_height), color='white')
    draw = ImageDraw.Draw(image)
    
    # Use a truetype font file (you can replace it with your own font file)
    font = ImageFont.load_default()
    
    # Add text to the image
    draw.text((10, 20), text, fill='black', font=font)
    
    # Add some random noise to make it harder for OCR
    for _ in range(200):
        x = random.randint(0, image_width - 1)
        y = random.randint(0, image_height - 1)
        draw.point((x, y), fill='black')

    return image

# Route to generate and serve CAPTCHA image
@app.route('/captcha')
def captcha():
    captcha_text = generate_captcha_text()
    image = create_captcha_image(captcha_text)
    
    # Save the image temporarily (you can improve this by saving to a database)
    image_path = 'temp_captcha.png'
    image.save(image_path)

    # Send the image file in the response
    return send_file(image_path, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)
