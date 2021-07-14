import importlib
import inspect
from typing import Any, Dict, Generic, Type, TypeVar, Union

import entrypoints
import typing_inspect

from datahub import __package_name__
from datahub.configuration.common import ConfigurationError

T = TypeVar("T")


def import_key(key: str) -> Any:
    assert "." in key, "import key must contain a ."
    module_name, item_name = key.rsplit(".", 1)
    item = getattr(importlib.import_module(module_name), item_name)
    return item


class Registry(Generic[T]):
    def __init__(self):
        self._mapping: Dict[str, Union[Type[T], Exception]] = {}

    def _get_registered_type(self) -> Type[T]:
        cls = typing_inspect.get_generic_type(self)
        tp = typing_inspect.get_args(cls)[0]
        return tp

    def _check_cls(self, cls: Type[T]) -> None:
        if inspect.isabstract(cls):
            raise ValueError(
                f"cannot register an abstract type in the registry; got {cls}"
            )
        super_cls = self._get_registered_type()
        if not issubclass(cls, super_cls):
            raise ValueError(f"must be derived from {super_cls}; got {cls}")

    def _register(self, key: str, tp: Union[Type[T], Exception]) -> None:
        if key in self._mapping:
            raise KeyError(f"key already in use - {key}")
        if key.find(".") >= 0:
            raise KeyError(f"key cannot contain '.' - {key}")
        self._mapping[key] = tp

    def register(self, key: str, cls: Type[T]) -> None:
        self._check_cls(cls)
        self._register(key, cls)

    def register_disabled(self, key: str, reason: Exception) -> None:
        self._register(key, reason)

    def is_enabled(self, key: str) -> bool:
        tp = self._mapping[key]
        return not isinstance(tp, Exception)

    def load(self, entry_point_key: str) -> None:
        entry_point: entrypoints.EntryPoint
        for entry_point in entrypoints.get_group_all(entry_point_key):
            name = entry_point.name

            try:
                plugin_class = entry_point.load()
            except ModuleNotFoundError as e:
                self.register_disabled(name, e)
                continue

            self.register(name, plugin_class)

    @property
    def mapping(self):
        return self._mapping

    def get(self, key: str) -> Type[T]:
        if key.find(".") >= 0:
            # If the key contains a dot, we treat it as a import path and attempt
            # to load it dynamically.
            MyClass = import_key(key)
            self._check_cls(MyClass)
            return MyClass

        if key not in self._mapping:
            raise KeyError(f"Did not find a registered class for {key}")
        tp = self._mapping[key]
        if isinstance(tp, Exception):
            raise ConfigurationError(
                f"{key} is disabled; try running: pip install '{__package_name__}[{key}]'"
            ) from tp
        else:
            # If it's not an exception, then it's a registered type.
            return tp

    def summary(self, verbose=True, col_width=15, verbose_col_width=20):
        lines = []
        for key in sorted(self._mapping.keys()):
            line = f"{key}"
            if not self.is_enabled(key):
                # Plugin is disabled.
                line += " " * (col_width - len(key))

                details = "(disabled)"
                if verbose:
                    details += " " * (verbose_col_width - len(details))
                    details += repr(self._mapping[key])
                line += details
            elif verbose:
                # Plugin is enabled.
                line += " " * (col_width - len(key))
                line += self.get(key).__name__

            lines.append(line)

        return "\n".join(lines)
