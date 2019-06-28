# rasa-telegram
Integrates a RASA bot with the Telegram API. 

## Requirements
You must create a Telegram bot through **BotFather**. After creating a bot, you will be provided of its **API key**. This key will be later used in the `main.py` script.

**Python 3.7** and **pip3** should be installed in your system. Also, **Ngrok** should be installed and accessible through the `ngrok` command.

## Installation
To install `rasa-x`, `rasa` with `spacy`, and `rasa_core`, run:

```
pip3 install rasa-x --extra-index-url https://pypi.rasa.com/simple
pip3 install rasa[spacy]
pip3 install rasa_core
python3.7 -m spacy download en_core_web_md
python3.7 -m spacy link en_core_web_md en --force
```

To install `flask`, run:

```
pip3 install flask
```

## Running
**1 -**  Train `RASA NLU` and `RASA core` by running:

```
python3.7 -m rasa_nlu.train -c config.yml --data data/nlu.md -o models --fixed_model_name nlu --project rasa-telegram-app --verbose
python3.7 -m rasa_core.train -d domain.yml -s data/stories.md -o models/rasa-telegram-app/core
```

**2 -** Start a `ngrok` service on port 5000 and copy the **HTTPs** forwarding link (ex.: https://xxxxxxxx.ngrok.io):

```
ngrok http 5000
```

**3 -** In a new terminal, start the action server:

```
python3.7 -m rasa_core_sdk.endpoint --actions actions
```

**4 -** In another terminal, start the Telegram bot:

```
python3.7 main.py --token <TOKEN> --tunnel <TUNNEL>
```

where \<TOKEN> should be replaced by the **API key** provided by BotFather and \<TUNNEL> should be replaced by the link you copied from the `ngrok` command.
