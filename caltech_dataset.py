from torchvision.datasets import VisionDataset

from PIL import Image

import os
import os.path
import sys
import pandas as pd


def pil_loader(path):
    # open path as file to avoid ResourceWarning (https://github.com/python-pillow/Pillow/issues/835)
    with open(path, 'rb') as f:
        img = Image.open(f)
        return img.convert('RGB')


class Caltech(VisionDataset):
    def __init__(self, root, split='train', transform=None, target_transform=None):
        super(Caltech, self).__init__(root,transform=transform, target_transform=target_transform)

        self.split = split # This defines the split you are going to use
                           # (split files are called 'train.txt' and 'test.txt')
        self.images  = pd.DataFrame(columns = ['img'])
        self.labelNames=[]
            
        splitted_dir=root.split('/')
        parent = splitted_dir[0]
        folder_data = splitted_dir[1]
        
        my_file = open(parent + '/' + split + '.txt', "r")
        content_list = my_file.readlines()
        
        for img in content_list:
            label = img.split('/')[0]
            if label != 'BACKGROUND_Google':
                x = pil_loader(parent + '/' + folder_data + '/' + img.split('\n')[0])
                self.images.loc[len(self.images)]=[x]
                self.labelNames.append(label)

        #'''
        #- Here you should implement the logic for reading the splits files and accessing elements
        #- If the RAM size allows it, it is faster to store all data in memory
        #- PyTorch Dataset classes use indexes to read elements
        #- You should provide a way for the __getitem__ method to access the image-label pair
        #  through the index
        #- Labels should start from 0, so for Caltech you will have lables 0...100 (excluding the background class) 
        #'''

    def __getitem__(self, index):
        '''
        __getitem__ should access an element through its index
        Args:
            index (int): Index

        Returns:
            tuple: (sample, target) where target is class_index of the target class.
        '''

        image =  self.images.iloc[index,0]
        label = self.images.iloc[index,1]
        # Provide a way to access image and label via index
                           # Image should be a PIL Image
                           # label can be int

        # Applies preprocessing when accessing the image
        if self.transform is not None:
            image = self.transform(image)

        return image, label

    def setIntLabel(self,labelList):
        self.images['labelInt'] = labelList
        self.images['labelName'] = self.labelNames
        
    def __len__(self):
        '''
        The __len__ method returns the length of the dataset
        It is mandatory, as this is used by several other components
        '''
        length = len(self.images) # Provide a way to get the length (number of elements) of the dataset
        return length
    
    def augmentation(self,transform):

        augmented_img = pd.DataFrame(columns=['img','labelInt'])
        for img in self.images['img']:
            print(transform(img))
    def checkType(self):
        self.images['img'].apply(lambda x: print(type))