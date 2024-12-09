from utils.constants import AWS_ACCESS_KEY_ID, AWS_ACCESS_KEY
import s3fs


def connect_to_s3():
    try:
        s3 = s3fs.S3FileSystem(anon = False,
                               key = AWS_ACCESS_KEY_ID,
                               secret = AWS_ACCESS_KEY)
        return s3
    except Exception as e:
        print(e)

def create_bucket_if_not_exists(s3, bucket):
    try:
        if not s3.exists(bucket):
            s3.mkdir(bucket)
            print('Bucket Created')
        else:
            print('Bucket exists')
    except Exception as e:
        print(e)

def upload_to_s3(s3, file_path, bucket, s3_file_name):
    try :
        s3.put(file_path, bucket + '/raw/' + s3_file_name)
        print('File uploaded')
    except FileNotFoundError :
        print('The file eas not found')