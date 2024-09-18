
# Imports
import os
import pathlib
import numpy as np
from tensorflow.keras.models import model_from_json

# Carrega os arquivos do modelo
def model_(): 
	this_folder = pathlib.Path.cwd()
	data_folder = this_folder/"RedesNeurais"/"TRABALHO_FINAL"/"deploy"
	json_file = open(data_folder/"model"/"model.json", 'r')
	loaded_model_json = json_file.read()
	json_file.close()
	loaded_model = model_from_json(loaded_model_json)
	loaded_model.load_weights(data_folder/"model"/"weights.h5")

	# Compila e Avalia o Modelo Carregado
	loaded_model.compile(loss='mse', optimizer='adam', metrics=['accuracy'])

	return loaded_model