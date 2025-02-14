from __future__ import annotations

import pathlib
import pickle
import uuid
from typing import Any
from typing import NamedTuple
from typing import TypeVar

T = TypeVar('T')


class Identifier(NamedTuple):
    """Object identifier.

    Attributes:
        cache_dir: Object directory.
        obj_id: Object ID.
    """

    cache_dir: pathlib.Path
    obj_id: uuid.UUID

    def path(self) -> pathlib.Path:
        """Get path to the object."""
        return self.cache_dir / str(self.obj_id)


class PickleFileTransformer:
    """Pickle file object transformer.

    Args:
        cache_dir: Directory to store pickled objects in.
    """

    def __init__(
        self,
        cache_dir: pathlib.Path | str,
    ) -> None:
        self.cache_dir = pathlib.Path(cache_dir).resolve()

    def is_identifier(self, obj: Any) -> bool:
        """Check if the object is an identifier instance."""
        return isinstance(obj, Identifier)

    def transform(self, obj: T) -> Identifier:
        """Transform the object into an identifier.

        Args:
            obj: Object to transform.

        Returns:
            Identifier object that can be used to resolve `obj`.
        """
        identifier = Identifier(self.cache_dir, uuid.uuid4())
        filepath = identifier.path()
        filepath.parent.mkdir(parents=True, exist_ok=True)

        with open(filepath, 'wb', buffering=0) as f:
            pickle.dump(obj, f)

        return identifier

    def resolve(self, identifier: Identifier) -> Any:
        """Resolve an object from an identifier.

        Args:
            identifier: Identifier to an object.

        Returns:
            The resolved object.
        """
        filepath = identifier.path()
        with open(filepath, 'rb') as f:
            obj = pickle.load(f)
        filepath.unlink()
        return obj
