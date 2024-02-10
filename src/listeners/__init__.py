# isort: dont-add-imports

from pkgutil import iter_modules

LOAD_EXTENSIONS = [module.name for module in iter_modules(__path__, f"{__package__}.")]
