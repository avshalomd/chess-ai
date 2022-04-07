import logging
from copy import deepcopy

import chess
from mcts import mcts

import configs


class Action:
    def __init__(self, player: int, move: str):
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


class ChessState():
    def __init__(self):
        self.board = chess.Board()
        self.current_player = 1  # (1) = White, (-1) = Black

    def getCurrentPlayer(self):
        return self.current_player

    def getPossibleActions(self):
        possible_actions = []
        for move in self.board.legal_moves:
            possible_actions.append(Action(player=self.current_player, move=str(move)))
        return possible_actions

    def takeAction(self, action: Action):
        new_state = deepcopy(self)
        new_state.board.push_uci(action.move)
        # print('----------------')
        # print(new_state.board)
        new_state.current_player = self.current_player * -1
        return new_state

    def isTerminal(self):
        return self.board.is_checkmate() or self.board.legal_moves.count() == 0

    def getReward(self):
        if self.board.is_checkmate():
            logging.debug('got to checkmate state')
            return configs.HIGH_REWARD
        if self.board.legal_moves.count() == 0:
            logging.debug('got to pat state')
            return configs.LOW_REWARD
        return False


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    initialState = ChessState()
    searcher = mcts(timeLimit=1000000)
    next_action = searcher.search(initialState=initialState)
    print(next_action)
