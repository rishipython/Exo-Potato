import pickle
from django.shortcuts import HttpResponse, HttpResponseRedirect, render
from numpy import genfromtxt
import numpy as np
import os
from io import StringIO
import pandas as pd
from pickle import load
from django.core.files.storage import FileSystemStorage
import inspect
import matplotlib.pyplot as plt
import json 
import pyrebase
# Create your views here.



config = {
  "apiKey": "AIzaSyCekvkaoDeGhHzTKiujxf0hU3HDdz95JWg",
  'authDomain': "exoplanethunter-2bc17.firebaseapp.com",
  'projectId': "exoplanethunter-2bc17",
  'storageBucket': "exoplanethunter-2bc17.appspot.com",
  'messagingSenderId': "27249178198",
  'appId': "1:27249178198:web:e4665f5d39b1d80988edf7",
  'measurementId': "G-5M5GN7F3BG", 
  "databaseURL": "https://console.firebase.google.com/project/exoplanethunter-2bc17/storage/exoplanethunter-2bc17.appspot.com/files"
}

firebase = pyrebase.initialize_app(config)
storage = firebase.storage()






model = load(open("C:\\Users\harsh\\Downloads\\blindsite_-_Copy_2\\blindsite - Copy (2)\\homepage\\knn.pkl","rb"))
global fileString
prob = None
def home(request):
    if(request.method=="POST" and request.FILES['file']):
        global fileString
        theFile = request.FILES["file"]
        fs = FileSystemStorage()
        filename = fs.save(theFile.name, theFile)
        uploaded_file_url = fs.url(filename)
        fileString = str(uploaded_file_url)
        return HttpResponseRedirect('upload')
    return render(request, 'homepage/home.html')

def upload(request):
    thePath = os.path.abspath(inspect.getfile(home))
    global prob
    global fileString
    cond = False
    my_data = get_csv_file("C:\\Users\harsh\\Downloads\\blindsite_-_Copy_2\\blindsite - Copy (2)\\"+str(fileString))
    result = model.predict(np.array([my_data]))
    if result[0] == 1:
        cond = True
    myVar = flux_graph(my_data, "fluxgraph")
    return render(request, 'homepage/results.html', {'cond':cond,'prob':prob, 'my_data':my_data.tolist(), 'storageVar':myVar})


    


def get_csv_file(file):
  csv_file = pd.read_csv(file)
  return np.array(csv_file.loc[:, 'VALUE'])

def flux_graph(arr, file):
    fig = plt.figure(figsize=(20,5), facecolor=(.18, .31, .31))
    ax = fig.add_subplot()
    ax.set_facecolor('#004d4d')
    ax.set_title("Change in Flux", color='white', fontsize=22)
    ax.set_xlabel('time', color='white', fontsize=18)
    ax.set_ylabel('Flux Change (Hz)', color='white', fontsize=18)
    ax.grid(False)
    ax.plot([i + 1 for i in range(len(arr))], arr, '#00f000')
    ax.tick_params(colors = 'black', labelcolor='#00ffff', labelsize=14)
    plt.savefig(f"{file}.png")
    
    path_on_cloud = f'graphs/{file}.png'
    storage.child(path_on_cloud).put(f'{file}.png')
    os.remove('fluxgraph.png')
    storage_url = storage.child(path_on_cloud).get_url(None)
    print(storage_url)
    return storage_url

