# Data analysis
- Document here the project: music_similarity
- Description: Project aimed to find similarity between songs
- Data Source: Spotify API
- Type of analysis: K-NN Recommender

# Startup the project

The initial setup.

Create virtualenv and install the project:
```bash
sudo apt-get install virtualenv python-pip python-dev
deactivate; virtualenv ~/venv ; source ~/venv/bin/activate ;\
    pip install pip -U; pip install -r requirements.txt
```

Unittest test:
```bash
make clean install test
```

Check for music_similarity in gitlab.com/{group}.
If your project is not set please add it:

- Create a new project on `gitlab.com/{group}/music_similarity`
- Then populate it:

```bash
##   e.g. if group is "{group}" and project_name is "music_similarity"
git remote add origin git@github.com:{group}/music_similarity.git
git push -u origin master
git push -u origin --tags
```

Functionnal test with a script:

```bash
cd
mkdir tmp
cd tmp
music_similarity-run
```

# Install

Go to `https://github.com/{group}/music_similarity` to see the project, manage issues,
setup you ssh public key, ...

Create a python3 virtualenv and activate it:

```bash
sudo apt-get install virtualenv python-pip python-dev
deactivate; virtualenv -ppython3 ~/venv ; source ~/venv/bin/activate
```

Clone the project and install it:

```bash
git clone git@github.com:{group}/music_similarity.git
cd music_similarity
pip install -r requirements.txt
make clean install test                # install and test
```
Functionnal test with a script:

```bash
cd
mkdir tmp
cd tmp
music_similarity-run
```
