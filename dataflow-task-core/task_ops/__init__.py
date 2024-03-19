import os
from contextlib import contextmanager
from urllib.parse import urlparse

import boto3
from botocore.exceptions import ClientError
from botocore.response import StreamingBody


def is_running_in_glue():
    return os.environ.get("GLUE_INSTALLATION") is not None


class S3Url(object):

    def __init__(self, url):
        self._parsed = urlparse(url, allow_fragments=False)

    @property
    def bucket(self):
        return self._parsed.netloc

    @property
    def key(self):
        if self._parsed.query:
            return self._parsed.path.lstrip('/') + '?' + self._parsed.query
        else:
            return self._parsed.path.lstrip('/')

    @property
    def url(self):
        return self._parsed.geturl()


_s3_client = boto3.client("s3")


@contextmanager
def open_s3(bucket: str, key: str, **kwargs) -> StreamingBody:
    """
    This method must be called with context manager
    :param bucket: s3 bucket
    :param key: file key
    :return: content stream as file-like object
    """
    body: StreamingBody = _s3_client.get_object(Bucket=bucket, Key=key, **kwargs)['Body']
    try:
        yield body
    finally:
        body.close()


def exists_s3(bucket: str, key: str) -> bool:
    """
    This method test if the specified key exists in bucket
    :param bucket:
    :param key:
    :return: true if key exists
    """
    try:
        _s3_client.head_object(Bucket=bucket, Key=key)
        exists = True
    except ClientError as e:
        error_code = e.response['Error']['Code']
        if error_code == '404':
            exists = False
        else:
            raise
    return exists
