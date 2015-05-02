#include <iostream>
#include "HumanPlayer.h"
#include <time.h>       /* time */

HumanPlayer::HumanPlayer(char symb) : Player(symb) {

}

HumanPlayer::~HumanPlayer() {

}

void HumanPlayer::get_move(OthelloBoard* b, int& col, int& row) {
    /* UNCOMMENT THIS TO MAKE 'HUMAN' AUTOMATICALLY PICK A RANDOM MOVE */
    row = rand() % b->get_num_rows();
    col = rand() % b->get_num_cols();
    printf("%d\n", col);
    printf("%d\n", row);

    /* COMMENT THIS TO MAKE 'HUMAN' AUTOMATICALLY PICK A RANDOM MOVE */
    // std::cout << "Enter col: ";
    // std::cin >> col;
    // std::cout << "Enter row: ";
    // std::cin >> row;
}

HumanPlayer* HumanPlayer::clone() {
	HumanPlayer *result = new HumanPlayer(symbol);
	return result;
}
