from flask import Flask, request, jsonify
import numpy as np
import json
import os

from sklearn.discriminant_analysis import StandardScaler
from normalization import normalization_
from deploy_model import model_
import pandas as pd
from sklearn.preprocessing import OneHotEncoder, QuantileTransformer
from flask_cors import CORS
import pandas as pd

app = Flask(__name__)
CORS(app)

model = model_()


# Endpoint de teste
@app.route('/')
def index():
	return "API para dar apoio as decisoes de contratacao de RH", 200

#Endpoint para predição
@app.route('/predict', methods=['POST'])
def predict():
	data_input = request.get_json()
	
	df_input = pd.read_json(json.dumps(data_input))

	features = ['EducationLevel','ExperienceYears','InterviewScore',
				'SkillScore','PersonalityScore','RecruitmentStrategy']
	

	recrutamento = [[1,2,3]]


	filtrado = df_input[features]

	ohe = OneHotEncoder(categories=recrutamento,handle_unknown='ignore')
	ohe_df = pd.DataFrame(ohe.fit_transform(filtrado[['RecruitmentStrategy']]).toarray(), columns=['RecruitmentStrategy_1','RecruitmentStrategy_2','RecruitmentStrategy_3'])
	df = filtrado.join(ohe_df)
	filtrado = df.drop(['RecruitmentStrategy'], axis=1)

	input_final_np = filtrado.to_numpy()


	input_final_np = normalization_(features, input_final_np)


	# faz a predicao com o modelo carregado
	out = model.predict(input_final_np)

	# Calcular a porcentagem
	percentage = float(out[0][0]) * 100

	# Determinar a mensagem baseada na porcentagem
	if percentage >= 90:
		message = "O candidato deve ser contratado."
	else:
		message = "O candidato não deve ser contratado."

	# Preparar a resposta
	response = {
		'contratar': percentage >= 90,
		'porcentagem': f"{percentage:.2f}%",
		'mensagem': message
	}

	return jsonify(content=response) , 200


if __name__ == "__main__":
	port = int(os.environ.get('PORT', 5000))
	app.run(host='0.0.0.0', port=port)