from abc import ABC, abstractmethod
from typing import Any, Dict, Type, TypeVar

import project

T = TypeVar('T')


class BaseModel(ABC):
    @classmethod
    def collection_name(cls) -> str:
        return cls.COLLECTION  # type: ignore

    @classmethod
    @abstractmethod
    def parse(cls: Type[T], db_dict: Dict[str, Any], cache: 'project.CacheManager') -> T:
        pass
