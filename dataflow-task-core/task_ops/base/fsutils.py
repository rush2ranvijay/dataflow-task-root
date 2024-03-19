import os
from pathlib import Path

from task_ops import S3Url, exists_s3, open_s3, is_running_in_glue
from task_ops.base.logutils import get_logger
from task_ops.exceptions import IllegalStateException

_log = get_logger(__name__)


def fs_open(path: str):
    if s3_bucket:
        full_path = f"{app_home}/{path}"
        _log.info(f"Opening path 's3://{s3_bucket}/{full_path}' as input stream")
        fs = open_s3(s3_bucket, full_path)
    else:
        _log.info(f"Opening path '{path}' as input stream")
        fs = open(path)

    return fs


def fs_exists(path: str) -> bool:
    if s3_bucket:
        full_path = f"{app_home}/{path}"
        exist = exists_s3(s3_bucket, full_path)
    else:
        exist = os.path.exists(path)
    return exist


def s3_bucket_and_app_home():
    # This method assume that script is defined
    # APP_HOME/scripts/xyz-job.py
    # This method read the --scriptLocation argument
    if is_running_in_glue():
        url = S3Url("s3://aws-glue-assets-383236716621-us-east-2/app/scripts")
        app_home = Path(url.key).parent
        posix_path = None
        while app_home:
            posix_path = app_home.as_posix()
            if posix_path == ".":
                raise IllegalStateException("Script location parent(or grandparent) must have conf/ directory in it's "
                                            "parent")
            if exists_s3(url.bucket, f"{posix_path}/conf/defaults.yaml"):
                break
            app_home = app_home.parent
    else:
        return None, None

    return url.bucket, posix_path


s3_bucket, app_home = s3_bucket_and_app_home()
