import boto3
import os
from dotenv import load_dotenv
import json

class AWS():
    def __init__(self):
        try:
            load_dotenv()
            with open('./config/config.json','r') as f:
                config = json.loads(f.read())
                f.close()
            self.__s3 = boto3.resource(
                service_name = 's3',
                region_name = config.get('AWS_S3_REGION_NAME'),
                aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID'),
                aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
            )
            self.__bucketName = config.get('AWS_S3_BUCKET_NAME')
        except Exception as err:
            print(err)
            
    def uploadToS3(self, filePath = '', pdfString = '', isSavedPdf = True):
        if(isSavedPdf):
            if(os.path.exists(filePath)):
                try:
                    self.__s3.Bucket(self.__bucketName).upload_file(Filename = filePath, Key = os.path.basename(filePath))
                    print(os.path.basename(filePath), 'uploaded')
                except Exception as e:
                    print(e)
            else:
                print('No such file exists')
        else:
            try:
                self.__s3.Bucket(self.__bucketName).put_object(Key = f'{filePath.replace(" ","-")}.pdf', Body = pdfString)
            except Exception as e:
                print(e)

    def downloadFromS3(self, fileName: str):
        try:
            self.__s3.Bucket(self.__bucketName).download_file(Key = fileName, Filename = fileName)
        except Exception as e:
            print(e)

if __name__ == '__main__':
    obj = AWS()
    # obj.uploadToS3('./pdfs/30-days-Fast-Track-Data-Science-Interview-Preparation.pdf')
    # for file in os.listdir('./pdfs'):
    #     obj.uploadToS3(os.path.join('./pdfs',file))
    obj.downloadFromS3('30-days-Fast-Track-Data-Science-Interview-Preparation.pdf')