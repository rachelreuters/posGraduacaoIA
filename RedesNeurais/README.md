
# Redes Neurais

Todos os estudos e projetos da disciplina de Redes Neurais

Instalar o Python 3.12

python -m venv venv
venv/Scripts/activate
pip install -r requirements.txt



para utilizar GPU e conda
- instalar CONDA

conda create --name tf python=3.7
conda activate tf

conda install -c conda-forge cudatoolkit=11.2 cudnn=8.1.0
pip install --upgrade pip
pip install "tensorflow<2.11" --user
