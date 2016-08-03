## Installation

```bash
git clone git@github.com:openhealthcare/elcid-deployment.git
cd elcid-deployment
mkvirtualenv elcid-setup -a $PWD
pip install -r requirements.txt
```

## Server Setup

1. run ./initial_bootstrap.sh
2. workon elcid-setup
3. go into env_setup and change the environment variables according to your preferences
4. fab server_setup:{{ project_name e.g. elcid }},{{ version_branch e.g. v0.6.0 }}

You should be up and running!

## Deployment

1. workon elcid-setup
2. double check all the env variables in env_setup are what you think they are
3. fab deploy:{{ project_name e.g. elcid }},{{ version_branch e.g. v0.6.0 }}
4. fab restart_everything:{{ project_name e.g. elcid }},{{ version_branch e.g. v0.6.0 }}
