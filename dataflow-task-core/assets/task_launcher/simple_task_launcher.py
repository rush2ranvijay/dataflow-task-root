import sys

from task_ops.base import logutils
from task_ops.task_base.task_args import get_db_url, get_task_id
from task_ops.tasks_dataflow.simple_dataflow_task import SimpleDataflowTask

log = logutils.get_logger(__name__)


def main():
    print('******************************************************************')
    print('spring.cloud.task.executionid cmd arg : {}'.format(get_task_id()))
    print('get_db_url : {}'.format(get_db_url()))
    print('******************************************************************')
    return SimpleDataflowTask("simple_task", "config", **{"sys_argv": sys.argv}).run()


if __name__ == "__main__":
    main()
