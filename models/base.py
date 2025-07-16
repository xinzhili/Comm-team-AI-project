from typing import Any

from  sqlalchemy import MetaData
from sqlalchemy.orm import declarative_base

metadata = MetaData(schema='testing')
Base: Any = declarative_base(metadata=metadata)