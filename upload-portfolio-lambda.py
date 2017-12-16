import boto3
from botocore.client import Config
import io
import zipfile
import mimetypes

def lambda_handler(event, context):
    # TODO implement
    sns = boto3.resource('sns')
    topic = sns.Topic('arn:aws:sns:us-east-1:917817934803:deployPortfolioTopic')
    try:
        job = event.get("CodePipeline.job")
        #TO RUN OUTSIDE OF CODEPIPELINE
        location = {
            "bucketName": 'netra-portfolio-app-build',
            "objectKey": 'netra-portfolio-app.zip'
        }
        if job:
            for artifact in job["data"]["inputArtifacts"]:
                if artifact["name"] == "MyAppBuild":
                    location = artifact["location"]["s3Location"]

        print("Building portfolio from " + str(location))

        s3 = boto3.resource('s3',config=Config(signature_version='s3v4'))
        portfolio_bucket = s3.Bucket('netra-portfolio-app')
        portfolio_build_bucket = s3.Bucket(location["bucketName"])

        portfolio_zip = io.BytesIO()
        portfolio_build_bucket.download_fileobj(location["objectKey"], portfolio_zip)

        with zipfile.ZipFile(portfolio_zip) as myzip:
            for nm in myzip.namelist():
                obj = myzip.open(nm)
                portfolio_bucket.upload_fileobj(obj,nm, ExtraArgs={'ContentType': mimetypes.guess_type(nm)[0]})
                portfolio_bucket.Object(nm).Acl().put(ACL='public-read')

        portfolio_zip.close()
        print('Job done')
        topic.publish(Subject="portfolio Deployed", Message="Your deploy is successful")
        if job:
            codepipeline = boto3.client('codepipeline')
            codepipeline.put_job_success_result(jobId=job["id"])
    except:
        topic.publish(Subject="portfolio deploy failed", Message="Your deploy is failed")
        raise

    return 'Hello from Lambda'
