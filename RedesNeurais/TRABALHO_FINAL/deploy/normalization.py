
# Imports
import os
import pathlib
import numpy as np
from sklearn.discriminant_analysis import StandardScaler
from sklearn.preprocessing import OneHotEncoder, QuantileTransformer
from tensorflow.keras.models import model_from_json
import pandas as pd
import joblib

# Carrega os arquivos do modelo
def normalization_(features, data): 
	this_folder = pathlib.Path.cwd()
	data_folder = this_folder/"RedesNeurais"/"TRABALHO_FINAL"/"deploy"
	
	STANDARD_SCALER = joblib.load(data_folder/'std_scaler.pkl')
	QT_SCALER = joblib.load(data_folder/'qt_scaler.pkl')

	novo_registro_transformado = STANDARD_SCALER.transform(QT_SCALER.transform(data))

	
	return novo_registro_transformado

features = ['EducationLevel','ExperienceYears','InterviewScore',
			'SkillScore','PersonalityScore','RecruitmentStrategy']
normalization_(features, [[2, 4, 33, 44, 55, 1, 0 ,0]])