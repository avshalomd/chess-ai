import logging
from copy import deepcopy

import chess
from mcts import mcts

import configs
from enums.EPlayer import EPlayer


class Action:
    def __init__(self, player: EPlayer, move: str):
        self.player = player
        self.move = move

    def __str__(self):
        return self.move

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        return self.__class__ == other.__class__ and self.move == other.move and self.player == other.player

    def __hash__(self):
        return hash((self.move, self.player))


def get_starting_player(starting_fen) -> EPlayer:
    if (starting_fen is None) or (starting_fen == ''):
        return EPlayer.WHITE
    else:
        if starting_fen.split()[1] == 'w':
            return EPlayer.WHITE
        elif starting_fen.split()[1] == 'b':
            return EPlayer.BLACK
        else:
            logging.error(f'Unrecognized starter player: {starting_fen.split()[1]}')


class ChessState:
    def __init__(self, starting_fen: str = None):
        self.board = chess.Board() if (starting_fen is None) or (starting_fen == '') else chess.Board(fen=starting_fen)
        self.current_player = get_starting_player(starting_fen=starting_fen)

    def getCurrentPlayer(self):
        return self.current_player

    def getPossibleActions(self):
        possible_actions = []
        for move in self.board.legal_moves:
            possible_actions.append(Action(player=self.current_player, move=str(move)))
        return possible_actions

    def takeAction(self, action: Action):
        new_state = deepcopy(self)
        new_state.current_player = EPlayer(self.current_player.value * -1)
        new_state.board.push_uci(action.move)
        return new_state

    def isTerminal(self):
        return self.board.is_game_over()

    def getReward(self):
        if self.board.is_checkmate():
            logging.debug(f'{EPlayer(self.current_player.value * -1).name} player got to checkmate state')
            return configs.HIGH_REWARD
        if self.board.can_claim_draw():
            logging.debug(f'{EPlayer(self.current_player.value * -1).name} player got to draw state')
            return configs.LOW_REWARD
        return False


if __name__ == "__main__":
    # logging.basicConfig(level=logging.DEBUG)
    initialState = ChessState()
    searcher = mcts(timeLimit=10 * 1000)
    next_action = searcher.search(initialState=initialState)
    print(next_action)
