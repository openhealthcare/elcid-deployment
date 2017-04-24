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
4. install the requirements file
5. fab server_setup

You should be up and running!

## Deployment Test
Deployment to Test does not set up the cron job syncing.

Set env.db_dump_dir to load in a database dump

1. workon elcid-setup
2. Edit the variables in `settings.ini as required.
3. fab deploy_test
4. fab restart_everything


# Deployement to Production
Deployment to production sets up a dump directory. It assumes this is the same
directory on a different server. It will load in the most recent database
dump.

1. workon elcid-setup
2. Edit the variables in `settings.ini as required.
3. fab deploy_prod
4. fab restart_everything

# Database Back ups.
You want to do regular database back ups. These will get put in env.db_dump_dir.
On a remote host at env.sync_host. These are set up by default if you do
fab deploy_prod, or you can do it yourself with

```bash
fab setup_cron
```

# Encryption keys

Generate keys:
`openssl req -x509 -nodes -newkey rsa:2048 -keyout private-key.pem -out public-key.pem`

# Decrypting a backup

`openssl smime -decrypt -in encrypted_backyp.dat -binary -inform DEM -inkey private-key.pem -out database.sql`
