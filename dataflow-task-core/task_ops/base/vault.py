from task_ops.base.generalutils import instantiate
from task_ops.base.secrets import SecretVault


def new_secret_vault(env) -> SecretVault:
    instance = None
    if env.flag("sys.vault.enabled"):
        impl = env.get_property("sys.vault.impl")
        impl_kwargs = env.get_section("sys.vault.impl_kwargs")
        instance = instantiate(impl, impl_kwargs)
    return instance
