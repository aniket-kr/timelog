import dataclasses
from typing import Any, ClassVar, Dict, Type

import project
from models import BaseModel
from models.base_model import T


@dataclasses.dataclass(frozen=True)
class Department(BaseModel):
    COLLECTION: ClassVar[str] = 'departments'
    code: str
    name: str

    @classmethod
    def parse(cls: Type[T], db_dict: Dict[str, Any], cache: project.CacheManager) -> T:
        return Department(
            code=str(db_dict['code']),
            name=str(db_dict['name']),
        )
