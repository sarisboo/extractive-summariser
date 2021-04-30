# Template Nounoursita 🧸

## Setup

```sh
# Clone this repository
$ git clone https://github.com/sarisboo/boilerplate.git <new_project> && cd <new_project>

# Recreate the git repository
$ rm -rf .git
$ git init

# Install dependencies
$ bin/dev poetry install
```

## Develop

### Add a new dependency

```sh
$ bin/dev poetry add nltk
```

### Run a script

To run a script, press `alt-t`.

Alternatively, you can run a script in the shell like this:
```sh
$ bin/dev poetry run python <script>
```

## Recipes

### Run Jupyter

```sh
# Install Jupyter
$ poetry add jupyter ipykernel

# Access Jupyter
$ bin/jupyter
```