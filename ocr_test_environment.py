
import os
import cv2
import numpy as np
import pandas as pd
import pytesseract

# Classe abstraite pour les algorithmes de reconnaissance de caractères
class OCRAlgorithm:
    def recognize(self, image):
        raise NotImplementedError("Subclasses should implement this method")

# Exemple d'implémentation d'un algorithme utilisant Tesseract
class TesseractOCR(OCRAlgorithm):
    def recognize(self, image):
        return pytesseract.image_to_string(image)

# Fonction pour charger les images de chèques
def load_images(image_folder):
    images = []
    for filename in os.listdir(image_folder):
        if filename.endswith('.jpg') or filename.endswith('.png'):
            img = cv2.imread(os.path.join(image_folder, filename), cv2.IMREAD_GRAYSCALE)
            if img is not None:
                images.append((filename, img))
    return images

# Fonction pour charger les données de validation
def load_validation_data(validation_file):
    return pd.read_csv(validation_file)

# Fonction pour tester un algorithme
def test_algorithm(algorithm, images, validation_data):
    results = []
    for filename, image in images:
        recognized_text = algorithm.recognize(image)
        expected_text = validation_data[validation_data['filename'] == filename]['expected_text'].values[0]
        results.append((filename, recognized_text, expected_text))
    return results

# Fonction pour évaluer les résultats
def evaluate_results(results):
    correct = 0
    for filename, recognized_text, expected_text in results:
        if recognized_text.strip() == expected_text.strip():
            correct += 1
    accuracy = correct / len(results)
    return accuracy

# Chemins vers les dossiers et fichiers
image_folder = 'path/to/image/folder'
validation_file = 'path/to/validation/file.csv'

# Chargement des images et des données de validation
images = load_images(image_folder)
validation_data = load_validation_data(validation_file)

# Test des algorithmes
algorithms = [TesseractOCR()]  # Vous pouvez ajouter d'autres algorithmes ici
for algorithm in algorithms:
    results = test_algorithm(algorithm, images, validation_data)
    accuracy = evaluate_results(results)
    print(f'Accuracy for {algorithm.__class__.__name__}: {accuracy:.2f}')
