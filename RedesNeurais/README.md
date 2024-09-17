
# Redes Neurais

Todos os estudos e projetos da disciplina de Redes Neurais

Instalar o Python 3.12

python -m venv venv
venv/Scripts/activate
pip install -r requirements.txt


Conda Commands

conda create --name py37 python=3.7    
conda activate py37                                          
conda env list 


para utilizar GPU e conda
- instalar CONDA

conda create --name tf python=3.7
conda activate tf

conda install -c conda-forge cudatoolkit=11.2 cudnn=8.1.0
pip install --upgrade pip
pip install "tensorflow<2.11" --user

#para utilizar alguns wrappers:
pip install scikeras  
pip install imblearn 


Endpoint pra teste do modelo de recrutamento de RH

POST http://127.0.0.1:5000/predict 
Input Body model:
[{
    "EducationLevel": 3,
    "ExperienceYears": 14,
    "InterviewScore": 31.70, 
    "SkillScore": 54,
    "PersonalityScore": 50, 
    "RecruitmentStrategy": 1,
    "Age": 55,
    "Gender":1,
    "PreviousCompanies": 3,
    "DistanceFromCompany": 44.33
}]

Output Response:
{
    "contratar": "0.9999032"
}


