# Program to Upload Color Image and convert into Black & White image
import os
from flask import  Flask, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
import cv2
import numpy as np

app = Flask(__name__)

# Open and redirect to default upload webpage
@app.route('/')
def load_form():
    return render_template('upload.html')


# Function to upload image and redirect to new webpage
@app.route('/gray', methods=['POST'])
def upload_image():
    choice = request.form['operation_type']
    file = request.files['file']
    filename = secure_filename(file.filename)
    
    img_array = np.fromstring(file.read(),dtype="uint8")
    decoded_array = cv2.imdecode(img_array,cv2.IMREAD_UNCHANGED)

    if choice == "grey":
        file_data = make_grayscale(decoded_array)
    elif choice == "sketch":
        file_data =make_sketch(decoded_array)
    elif choice == "oil":
        file_data = make_oil(decoded_array)    
    elif choice == "rgb":
        file_data = make_rgb(decoded_array)    
    elif choice == "invert":
        file_data = invert(decoded_array)  
    elif choice == "water":
        file_data = make_water(decoded_array)
    elif choice == "HDR":
        file_data = HDR(decoded_array)          
    else:
        print("No image selected")        
    with open(os.path.join('static/', filename),
              'wb') as f:
        f.write(file_data)

    display_message = 'Image successfully uploaded and displayed below'
    return render_template('upload.html', filename=filename, message = display_message)



def make_grayscale(decoded_image):
    # Make grayscale
    converted_gray_img = cv2.cvtColor(decoded_image, cv2.COLOR_RGB2GRAY)
    status, output_image = cv2.imencode('.PNG', converted_gray_img)
    return output_image

def make_sketch(decoded_image):
    grey_img = cv2.cvtColor(decoded_image,cv2.COLOR_BGR2GRAY)
    sharp_img = cv2.bitwise_not(grey_img)
    blur_img = cv2.GaussianBlur(sharp_img,(111,111),0)
    sharpened_blur_img = cv2.bitwise_not(blur_img)
    sketch_img = cv2.divide(grey_img,sharpened_blur_img,scale=256.0)
    status,final_img = cv2.imencode('.PNG',sketch_img)

    return final_img

def make_oil(converted_img):
    oil_img = cv2.xphoto.oilPainting(converted_img,7,1)
    status,final_img = cv2.imencode(".PNG",oil_img)

    return final_img

def make_rgb(converted_img):
    rgb_img = cv2.cvtColor(converted_img,cv2.COLOR_BGR2RGB)
    status,output_img = cv2.imencode(".PNG",rgb_img)

    return output_img

def invert(input_img):
    inverted_img = cv2.bitwise_not(input_img)
    status, result = cv2.imencode(".PNG",inverted_img)
    
    return result

def make_water(input_img):
    water_img = cv2.stylization(input_img, sigma_s=60, sigma_r=0.6)
    status, result = cv2.imencode(".PNG",water_img)

    return result

def HDR(input_img):
    HDR_img = cv2.detailEnhance(input_img, sigma_s=12, sigma_r=0.15)
    status,result = cv2.imencode(".PNG",HDR_img)

    return result

@app.route('/display/<filename>')
def display_image(filename):
    return redirect(url_for('static', filename=filename))



if __name__ == "__main__":
    app.run()


