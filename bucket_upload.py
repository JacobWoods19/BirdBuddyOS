from google.cloud import storage
import os
def make_bucket_public(bucket_name):
    """Makes a bucket publicly readable."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    policy = bucket.get_iam_policy(requested_policy_version=3)

    policy.bindings.append({
        "role": "roles/storage.objectViewer",
        "members": {"allUsers"},
    })

    bucket.set_iam_policy(policy)

    print(f"Bucket {bucket.name} is now publicly readable")
def list_buckets(credentials_json):
    """Lists all buckets in the project specified in the service account JSON."""
    # Initialize a storage client with specified credentials
    storage_client = storage.Client.from_service_account_json(credentials_json)
    
    # Fetch all buckets
    buckets = storage_client.list_buckets()

    # Print the names of the buckets
    for bucket in buckets:
        print(bucket.name)
#Function to list all objects in a bucket
def list_blobs(bucket_name, credentials_json):
    """Lists all the blobs in the bucket."""
    storage_client = storage.Client.from_service_account_json(credentials_json)
    bucket = storage_client.get_bucket(bucket_name)

    blobs = bucket.list_blobs()
    blob_amt = 0
    for blob in blobs:
        print(blob.name)
        blob_amt += 1
    print(f"Total number of blobs: {blob_amt}")


# Function to upload a file to a Google Cloud Storage bucket
def upload_to_gcs(bucket_name, source_file_name, destination_blob_name, credentials_json):
    """Uploads a file to the specified GCS bucket."""
    # Explicitly use service account credentials by specifying the private key file.
    storage_client = storage.Client.from_service_account_json(credentials_json)

    # Get the bucket
    bucket = storage_client.get_bucket(bucket_name)

    # Create a new blob (file object) in the bucket
    blob = bucket.blob(destination_blob_name)

    # Upload the file
    blob.upload_from_filename(source_file_name)

    # Optionally, make the blob publicly viewable
    blob.make_public()

    # Return the public URL
    return blob.public_url

# # # Specific details for your upload
bucket_name = "clippy_bird-2"
# source_file_name = "C:/Users/mrwoo/OneDrive/Documents/GitHub/BirdBuddyOS/Photos/2024-04-29/360_F_177476718_VWfYMWCzK32bfPI308wZljGHvAUYSJcn.jpg"
# destination_blob_name = "BIRD.jpg"
credentials_json = "C:/Users/mrwoo/OneDrive/Documents/GitHub/BirdBuddyOS/key.json"

# # # # Perform the upload and print the resulting public URL
# url = upload_to_gcs(bucket_name, source_file_name, destination_blob_name, credentials_json)
# print(url)
# # print("Image uploaded successfully! Public URL: ", url)
# # List all buckets in the project
# list_buckets(credentials_json)
# # List all objects in a bucket
list_blobs(bucket_name, credentials_json)