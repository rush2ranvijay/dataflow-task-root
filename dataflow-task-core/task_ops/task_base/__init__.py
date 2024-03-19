from task_ops.base.environments import env

ROOT_DATAFLOW_TASK = "dataflow_tasks"
JOB_NAME_PARAM = "job_name"
TENANT_ID_PARAM = "tenant_id"
REGION_NAME = "region_name"


def get_dataflow_task_section(dataflow_task_name, section_name):
    if section_name is not None:
        return env.get_section(f"{ROOT_DATAFLOW_TASK}.{dataflow_task_name}.{section_name}")
    else:
        return env.get_section(f"{ROOT_DATAFLOW_TASK}.{dataflow_task_name}")


def get_config_section_by_key(config_key):
    """
           This method loads all the configuration details, base on its name given in config yaml files like
           defaults, dev or prod. the format should be like root.key
    """
    if config_key is None:
        return None
    else:
        return env.get_section(config_key)

