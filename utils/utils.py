import logging
import re


def is_valid_fen(fen: str) -> bool:
    """
        check if input string is a valid FEN [https://en.wikipedia.org/wiki/Forsyth%E2%80%93Edwards_Notation]
    """
    regex_match = re.match(
        '\s*^(((?:[rnbqkpRNBQKP1-8]+\/){7})[rnbqkpRNBQKP1-8]+)\s([b|w])\s(-|[K|Q|k|q]{1,4})\s(-|[a-h][1-8])\s(\d+\s\d+)$',
        fen)
    if regex_match:
        regex_list = regex_match.groups()
        fen = regex_list[0].split("/")
        if len(fen) != 8:
            logging.info(f"expected 8 rows in position part of fen: {repr(fen)}")
            return False

        for fenPart in fen:
            field_sum = 0
            previous_was_digit, previous_was_piece = False, False

            for c in fenPart:
                if c in ["1", "2", "3", "4", "5", "6", "7", "8"]:
                    if previous_was_digit:
                        logging.info(f"two subsequent digits in position part of fen: {repr(fen)}")
                        return False
                    field_sum += int(c)
                    previous_was_digit = True
                    previous_was_piece = False
                elif c == "~":
                    if not previous_was_piece:
                        logging.info(f"~ not after piece in position part of fen: {repr(fen)}")
                        return False
                    previous_was_digit, previous_was_piece = False, False
                elif c.lower() in ["p", "n", "b", "r", "q", "k"]:
                    field_sum += 1
                    previous_was_digit = False
                    previous_was_piece = True
                else:
                    logging.info(f"invalid character in position part of fen: {repr(fen)}")
                    return False

            if field_sum != 8:
                logging.info(f"expected 8 columns per row in position part of fen: {repr(fen)}")
                return False

    else:
        logging.info("fen doesn`t match follow this example: rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1 ")
        return False
    return True


if __name__ == '__main__':
    print(is_valid_fen('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'))
