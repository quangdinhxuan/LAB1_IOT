from keras.models import load_model  # TensorFlow is required for Keras to work
import cv2  # Install opencv-python
import numpy as np

# Disable scientific notation for clarity
np.set_printoptions(suppress=True)

# Load the model
model = load_model("keras_Model.h5", compile=False)

# Load the labels
# class_names = open("labels.txt", "r").readlines()

class_names = ["Không khẩu trang", "Có khẩu trang", "Không có người"]

# CAMERA can be 0 or 1 based on default camera of your computer
camera = cv2.VideoCapture(0)
# video_capture = cv2.VideoCapture(0)
#
# cv2.namedWindow("Window")
#
# while True:
#     ret, frame = video_capture.read()
#     cv2.imshow("Window", frame)
#
#     #This breaks on 'q' key
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break
#
# video_capture.release()
# cv2.destroyAllWindows()


def image_detector():
    # Grab the webcamera's image.
    ret, image = camera.read()

    # Resize the raw image into (224-height,224-width) pixels
    image = cv2.resize(image, (224, 224), interpolation=cv2.INTER_AREA)

    # Show the image in a window
    cv2.imshow("Webcam Image", image)
    cv2.waitKey(5)

    # Make the image a numpy array and reshape it to the models input shape.
    image = np.asarray(image, dtype=np.float32).reshape(1, 224, 224, 3)

    # Normalize the image array
    image = (image / 127.5) - 1

    # Predicts the model
    prediction = model.predict(image)
    index = np.argmax(prediction)
    class_name = class_names[index]
    confidence_score = prediction[0][index]

    # Print prediction and confidence score
    print(class_name)
    print("Confidence Score:", str(np.round(confidence_score * 100))[:-2], "%")
    return class_name
