# install
conda create --name tf_gpu
activate tf_gpu
conda install tensorflow-gpu
conda install python=3.6.1
pip install rasa_nlu
pip install -r requirements.txt
python -m spacy download it_core_news_sm
npm i rasa-nlu-trainer -g

# training
rasa-nlu-trainer -s training_data.json
python -m rasa_nlu.train -c nlu_config.yml --data training_data.json -o models --fixed_model_name nlu --project current --verbose

# run
python handler.py