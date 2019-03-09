import io

import boto3
import qrcode
import qrcode.image.svg


class RecipientTagGenerator:

    @staticmethod
    def create():
        bucket = boto3.resource('s3').Bucket('hackqc2019')
        return RecipientTagGenerator(app_url="https://hackqc2019.com/donate", bucket=bucket)

    def __init__(self, app_url, bucket):
        self._app_url = app_url
        self._bucket = bucket

    def create_tag(self, recipient):
        s3_key = f'tags/{recipient}.svg'

        with io.BytesIO() as image:
            self._create_tag_image(recipient).save(image)

            image.seek(0)
            self._bucket.put_object(
                Key=s3_key,
                Body=image,
                ContentType='image/svg+xml',
                ACL='public-read'
            )

        return {
            'qrcode_url': f'https://s3-ca-central-1.amazonaws.com/{self._bucket.name}/{s3_key}'
        }

    def _create_tag_image(self, recipient):
        factory = qrcode.image.svg.SvgPathImage
        return qrcode.make(f'{self._app_url}/{recipient}', image_factory=factory)
