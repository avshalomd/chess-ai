import logging

from mcts import mcts

import configs
from ChessState import ChessState, Action
from enums.EPlayer import EPlayer
from enums.EAIMode import EAIMode
from utils.validation import is_valid_fen


def get_player_color() -> EPlayer:
    while True:
        data = input("Choose player color (B/W): ")
        if data.lower() not in ('b', 'w'):
            print("Unsupported player color.")
        else:
            if data.lower() == 'b':
                return EPlayer.BLACK
            else:
                return EPlayer.WHITE


def get_game_initial_state() -> str:
    while True:
        data = input("Choose game initial state:\n"
                     " (1) - GAME_STATE_EASY_WHITE_WIN\n"
                     " (C) - Custom state (FEN encoded)\n"
                     " (ENTER) - New Game\n")

        if data.lower() == 'c':
            while True:
                initial_state_string = input("Insert legal FEN encoded state: ")
                if is_valid_fen(initial_state_string):
                    return initial_state_string
        elif data == '1':
            return configs.GAME_STATE_EASY_WHITE_WIN
        elif data == '':
            return ''
        else:
            raise ValueError('Unsupported game initial state.')


class ChessGame:
    def __init__(self, ai_mode: EAIMode = EAIMode.NORMAL):
        self.human_player_color = get_player_color()
        self.game_initial_state = get_game_initial_state()
        self.current_game_state = ChessState(starting_fen=self.game_initial_state)
        self.ai_move_time_limit_seconds = ai_mode.value

    def play(self):
        while not self.current_game_state.board.is_game_over():
            self._print_game_state()
            self._make_move()
        self._print_game_over_state()

    def _make_move(self):
        if self.current_game_state.current_player == self.human_player_color:
            action = self._get_human_action()
        else:
            print('Please wait while the AI is thinking...\n')
            action = mcts(timeLimit=self.ai_move_time_limit_seconds * 1000).search(self.current_game_state)

        self.current_game_state = self.current_game_state.takeAction(action)

    def _print_board(self):
        print('---------------')
        print(self.current_game_state.board)
        print('---------------')

    def _print_game_state(self):
        print(f"\nIt's {self.current_game_state.current_player.name}'s turn")
        self._print_board()

    def _print_game_over_state(self):
        if self.current_game_state.board.is_checkmate():
            print(f'{EPlayer(self.current_game_state.current_player.value * -1).name} has won by checkmate')
        elif self.current_game_state.board.can_claim_draw():
            print(f"It's a draw")
        else:
            print("what just happened?")
        self._print_board()

    def _get_human_action(self) -> Action:
        while True:
            action = input("Make a move: ")
            legal_actions = [move.uci() for move in list(self.current_game_state.board.legal_moves)]
            if action not in legal_actions:
                print(f"Illegal action! (HINT: Choose from {legal_actions})")
                continue
            return Action(player=self.human_player_color, move=action)


# TODO: README
# TODO: game visualization
# TODO: collect and display AI move statistics
# TODO: experiment with different policies
# TODO: save MCTS game tree and use previous knowledge (statistics) as the game evolves (instead of reset it every turn)
# TODO: add progress bar (or any other indicator) for AI thinking time
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    ChessGame(ai_mode=EAIMode.NORMAL).play()
