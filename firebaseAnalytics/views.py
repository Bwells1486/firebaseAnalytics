from django.shortcuts import render
import pyrebase
 
config={
    apiKey: "AIzaSyDWb4Ek94NjS1sbW30lJ66jG4NLRJik78I",
    authDomain: "rogue-media-project.firebaseapp.com",
    databaseURL: "https://rogue-media-project-default-rtdb.firebaseio.com",
    projectId: "rogue-media-project",
    storageBucket: "rogue-media-project.appspot.com",
    messagingSenderId: "649044300996",
    appId: "1:649044300996:web:6846c487fba696201b6591",
}
firebase=pyrebase.initialize_app(config)
authe = firebase.auth()
database=firebase.database()
 
def home(request):
    user1 = database.child('Users').child(1).get()
    user2 = database.child('Users').child(2).get()
    user3 = database.child('Users').child(3).get()
    return render(request,"Home.html",{"user 1":user1,"user 2":user2,"user 3":user3 })