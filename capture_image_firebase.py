def upload_image(filename):
    from picamera2 import Picamera2
    import cv2
    import os
    import time
    import firebase_admin
    from firebase_admin import credentials, storage
    from datetime import datetime

    # Initialize Firebase
    cred = credentials.Certificate('/home/tirta/Desktop/TUGAS_AKHIR/serviceAccountKey.json')
    firebase_admin.initialize_app(cred, {
        'storageBucket': 'smart-lock-firebase-b1b7b.appspot.com'
    })

    bucket = storage.bucket()

    # Path to store the image in Firebase Storage
    firebase_storage_path = f"Images/{filename}.jpg"

    # Upload the image to Firebase Storage with metadata
    blob_image = bucket.blob(firebase_storage_path)
    metadata = {
        'class': 'verified',  # Custom metadata
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Timestamp
    }
    blob_image.upload_from_filename(new_filepath)





