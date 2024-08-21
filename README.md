# Robotin


python version: [3.12.3](https://www.python.org/downloads/release/python-3123/)
install [Torch](https://pytorch.org/get-started/locally/): pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu124


## Setup

### Create env
```
py -m venv .env
.\.env\Scripts\activate
py -m pip install --upgrade pip
py -m pip install -r .\requirements.txt
```

### Run

```
.\.env\Scripts\activate
py main.py
```

### Run server
```
fastapi dev server.py
```


## Commands

button_1: normal face
button_2: text box
button_3: show image

space: toggle speaking

button_d: start face reckoning
button_s: stop face reckoning

button_l: start listening





