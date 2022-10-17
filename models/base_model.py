from abc import ABC, abstractmethod
from typing import Any, Dict

import project


class BaseModel(ABC):
    @classmethod
    @abstractmethod
    def collection_name(cls) -> str:
        return cls.COLLECTION  # type: ignore

    @staticmethod
    @abstractmethod
    def parse(db_dict: Dict[str, Any], cache: 'project.CacheManager') -> 'BaseModel':
        pass
