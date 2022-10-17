from typing import Type

import models


class UnregisteredSourceError(Exception):
    def __init__(self, model: Type[models.BaseModel]):
        msg = f"Model '{model.__name__}' is not registered"
        super().__init__(msg)
