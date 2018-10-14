# Catch Fat Criminals

Catch Fat Criminals uses Machine Learning to match a person's face, with how likely they are to commit crimes. Using this data, we can then identify potential criminals in a neighbourhood, but using image recognition software with the CCTVs around the area.

# video demo
https://youtu.be/0QuyB1zrIcE


# How It Works

CrimeClassifier.ipynb is a Jupyter notebook which describes how we managed to train our decision tree classifier, achieving an accuracy of 0.92. The safe decision tree model is taught in 

Facial Recognition.ipynb and Facial Recognition.py is what we use to detect the faces of people in the video.

facial_recognition_server.py is the server used to handle API calls to the facial recognition module.

app.js is an Express app, used to render the landing page, where users can input data. It also handles the processed data (after classifiying the users) and stores it in a database.

# Getting Started

Go to your preferred directory, and clone the repo.
```
git clone https://github.com/chinzhiweiblank/NTUition2018.git
```

For the website, you will have to install [npm](https://www.npmjs.com/get-npm) and [pip](https://pip.pypa.io/en/stable/installing/). Once done, install the dependencies.
```
cd NTUition2018
npm install
pip install
```
Since the dataset is over GitHub's limit of 100MB, you will have to download the [files](https://www.kaggle.com/account/login?ReturnUrl=%2fc%2f4458%2fdownload-all) with a Kaggle/Gmail account. Put train.csv in your working directory.

# How To Use

This project is split into 2 portions:
1. Creating the database of inidividuals with probability of comitting crime
2. Run facial recognition software with database of software


# Creating the database of individuals
Users will first have to run the servers for the app, and the API server.
```
node app.js
python facial_recognition_server.py

```
[http://localhost:8000](https://localhost:8000)
This runs a two servers whereby the node server handles a html page to input user details and pictures. The node server then will make an api call to the python server to run the decision tree and returning the information to the node server which is then saved on a database.

# Run facial recognition software
Once the database is created, we will then use facial recognition to match individuals from live video stream to our database.

```
python Facial Recognition.py
```
Run this command to run the facial recognition camera which launches via the laptop webcamera. This displays the bounding box in real-time around criminal faces. 



# Adding new faces into the database
```
Go to database_facial and add a picture of an individual, and go inside database_facial/criminal.txt and input person name,crime,probability 
```

Alternatively, if users want to add in new data sets, they can go to [http://localhost:8000](https://localhost:8000), and input some data using the form provided. Once sent, data will be sent to the API server, and processed, before sending it back to the app where it will be stored.



# Model files
The pre-trained model is in the filename.joblib.


# Suggested Improvements
1) Better Facial Recognition
2) More comprehensive dataset for analysis
3) Integrate with hardware such as autonomous drones or RCs or self-swivelling cameras
4) Better models for prediction and higher accuracy
5) Link up with surveillance videos to improve and assess accuracy in real life
