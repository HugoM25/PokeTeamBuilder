<h1 align="center"> Pokemon Team Generator </h1>

<img align="center" width="100%" src="https://github.com/HugoM25/PokeTeamBuilder/blob/master/webapp_example.png" alt="cover" />

<!-- Table of Contents -->
# Table of Contents
- [About the Project](#about-the-project)
  * [Context](#context)
  * [Made with](#made-with)
  * [Features](#features)
- [Getting Started](#getting-started)
  * [Prerequisites](#prerequisites)
  * [Installation](#installation)
- [Usage](#usage)
  * [Launch the app locally](#launch-the-app-locally)
  * [Update the app](#update-the-app)
- [Examples](#examples)
- [License](#license)
- [Author](#author)

# About the Project 

## Context  

This project is a remake of one of my old projects (made in plain javascript and using the python framework flask as backend). In order to improve in full-stack development I decided to remake it using angular as frontend framework.

The goal of this project is to allow the user to generate a viable competitive team easily from the pokemons of his choice. Additional features have been added such as viewing the statistics of a tier. You will be able to see the average speed of the pokemon in the tier or the most represented type for example.

## Made with 

The fronted has been made using `angular`.
The backend has been made using the python `flask` framework and `neo4j` for the database.

## Features 

This web app allows you to easily generate pokemon teams and view statistics on current tiers. The generated Pokemon teams can be easily exported in the showdown format. You can choose and lock some pokemons you really want to play with and the app will generate a team around them.

<img align="center" width="100%" src="https://github.com/HugoM25/PokeTeamBuilder/blob/master/team_poke_generation.gif" alt="generation_team_example_gif" />

# Getting Started

## Prerequisites 

In order to make the web app work you will need to have npm installed.
You will also need python 3.X installed with the libraries listed in the [requirements.txt](https://github.com/HugoM25/PokeTeamBuilder/blob/master/backend/app/requirements.txt) file.

## Installation 

Clone this repository and follow the [usage](#usage) part in order to launch the app. 

# Usage 

## Launch the app locally

  1. Start the database 
  
  Go to the db folder and in a terminal execute this command : 
  ```console
  neo4j/bin/neo4j start 
  ```
  
  2. Start the backend 
  
  In the backend/app folder execute this command : 
  ```console
  python api.py 
  ```
  
  3. Start the frontend 
  
  In the frontend folder execute this command to start the frontend : 
  ```console 
  ng serve 
  ```
  
  Open [http://localhost:4200/](http://localhost:4200/) and enjoy the webapp.
  
 ## Update the app 
 
 Every month, new data are shared by smogon, in order to keep the database up to date you need to run the `update.py` script which will automatically update the database. 
 
 ```console
 python update.py
 ```
 
 This update can take up to a few minutes for each tier you decide to track. You can choose which tiers to track by modifying the settings.json file.
 Just add a property containing the name of the tier and the name of the file present on [this page](https://www.smogon.com/stats/2022-12/chaos/) 
 ```json
 "tiersTracked": {
        "GEN8OU": {
            "name" : "[Gen8] OU",
            "fileNameShowdown": "gen8ou-0.json"
        },
        "GEN8UU": {
            "name" : "[Gen8] UU",
            "fileNameShowdown": "gen8uu-0.json"
        },
        "GEN8RU": {
            "name" : "[Gen8] RU",
            "fileNameShowdown": "gen8ru-0.json"
        },
        "GEN8BDSPOU": {
            "name" : "[BDSP] OU",
            "fileNameShowdown": "gen8bdspou-0.json"
        },
        "GEN9OU":{
            "name" : "[Gen9] OU",
            "fileNameShowdown": "gen9ou-0.json"
        }
    },
```
# Examples

[WIP] Needs to implement some functionalities before release.

# License 

Distributed under the MIT License. 

# Author

- [@HugoM25](https://github.com/HugoM25)
