from abc import ABCMeta
from typing import Any


class Singleton(ABCMeta, type):
    _instances = {}

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        if self not in self._instances:
            self._instances[self] = super().__call__(*args, **kwargs)
        return self._instances[self]


class SharedServer(metaclass=Singleton):
    pass


class SharedSupvisor(metaclass=Singleton):
    pass


if __name__ == "__main__":
    server1 = SharedServer()
    server2 = SharedServer()
    assert server1 is server2

    supvisor1 = SharedSupvisor()
    supvisor2 = SharedSupvisor()
    assert supvisor1 is supvisor2

    assert SharedServer._instances is SharedSupvisor._instances
    assert len(SharedServer._instances) == 2
