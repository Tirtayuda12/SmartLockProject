import firebase_admin
from firebase_admin import credentials, storage

cred = credentials.Certificate('/home/tirta/Desktop/TUGAS_AKHIR/serviceAccountKey.json')
firebase_admin.initialize_app(cred, {
    'storageBucket':'smart-lock-firebase-b1b7b.appspot.com',
    'databseURL':'https://smart-lock-firebase-b1b7b-default-rtdb.asia-southeast1.firebasedatabase.app'
})

def upload_image(file_path, destination_blob_name):
    """Upload gambar ke bucket."""
    bucket = storage.bucket()
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(file_path)
    blob.make_public()
    print(f'File {file_path} diunggah ke {destination_blob_name}.')
    print(f'URL publik: {blob.public_url}')

file_path = './foto_sementara/naruto.jpg'
destination_blob_name = 'Images/your_image.jpg'

upload_image(file_path, destination_blob_name)