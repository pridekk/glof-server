import firebase_admin
from firebase_admin import credentials
from firebase_admin import auth
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)

decoded_token = auth.verify_id_token("test")

if __name__ == "__main__":
    print("test")