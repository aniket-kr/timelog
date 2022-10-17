import dataclasses
from typing import Dict, Generic, Iterator, Optional, Type

import models
from project import CacheManager
from project.cache_manager import TModel
from project.errors import UnregisteredSourceError
from services import db


@dataclasses.dataclass
class CacheNode(Generic[TModel]):
    model: Type[TModel]
    source: str
    is_stale: bool = True
    _raw_data: Dict[str, TModel] = dataclasses.field(default_factory=dict, init=False)

    def refresh(self, cache: CacheManager) -> None:
        docs_ref = db.collection(self.source).stream()
        self._raw_data.clear()
        for doc_ref in docs_ref:
            self._raw_data[doc_ref.id] = self.model.parse(doc_ref.to_dict(), cache)
        self.is_stale = False

    def data(self, cache: CacheManager) -> Dict[str, TModel]:
        if self.is_stale:
            self.refresh(cache)
        return self._raw_data


class PersistentCache(CacheManager):
    def __init__(self, project_id: str):
        super().__init__(project_id)
        self._cache: Dict[str, CacheNode] = {}

    def register(self, model: Type[models.BaseModel]) -> None:
        source = '/'.join(['projects', self.project_id, model.collection_name()])
        node = CacheNode(model=model, source=source)
        self._cache[model.collection_name()] = node

    def _get_node(self, model: Type[TModel]) -> CacheNode[TModel]:
        node = self._cache.get(model.collection_name())
        if node is None:
            raise UnregisteredSourceError(model)
        return node

    def get(self, model: Type[TModel], id_: str) -> TModel:
        node = self._get_node(model)
        return node.data(self)[id_]

    def collection(self, model: Type[TModel]) -> Iterator[TModel]:
        node = self._get_node(model)
        return iter(node.data(self).values())

    def clear(self, model: Optional[Type[TModel]] = None, id_: Optional[str] = None, /) -> None:
        match (model is None, id_ is None):
            case True, True:
                for node in self._cache.values():
                    node.is_stale = True

            case False, _:
                try:
                    self._cache[model.collection_name()].is_stale = True
                except KeyError:
                    pass
