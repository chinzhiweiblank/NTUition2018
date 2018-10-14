# Catch Fat Criminals

Catch Fat Criminals uses Machine Learning to match a person's face, with how likely they are to commit crimes. Using this data, we can then identify potential criminals in a neighbourhood, but using image recognition software with the CCTVs around the area.

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

Users will first have to run the servers for the app, and the API server.
```
node app.js
python facial_recognition_server.py
```

After that, users can run the facial recognition program.
```
python Facial Recognition.ipynb
```
The program will capture the faces of those in the video, and run the classifier to determine the likelyhood of the person commiting a crime in the future. This would be displayed real-time on the video screen.

If users want to add in new data sets, they can go to [http://localhost:8000](https://localhost:8000), and input some data using the form provided. Once sent, data will be sent to the API server, and processed, before sending it back to the app where it will be stored.

