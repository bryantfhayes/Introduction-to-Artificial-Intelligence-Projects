/*
 * MinimaxPlayer.cpp
 *
 *  Created on: Apr 17, 2015
 *      Author: wong
 */
#include <iostream>
#include <assert.h>
#include "MinimaxPlayer.h"

using std::vector;

MinimaxPlayer::MinimaxPlayer(char symb) :
		Player(symb) {

}

MinimaxPlayer::~MinimaxPlayer() {

}

void MinimaxPlayer::get_move(OthelloBoard* b, int& col, int& row) {
    int i, j = 0;
	int c, r = 0;

	for(c = 0; c < b->get_num_cols(); c++){
		for(r = 0; r < b->get_num_rows(); r++){
			if(b->is_legal_move(c, r, symbol)){
				col = c;
				row = r;
				return;
			}
		}
	}
}

MinimaxPlayer* MinimaxPlayer::clone() {
	MinimaxPlayer* result = new MinimaxPlayer(symbol);
	return result;
}
