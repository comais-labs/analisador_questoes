from ultralytics.data.utils import autosplit
import os
import shutil

dataset_path = 'dataset/augmented/'

dirs =  autosplit(dataset_path, weights=(0.8, 0.2, 0.0))
DIRS = ['train', 'val']
for d in DIRS:
    os.makedirs(os.path.join(dataset_path, d, 'images'), exist_ok=True)
    os.makedirs(os.path.join(dataset_path, d, 'labels'), exist_ok=True)

for d in DIRS:
    with open(f'dataset/autosplit_{d}.txt', 'r') as f:
    # ler todas linhas do arquivo
        lines = f.readlines()
        for line in lines:
            # remover quebra de linha
            line = line.strip()
            # criar o caminho completo para a imagem
            img_path = os.path.join('dataset', line)
            label_path = line.replace('images', 'labels').replace('.png', '.txt')
            label_path = os.path.join('dataset', label_path)
            shutil.copy(img_path, os.path.join(dataset_path, d, 'images'))
            shutil.copy(label_path, os.path.join(dataset_path, d, 'labels'))

           