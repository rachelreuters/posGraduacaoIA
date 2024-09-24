import pathlib
import joblib

def normalization_(data): 
	this_folder = pathlib.Path.cwd()
	data_folder = this_folder/"RedesNeurais"/"TRABALHO_FINAL"/"deploy"
	
	STANDARD_SCALER = joblib.load(data_folder/'std_scaler.pkl')
	QT_SCALER = joblib.load(data_folder/'qt_scaler.pkl')

	novo_registro_transformado = STANDARD_SCALER.transform(QT_SCALER.transform(data))

	
	return novo_registro_transformado
