from keras.models import load_model
import cv2
import numpy as np
import time
import csv

# Disable scientific notation for clarity
np.set_printoptions(suppress=True)

# Load the model
model = load_model("./model/keras_model.h5", compile=False)

# Load the labels
class_names = open("./model/labels.txt", "r").readlines()

# CAMERA can be 0 or 1 based on the default camera of your computer
camera = cv2.VideoCapture(0)

start_time = time.time()
detect_list = []

while True:
    # Grab the web camera's image.
    ret, image = camera.read()

    # Resize the raw image into (224-height,224-width) pixels
    image = cv2.resize(image, (224, 224), interpolation=cv2.INTER_AREA)

    # Show the image in a window
    cv2.imshow("Webcam Image", image)

    # Make the image a numpy array and reshape it to the model's input shape.
    image = np.asarray(image, dtype=np.float32).reshape(1, 224, 224, 3)

    # Normalize the image array
    image = (image / 127.5) - 1

    # Predicts the model
    prediction = model.predict(image)
    index = np.argmax(prediction)
    class_name = class_names[index]
    confidence_score = prediction[0][index]

    # Print prediction and confidence score
    print("Class:", class_name[2:], end="")
    print("Confidence Score:", str(np.round(confidence_score * 100))[:-2], "%")
    
    detect_list.append(class_name[2:])
    
    # Check if 5 seconds have passed
    if time.time() - start_time >= 3:
        most_common_value = max(detect_list, key=detect_list.count)
        
        # Save most_common_value to a CSV file, clearing existing content
        with open('./most_common_values.csv', 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(["Class", "Timestamp"])  # Add header
            csv_writer.writerow([most_common_value, time.strftime("%Y-%m-%d %H:%M:%S")])
            print("Saved to CSV file")
        
        # Clear the detect_list for the next 5 seconds
        detect_list = []
        start_time = time.time()

    # Listen to the keyboard for presses.
    keyboard_input = cv2.waitKey(1)

    # 27 is the ASCII for the esc key on your keyboard.
    if keyboard_input == 27:
        break

camera.release()
cv2.destroyAllWindows()
