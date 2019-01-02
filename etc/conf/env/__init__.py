__author__ = "Suyash Soni"
__email__ = "suyash.soni@srijan.net"
__copyright__ = "Copyright 2018, Srijan Technologies"

import sys, pkgutil, inspect, importlib

# Dict, stores env name and env class mapping. e.g. 'dev': <class 'etc.conf.env.dev.DevConfig'>
ENV_CONFIG = dict()
package = sys.modules[__name__]
__config_pkg_loc__ = __name__
__config_classes__ = {}

for importer, modname, ispkg in pkgutil.iter_modules(package.__path__):
    imodule = importlib.import_module('{}.{}'.format(__config_pkg_loc__, modname))
    for member in inspect.getmembers(imodule, inspect.isclass):
        __config_classes__[member[0]] = member[1]

for env_cls_name, env_cls in __config_classes__.items():
    env_name = getattr(env_cls, '__env__', None)
    if env_name: ENV_CONFIG[env_name] = env_cls

__all__ = ["ENV_CONFIG"]