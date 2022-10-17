from abc import ABC, abstractmethod
from typing import Iterator, Optional, Type, TypeVar

import models

TModel = TypeVar('TModel', bound=models.BaseModel)


class CacheManager(ABC):
    def __init__(self, project_id: str):
        self._project_id = project_id

    @property
    def project_id(self) -> str:
        return self._project_id

    @abstractmethod
    def register(self, model: Type[models.BaseModel]) -> None:
        pass

    @abstractmethod
    def get(self, model: Type[TModel], id_: str) -> TModel:
        pass

    @abstractmethod
    def collection(self, model: Type[TModel]) -> Iterator[TModel]:
        pass

    @abstractmethod
    def clear(self, model: Optional[Type[TModel]] = None, id_: Optional[str] = None, /) -> None:
        pass
