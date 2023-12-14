import os 
import cv2
import pandas as pd 
from deepface import DeepFace 


data={
	'Name':[],
	'Age':[],
	'Gender':[],
	'Race':[]
}

for file in os.listdir('Image-data'):
	result=DeepFace.analyze(cv2.imread(f'Image-data/{file}'),actions=('age','gender','race'))
	data['Name'].append(file.split('.')[0])
	data['Age'].append(result[0]['Age'])
	data['Gender'].append(result[0]['dominant_gender'])
	data['Race'].append(result[0]['dominant_race'])

dataframe=pd.DataFrame(data)
dataframe.to_csv('Face-Analytics')
print(dataframe)