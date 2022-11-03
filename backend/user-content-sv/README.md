## User content service

## Initial setup

- Create a virtual env

```bash
python3 -m venv /home/vscode/venvs/mlc-uc-sv
```

- Activate the venv

```bash
source /home/vscode/venvs/mlc-uc-sv/bin/activate
```

- Deactivate the venv

```bash
deactivate
```

- Install required packages

```bash
pip3 install flask-restful 
```

- Freeze the package to `requirements.txt`

```bash
pip3 freeze > requirements.txt
```

- Activate pythone intepretor for vscode

## Make the service available grobally

- run the ngrok command

```bash
/home/vscode/ngrok/ngrok http 5000
```

- install the common packages

```bash
python3 setup.py install
```