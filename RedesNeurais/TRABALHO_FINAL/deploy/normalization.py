
# Imports
import os
import pathlib
import numpy as np
from sklearn.discriminant_analysis import StandardScaler
from sklearn.preprocessing import OneHotEncoder, QuantileTransformer
from tensorflow.keras.models import model_from_json
import pandas as pd

# Carrega os arquivos do modelo
def normalization_(features, data): 
	this_folder = pathlib.Path.cwd()
	data_folder = this_folder/"RedesNeurais"/"TRABALHO_FINAL"/"deploy"
	df = pd.read_csv(data_folder/'original_data.csv', sep=',', decimal='.')
	df = df[features]
	recrutamento = [[1,2,3]]
	ohe = OneHotEncoder(categories=recrutamento,handle_unknown='ignore')
	ohe_df = pd.DataFrame(ohe.fit_transform(df[['RecruitmentStrategy']]).toarray(), columns=['RecruitmentStrategy_1','RecruitmentStrategy_2','RecruitmentStrategy_3'])
	df = df.join(ohe_df)
	df = df.drop(['RecruitmentStrategy'], axis=1)

	X = df.to_numpy() 
	STANDARD_SCALER = StandardScaler()
	qt = QuantileTransformer(output_distribution='normal')
	teste_quantile = qt.fit_transform(X)

	STANDARD_SCALER.fit(teste_quantile)
	novo_registro_transformado = STANDARD_SCALER.transform(qt.transform(data))

	return novo_registro_transformado