# Projet 10 - Déploiement sur VPS détaillé:

# Préparation

Tout d'abord, je génère une paire de clés SSH : `ssh-keygen -t ed25519`  
Elle sera nommée `ocp10_ed25519`  
Je commande aussi un VPS chez Scaleway avec Ubuntu 20.04

Je vais tout d'abord mettre à jour le système
```
sudo apt update && sudo apt upgrade -y
```

## Configuration SSH

Scaleway ne permet la connexion que par clé SSH, et désactive par défaut la connexion par mot de passe.  
C'est pas mal mais je préfère quand même créer un utilisateur et lui attribuer ma clé SSH.
```
adduser seb
adduser seb sudo
su seb
mkdir ~/.ssh
chmod 700 ~/.ssh
touch ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys
```

Il ne reste plus qu'à copier ma clé SSH publique dans `~/.ssh/authorized_keys` et vérifier la configuration de sshd.  
J'en profite pour modifier certains éléments :
```
Port 5843
PermitRootLogin no
PubkeyAuthentication yes
PasswordAuthentication no
```

Je peux enfin redémarrer sshd `sudo systemctl restart sshd`  
Je n'ai plus qu'à ajuster la configuration de mon client SSH
```
Host purbeurre
  HostName 12.34.56.789
  Port 5843
  User seb
  IdentityFile ~/.ssh/ocp10_ed25519
```

je peux désormais me connecter simplement avec la commande `ssh purbeurre`  
A partir de maintenant, tout se fera depuis l'utilisateur `seb`

## Configuration du firewall

J'installe et configure le firewall de la manière suivante:
```
sudo apt install ufw
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow 5843
sudo ufw allow 80
sudo ufw allow 443
sudo ufw enable
```

## Installation de Python 3.9

Le projet nécessite Python 3.9, mais celui-ci n'est pas disponible dans les dépots de Ubuntu 20.04, je choisis donc de l'installer depuis les PPA
```
sudo apt install software-properties-common
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
sudo apt install python3.9
```

Je passe ensuite Python 3.9 en version à utiliser par défaut
```
sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.8 1
sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.9 2
```

# Déploiement

J'installe postgres, nginx, certbot et d'autres dépendances, et je met à jour pip:
```
sudo apt install \
	python3-pip python3.9-dev python3.9-venv \
	libssl-dev libffi-dev python3-setuptools \
	libpq-dev postgresql postgresql-contrib \
	build-essential nginx certbot git supervisor
pip3 install --upgrade pip
```

Je créée la base de données:
```
sudo -u postgres psql

CREATE DATABASE purbeurre;
CREATE USER purbeurre_admin WITH PASSWORD 'PASSWORD_HERE';
ALTER ROLE purbeurre_admin SET client_encoding TO 'utf8';
ALTER ROLE purbeurre_admin SET default_transaction_isolation TO 'read committed';
ALTER ROLE purbeurre_admin SET timezone TO 'Europe/Paris';
GRANT ALL PRIVILEGES ON DATABASE purbeurre TO purbeurre_admin;
\q
```

Je clone ensuite le dépôt du projet et fais une copie du fichier `.env.sample`
```
cd ~
git clone https://github.com/sebgoliot/oc_p8-purbeurre
cd oc_p8-purbeurre
cp .env.sample .env
```

Je remplis ensuite le contenu du fichier `.env` copié et procède à l'initialisation du projet
```
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
python3 manage.py migrate
python3 manage.py collectstatic
python3 manage.py import_products 5000
deactivate
```

Je créée un script pour supervisor et new relic : 

```
touch supervisor_run.sh
chmod +x supervisor_run.sh
```
```
#!/bin/

cd ~/oc_p8-purbeurre
source venv/bin/activate
NEW_RELIC_CONFIG_FILE=newrelic.ini newrelic-admin run-program gunicorn purbeurre.wsgi:application -w 4
```

