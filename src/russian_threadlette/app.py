import sys
import time
from threading import Barrier

from .names import PLAYER_NAMES
from .players import Player


def players_connected() -> None:
    print("All players have connected")


def main(args: list[str] | None = None) -> int:
    args = args or sys.argv[1:]
    if len(args) != 2:
        raise ValueError("Missing required args: (n_players, chance)")

    n_players: int = int(args[0])
    chance: float = float(args[1])

    if n_players > (max_players := len(PLAYER_NAMES)):
        raise ValueError(f"Max players allowed is {max_players}")

    game_started = Barrier(n_players, action=players_connected)
    players: list[Player] = [
        Player(PLAYER_NAMES[i], chance, game_started) for i in range(n_players)
    ]

    game_start = time.monotonic_ns()
    for player in players:
        player.start()
    for player in players:
        player.join()
    game_end = time.monotonic_ns()

    rounds_played: int = sum((player.rounds for player in players))
    for player in players:
        play_percentage = (player.rounds / rounds_played) * 100
        print(f"{player.name} played {player.rounds} rounds ({play_percentage:.01f}%).")

    game_duration_s = (game_end - game_start) * 1.0e-9
    print(f"Game duration: {game_duration_s:.04f}s")
    print(f"Total rounds played: {rounds_played}")
    rounds_per_s = rounds_played / game_duration_s
    print(f"Average rounds per second: {rounds_per_s:.04f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
