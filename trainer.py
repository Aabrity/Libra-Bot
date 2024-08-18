import os
import cv2
import numpy as np
from PIL import Image, ImageEnhance

recognizer = cv2.face.LBPHFaceRecognizer_create()
dataset_path = "admin/dataset"

def augment_image(image):
    """Perform data augmentation on the given image."""
    enhancers = [
        ImageEnhance.Color(image),
        ImageEnhance.Contrast(image),
        ImageEnhance.Brightness(image),
        ImageEnhance.Sharpness(image)
    ]
    
    augmented_images = []
    for enhancer in enhancers:
        for factor in [0.8, 1.0, 1.2]:
            augmented_images.append(enhancer.enhance(factor))
    
    return augmented_images

def get_images_with_id(path):
    image_paths = [os.path.join(path, f) for f in os.listdir(path)]
    faces = []
    ids = []
    
    for image_path in image_paths:
        try:
            face_img = Image.open(image_path).convert("L")
            id = int(os.path.split(image_path)[-1].split(".")[1])
            print(f"ID: {id}")
            augmented_images = augment_image(face_img)
            
            for img in augmented_images:
                face_np = np.array(img, np.uint8)
                faces.append(face_np)
                ids.append(id)
                cv2.imshow("Training", face_np)
                cv2.waitKey(10)
                
        except Exception as e:
            print(f"Error processing {image_path}: {e}")
    
    return np.array(ids), faces

ids, faces = get_images_with_id(dataset_path)
recognizer.train(faces, ids)
recognizer.save("admin/recognizer/trainingdata.yml")
cv2.destroyAllWindows()
