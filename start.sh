#!/usr/bin/env bash

# Set conda env
conda activate base

# Train RASA NLU
python -m rasa_nlu.train -c config.yml --data data/nlu.md -o models --fixed_model_name nlu --project rasa-telegram-app

# Train RASA core
python -m rasa_core.train -d domain.yml -s data/stories.md -o models/rasa-telegram-app/core

# Start action server
python -m rasa_core_sdk.endpoint --actions actions

# Run bot
python -m rasa_core.run -d models/current/dialogue -u models/current/nlu --endpoints endpoints.yml
