My_Bucket = '<Your-Bucket-Here>'  #Example myBucket6385

import boto3

def lambda_handler(event, context):
   s3 = boto3.resource('s3')
   bucket = s3.Bucket(My_Bucket)
   bucket.object_versions.delete()
   bucket.delete()

   #Don't forget to give me permissions to delete S3 (create inline policy)
