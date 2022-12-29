<h1 align="center"> Pokemon Team Generator </h1>

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
- [Examples](#examples)
- [License](#license)
- [Author](#author)

# About the Project 

## Context 

This project is a remake of one of my old projects made in plain javascript and using the python framework flask as backend. In order to improve in full-stack development I decided to remake it using angular as frontend framework.

## Made with 

The fronted has been made using `angular`
The backend has been made using python `flask` framework and `neo4j` for the database

## Features 

This web app allows you to easily generate pokemon teams and view statistics on current tiers. The generated Pokemon teams can be easily exported in the showdown format.

# Getting Started

## Prerequisites 

In order to make the web app work you will need to have npm installed.
You will also need python 3.X installed with the libraries listed in the [requirements.txt]() file.

## Installation 

# Usage 

  1. Start the database 
  
  Go to the backend folder and in a terminal execute this command : 
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

# Examples

# License 

Distributed under the MIT License. 

# Author

- [@HugoM25](https://github.com/HugoM25)
