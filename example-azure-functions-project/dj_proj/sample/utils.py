from functools import lru_cache
import pkg_resources


@lru_cache(maxsize=2)
def get_installed_packages():
    """
    List the packages we can see at runtime
    """
    return [(dist.project_name, dist.version) \
        for dist in pkg_resources.working_set]
