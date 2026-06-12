import os
import boto3



def upload_file_to_s3(file_path):
    s3 = boto3.client("s3")
    object_name = os.path.basename(file_path)
    print(object_name)

    with open(file_path, "rb") as f:
        s3.upload_fileobj(
            f,
            Bucket="music-party",
            Key=object_name,
            ExtraArgs={
                "ContentType": "audio/mpeg",
                "ContentDisposition": "inline"
            }
        )

def get_url( key):
    s3 = boto3.client("s3")
    return s3.generate_presigned_url(
        ClientMethod="get_object", Params={"Bucket": "music-party", "Key": key}, ExpiresIn=3600
    )

def delete_file_from_s3(key):
    s3 = boto3.client("s3")
    s3.delete_object(Bucket="music-party", Key=key)
    return "success"