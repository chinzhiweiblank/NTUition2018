# Catch Fat Criminals

Catch Fat Criminals uses Machine Learning to match a person's face, with how likely they are to commit crimes. Using this data, we can then identify potential criminals in a neighbourhood, but using image recognition software with the CCTVs around the area.

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

# How It Works

CrimeClassifier.ipynb is a Jupyter notebook which describes how we managed to train our decision tree classifier, achieving an accuracy of 0.92. The safe decision tree model is taught in 

Facial Recognition.ipynb and Facial Recognition.py is what we use to detect the faces of people in the video.

facial_recognition_server is the server used to handle API calls to the facial recognition module.

app.js is an Express app, used to render the landing page, where users can input data. It also handles the processed data (after classifiying the users) and stores it in a database.
