import pyrebase

firebaseConfig = {
  "apiKey": "AIzaSyD-EgQSVpcSCbxSt9z4VxqJEQJ9zE_MrE4",
  "authDomain": "simpliise.firebaseapp.com",
  "projectId": "simpliise",
  "storageBucket": "simpliise.firebasestorage.app",
  "messagingSenderId": "76864127343",
  "appId": "1:76864127343:web:caeafff4db6f8e545b689a",
  "measurementId": "G-VQL4639R2E",
  "databaseURL": ""
}
firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()
