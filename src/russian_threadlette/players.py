import random
import threading
from threading import Barrier, Event, ExceptHookArgs, Thread


class BulletCaughtException(BaseException):
    pass


_player_died: Event = Event()


def player_death_hook(args: ExceptHookArgs) -> None:
    assert args.exc_type is BulletCaughtException
    assert args.thread is not None
    _player_died.set()
    print(f"{args.thread.name} has died")


threading.excepthook = player_death_hook


class Player(Thread):
    def __init__(self, name: str, chance: float, game_started: Barrier) -> None:
        super().__init__(name=f"Player {name}")
        assert chance < 1.0 and chance > 0.0
        self._chance = chance
        self._game_started = game_started
        self._rounds: int = 0

    def run(self) -> None:
        self._game_started.wait()
        while not _player_died.is_set():
            self._rounds += 1
            if random.random() < self._chance:
                raise BulletCaughtException()

    @property
    def rounds(self) -> int:
        return self._rounds
