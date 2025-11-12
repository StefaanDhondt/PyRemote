# Introduction
This is a Flask app to run on a Windows PC, to control mouse and keyboard from a browser (Connect to `http://<ip windows machine>:5000`).
You can use this e.g. to control a Windows PC from Home Assistant by using a webpage card (https://www.home-assistant.io/dashboards/iframe/).

# Development
## Getting started
1. Run `dsvenv` (https://pypi.org/project/dsvenv/) in the root folder. It'll create a venv with the right Python version and dependencies.
2. Open the root folder in VSCode.
   - You can run the app with the `Python: Flask` config.
   - To create an `exe`, use the `Build` task.
