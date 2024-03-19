import sys

from task_ops.base import logutils
from task_ops.tasks_dataflow.simple_dataflow_task import SimpleDataflowTask

log = logutils.get_logger(__name__)


def main():
    # args = ['/tmp/glue-python-scripts-Q1FI/simple_task_launcher.py', '--extra-py-files',
    # 's3://aws-glue-assets-383236716621-us-east-2/app/convertML-0.1.0-py3-none-any.whl', '--job_name',
    # 'churn_ml_model_ranvijay', '--scriptLocation',
    # 's3://aws-glue-assets-383236716621-us-east-2/app/scripts/simple_task_launcher.py', '--python-version', '3.9',
    # '--tenant_id', 'ranvijay']
    return SimpleDataflowTask("simple_task", "config", **{"sys_argv": sys.argv[1:]}).run()


if __name__ == "__main__":
    main()
