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
        s3 = boto3.resource('s3',config=Config(signature_version='s3v4'))
        portfolio_bucket = s3.Bucket('netra-portfolio-app')
        portfolio_build_bucket = s3.Bucket('netra-portfolio-app-build')

        portfolio_zip = io.BytesIO()
        portfolio_build_bucket.download_fileobj('netra-portfolio-app.zip', portfolio_zip)

        with zipfile.ZipFile(portfolio_zip) as myzip:
            for nm in myzip.namelist():
                obj = myzip.open(nm)
                portfolio_bucket.upload_fileobj(obj,nm, ExtraArgs={'ContentType': mimetypes.guess_type(nm)[0]})
                portfolio_bucket.Object(nm).Acl().put(ACL='public-read')

        portfolio_zip.close()
        print('Job done')
        topic.publish(Subject="portfolio Deployed", Message="Your deploy is successful")
    except:
        topic.publish(Subject="portfolio deploy failed", Message="Your deploy is failed")
        raise

    return 'Hello from Lambda'
