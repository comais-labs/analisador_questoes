from ultralytics import YOLO
from PIL import Image
import pytesseract
import json
import re
import glob

# Load model
model =  YOLO('runs/detect/train6/weights/best.pt')

# load image
dir_imgs = 'data/imgs/imgs_pages/*.png'

text_questions = []

for img_path in glob.glob(dir_imgs):
    img = Image.open(img_path)
    # Extração de texto com configuração personalizada

    results = model(img) 
   
    # get Bounding box, somente questões
    bb_questions = []
    for result in results:
        for box in result.boxes:
            if box.cls == 0:
                category = box.cls
                bounding_box = box.xyxy.tolist()
                bb_questions.append(bounding_box[0])
                print(f"Category: {category}, Bounding Box: {bounding_box}")
    #gerar imagen de cada bounding box
    
    for i, box in enumerate(bb_questions):
        img_question = img.crop(box)
        text = pytesseract.image_to_string(img_question, lang='por', config='--oem 3 --psm 6 ')
        text_questions.append(text)
    #dump questions to json
    #limpar texto

text_questions = [text.replace('\n', ' ') for text in text_questions ]
# remove multiple spaces
text_questions = [re.sub(' +', ' ', text) for text in text_questions]
# remove leading and trailing spaces
text_questions = [text.strip().lower() for text in text_questions if text != '']

with open('questions.json', 'w', encoding='utf-8') as f:
        json.dump(text_questions, f, indent=3, )

#cli
#yolo train data=yolo.yaml