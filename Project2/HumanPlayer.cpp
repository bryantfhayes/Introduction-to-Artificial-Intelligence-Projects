#include <iostream>
#include "HumanPlayer.h"
#include <time.h>       /* time */

HumanPlayer::HumanPlayer(char symb) : Player(symb) {

}

HumanPlayer::~HumanPlayer() {

}

void HumanPlayer::get_move(OthelloBoard* b, int& col, int& row) {
    row = rand() % b->get_num_rows();
    col = rand() % b->get_num_cols();
    printf("%d\n", col);
    printf("%d\n", row);
    //std::cout << "Enter col: ";
    //std::cin >> col;
    //std::cout << "Enter row: ";
    //std::cin >> row;

}

HumanPlayer* HumanPlayer::clone() {
	HumanPlayer *result = new HumanPlayer(symbol);
	return result;
}
