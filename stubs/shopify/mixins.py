from typing import Any, Mapping


class Metafields:
    ...


class Events:
    ...


class Countable:
    @classmethod
    def count(cls, _options: None = None, **kwargs: Mapping[str, Any]) -> int:
        ...
