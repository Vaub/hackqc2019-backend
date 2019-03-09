import io

import boto3
import qrcode
import qrcode.image.svg

TAG_BUCKET = 'hackqc2019'


def create_tag(recipient):
    bucket = boto3.resource('s3').Bucket(TAG_BUCKET)
    with io.BytesIO() as image:
        _create_tag_image(recipient).save(image)

        image.seek(0)
        bucket.put_object(
            Key=f'{recipient}.svg',
            Body=image,
            ContentType='image/svg+xml',
            ACL='public-read'
        )

    return {
        'qrcode_url': f'https://s3-ca-central-1.amazonaws.com/{TAG_BUCKET}/{recipient}.svg'
    }


def _create_tag_image(recipient):
    factory = qrcode.image.svg.SvgPathImage
    return qrcode.make(f'https://hackqc2019/donate/{recipient}', image_factory=factory)
