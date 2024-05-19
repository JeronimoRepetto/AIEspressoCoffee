# AI Espresso Coffe
This repository contains the code for AI Espresso Coffe

## Setup
To run the project, you need to:
- Download the repository
- Optional: Create a virtual environment
- Install the dependencies by running:
	- ```pip install -r requirements.txt```
- Create a file called ```.env```
	- In the file, place the keys. For the project as shown in the video (and this repository), I am using:
	- ```OPENAI_API_KEY=XXXXXX```
	- ```ELEVENLABS_API_KEY=XXXXXX```
	- ```WEATHER_API_KEY=XXXXXX```

## Adjustments
The project has some things you might want to modify, for example:

- In the LLM class, you can modify it so that the assistant is not "rude". It is used in 2 places in the file.
- In the PcCommand class, it opens Chrome by looking for it in a fixed path for Windows. You can modify it to look for the executable on Mac / Linux.

## Execution
- This project uses Flask. You can start the server in debug mode by default on port 5000 with the command:
	- ```flask --app app run --debug```
	- In your browser, go to http://localhost:5000
	- Click to start recording (it will ask for permission). Click to stop recording
	- Wait and see how it takes over the world

## Licenses
- Microphone image by Freepik

## Inspiration and Base Code
https://github.com/ringa-tech/asistente-virtual
