import os
import io
import boto3

class S3Handler:
    
    def __init__(self, bucket_name: str, access_key: str, secret_key: str, endpoint: str):   
        
        self.__BUCKET_NAME = bucket_name
        self.session = boto3.session.Session()
        self.__CLIENT = self.session.client(service_name='s3',
                                            endpoint_url=endpoint, 
                                            aws_access_key_id=access_key, 
                                            aws_secret_access_key=secret_key
                                            )

    
    def save(self, file_path, content: bytes):

        content_bytes = io.BytesIO(content)

        self.__CLIENT.put_object(Bucket=self.__BUCKET_NAME,
                                 Key=file_path,
                                 Body=content_bytes,
                                )
        return file_path
    
    
    def load(self, file_name):
        
        res = self.__CLIENT.get_object(Bucket=self.__BUCKET_NAME,
                                       Key=file_name
                                       )
        
        file = res['Body'].read()

        return file

s3_handler = S3Handler(bucket_name=os.environ.get("BUCKET_NAME"),
                       access_key=os.environ.get("ACCESS_KEY"),
                       secret_key=os.environ.get("SECRET_KEY"),
                       endpoint=os.environ.get("S3_URL")
                      )