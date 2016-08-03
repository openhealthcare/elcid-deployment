## Installation

```bash
git clone git@github.com:openhealthcare/elcid-deployment.git
cd elcid-deployment
mkvirtualenv elcid-setup -a $PWD
pip install -r requirements.txt
cp settings.ini.example settings.in
```

## Server Setup

1. run ./initial_bootstrap.sh
2. workon elcid-setup
3. Edit the variables in `settings.ini as required.
4. fab server_setup

You should be up and running!

## Deployment

1. workon elcid-setup
2. Edit the variables in `settings.ini as required.
3. fab deploy
4. fab restart_everything