Je configure supervisor : `sudo nano /etc/supervisor/conf.d/purbeurre.conf`
```
[program:purbeurre]
command = /home/seb/oc_p8-purbeurre/supervisor_run.sh
user = seb
directory = /home/seb/oc_p8-purbeurre
stdout_logfile = /var/log/purbeurre/gunicorn_supervisor.log
redirect_stderr = true
autostart = true
autorestart = true
```

Je récupère ma clé d'API RewRelic et génère sa configuration  
Je créée aussi le dossier de logs pour supervisor, le lance et m'assure que tout est ok

```
newrelic-admin generate-config YOUR_API_KEY newrelic.ini
deactivate

sudo mkdir /var/log/purbeurre
sudo systemctl enable supervisor
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl status
```

Je configure NGINX à l'aide de NginxConfig, je passe les détails de sa mise en oeuvre  
Le lien suivant contient la configuration et les commandes utilisées :
[NGINXConfig | DigitalOcean](https://www.digitalocean.com/community/tools/nginx?domains.0.server.domain=purbeurre.sebgoliot.com&domains.0.https.hstsPreload=true&domains.0.https.letsEncryptEmail=contact%40sebgoliot.com&domains.0.php.php=false&domains.0.reverseProxy.reverseProxy=true&domains.0.reverseProxy.proxyPass=http%3A%2F%2F127.0.0.1%3A8000&domains.0.routing.root=false&domains.0.logging.accessLog=true&domains.0.logging.errorLog=true&global.https.ocspCloudflareType=both&global.https.ocspGoogleType=both&global.https.ocspOpenDnsType=both&global.app.lang=fr)

Le domaine a été acheté chez OVH, mais j'utilise Cloudflare pour la gestion des enregistrements DNS:  
Je configure ainsi les enregistrements afin de faire pointer mon domaine sur l'IP du serveur
en ajoutant les enregistrements A et AAAA pour les IP v4 et v6  

Toujours chez Cloudflare, je passe le mode de chiffrement SSL en `Flexible` le temps de l'obtention d'un certificat auprès de letsencrypt
Une fois un certificat obtenu avec Certbot, je repasse le mode de chiffrement en `Strict`

# Monitoring

Le projet a été modifié pour intégrer l'installation de `Sentry`  
Il ne reste plus qu'à préparer l'installation de `NewRelic` 

## Préparation pour NewRelic

Je modifie la configuration de NGINX en ajoutant:
```
# Status monitoring
server {
    listen 127.0.0.1:80;
    server_name 127.0.0.1;

    location /status {
        stub_status;
    }
}
```

Et j'ajoute cette configuration à la base de données:
```
sudo -u postgres psql

CREATE USER new_relic WITH PASSWORD 'PASSWORD_HERE';
GRANT SELECT ON pg_stat_database TO new_relic;
GRANT SELECT ON pg_stat_database_conflicts TO new_relic;
GRANT SELECT ON pg_stat_bgwriter TO new_relic;
\q
```

## Installation de NewRelic

Je repasse temporairement à l'ancienne version de Python (3.8) le temps de l'installation

```
sudo update-alternatives --config python3
```

Je procède à l'installation de NewRelic en suivant l'installation guidée  
Une fois l'installation terminée, je rétablis la version de python3 (3.9)

## Cron
Je créée enfin une tache Cron

```
sudo systemctl enable cron
crontab -e

14 3 * * mon ~/oc_p8-purbeurre/update_products.sh
```

Et le script qui lui est associée

```
touch update_products.sh
chmod +x update_products.sh
```

```
#!/bin/

cd ~/oc_p8-purbeurre
source venv/bin/activate
python3 manage.py import_products 5000
```

# Touches finales

Ajout d'une directive afin d'ignorer les accès au serveur via son IP  
Il faudra aussi supprimer un lien symbolique: `sudo rm /etc/nginx/sites-enabled/default`
```
# Deny access from the server IP
server {
    listen      80 default_server;
    listen      [::]:80 default_server;
    server_name _;
    return 403;
}
```
Et dans le bloc HTTPS:
```
# deny ip access from HTTPS
    if ($host != purbeurre.sebgoliot.com){
        return 403;
    }

```
