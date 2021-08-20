# Tic-Tac-Toe App

Tic-Tac-Toe Game built using [H2O Wave framework](https://wave.h2o.ai)

<img src="./static/play.gif" width="80%" height="80%"/>

## Running this App Locally

### System Requirements 
1. Python 3.6+
2. pip3

### 1. Run the Wave Server
Follow the documentation to [download and run](https://h2oai.github.io/wave/docs/installation) the Wave Server on your local machine.<br>
For macOS run the following command to download and run H2O Wave server.
```shell script
make wave run-wave
```


### 2. Build the python environment
```shell script
make setup
```

### 3. Run the application
```shell script
make run
```

### 4. View the application
Go to http://localhost:10101/tic_tac_toe from browser