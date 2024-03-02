### May 2022

## Development Team

<ul>
    <li>Keenan Flynn</li>
    <li>Jasmine Thai</li>
    <li>Martin Yap</li>
    <li>Hoyun Yoon</li>
</ul>

## Project Description

Using famous quotes from across the globe, this project seeks to generate new and fun quotes with generative LSTM neural networks. A user can generate a quote with an interactive UI, being able to choose the length, starting word, and fuziness (or the ridiculousness) of the quote. It will also attribute the quote to a fictional person.

The LSTM model is interacted with through a Python Flask app. 

## Datasets

The project utilizes the following datasets in order to train the LSTM model.

- Approximately 1,600 inspirational quotes (https://github.com/dwyl/quotes)
- Approximately 39,000 quotes (https://github.com/alvations/Quotables)


## Presentation


Presentation: https://docs.google.com/presentation/d/1437VA4elB5--_IDGWHrJJpO0wxdTeqO4nKTAJRgMJ3Y/edit?usp=sharing

Video Presentation: https://www.youtube.com/watch?v=GjASZmY6T-Y&t=2s

## Installation


How to run the code after git clone:
    
    Open command prompt

    1.) cd tab to the folder with app.py
    
    2.) set FLASK_APP = app.py
    
    3.) set FLASK_DEBUG=1
    
    4.) flask run (if this doesn't work use the command below)
        python -m flask run
