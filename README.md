# How to Use

## Installation

### Mac

You should be able to just copy and paste this whole thing into the terminal and it will finish by opening the .env file for you to put your OpenAI key in.

```shell
# Install Homebrew
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install python3
brew install python3

# Clone this repo and cd into it
git clone https://github.com/ejenk0/transcribe.git ~
cd ~/transcribe

# Setup python virtual environment for this project
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy the example env
cp .env.example .env

# Edit the .env file to add your OpenAI key
open .env
```

## Usage

Place the audio file(s) you want to transcribe in the `audio` directory. Then run the script:

```shell
# cd into the project directory
cd ~/transcribe

# Run the script
./transcribe.py
```
