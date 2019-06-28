# rasa-telegram
Integrates a RASA bot with the Telegram API.

## Requirements
**Python 3.7** and **pip3** should be installed in your system. Also, **Ngrok** should be installed and accessible 
through the ```ngrok``` command.

## Installation
To install ```rasa-x```, ```rasa_nlu```, and ```rasa_core```, run:

```
pip3 install rasa-x --extra-index-url https://pypi.rasa.com/simple
pip3 install rasa[spacy]
pip3 install rasa_core
python3.7 -m spacy download en_core_web_md
python3.7 -m spacy link en_core_web_md en --force
```

To install ```flask```, run:

```
pip3 install flask
```

## Running
To train ```RASA NLU``` and ```RASA core```, run:

```
python3.7 -m rasa_nlu.train -c config.yml --data data/nlu.md -o models --fixed_model_name nlu --project rasa-telegram-app --verbose
python3.7 -m rasa_core.train -d domain.yml -s data/stories.md -o models/rasa-telegram-app/core
```

Start the action server:
```
python3.7 -m rasa_core_sdk.endpoint --actions actions
```

Start the Telegram bot:
```
python3.7 main.py --token <TOKEN>
```
