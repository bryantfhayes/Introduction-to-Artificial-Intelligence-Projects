/*
 * MinimaxPlayer.cpp
 *
 *  Created on: Apr 17, 2015
 *      Author: wong
 */
#include <iostream>
#include <assert.h>
#include "MinimaxPlayer.h"
#include <algorithm>

using std::vector;

#define TRUE 1
#define FALSE 0


MinimaxPlayer::MinimaxPlayer(char symb) :
		Player(symb) {

}

MinimaxPlayer::~MinimaxPlayer() {

}

// Check every combination of col and row and see if there are
// any legal moves. If a move is legal add it to the array of successors and
// increment counter.
MinimaxPlayer::OthelloNode* MinimaxPlayer::get_successors(OthelloNode* successors, OthelloBoard* current_board, int& num_of_successors) {
	int row, col = 0;
	for(row = 0; row < current_board->get_num_rows(); row++) {
		for(col = 0; col < current_board->get_num_cols(); col++) {
			if(current_board->is_legal_move(col, row, current_symbol)) {
				successors[num_of_successors].board = new OthelloBoard(*(current_board));
				successors[num_of_successors].board->play_move(col, row, current_symbol);
				successors[num_of_successors].column = col;
				successors[num_of_successors].row = row;
				successors[num_of_successors].value = -1;
				num_of_successors++;
			}
		}
	}
	return successors;
}

// MIN-VALUE(state)
// 1. Initialize an array to hold all successor boards
// 2. Make current player = P2
// 3. Generate Successor array
// 4. For each successor run max_value
// 5. Of all possible boards choose the min value and return that value
int MinimaxPlayer::min_value(OthelloBoard* b) {
	//std::cout << "LOOP2\n";
	if(terminal_test(b)) {
		return utility(b);
	}
	int value = 100;
	int num_of_successors = 0;
	int i = 0;
	MinimaxPlayer::OthelloNode successors[(b->get_num_cols() * b->get_num_rows()) - 4];

	current_symbol = b->get_p2_symbol();
	MinimaxPlayer::OthelloNode* successor_list = get_successors(successors, b, num_of_successors);

	for(i = 0; i < num_of_successors; i++) {
		value = std::min(value, max_value(successor_list[i].board));
	}

	return value;
}

// MAX-VALUE(state)
// 1. Initialize an array to hold all successor boards
// 2. Make current player = P1
// 3. Generate Successor array
// 4. For each successor run min_value
// 5. Of all possible boards choose the max value and return that value
int MinimaxPlayer::max_value(OthelloBoard* b) {
	if(terminal_test(b)) {
		return utility(b);
	}
	int value = -100;
	int num_of_successors = 0;
	int i = 0;
	MinimaxPlayer::OthelloNode successors[(b->get_num_cols() * b->get_num_rows()) - 4];

	current_symbol = b->get_p1_symbol();
	MinimaxPlayer::OthelloNode* successor_list = get_successors(successors, b, num_of_successors);

	for(i = 0; i < num_of_successors; i++) {
		value = std::max(value, min_value(successor_list[i].board));
	}

	return value;
}

// Terminal is reached when there are no more moves left for either player to make.
bool MinimaxPlayer::terminal_test(OthelloBoard* b) {
	if( !(b->has_legal_moves_remaining(b->get_p1_symbol())) && !(b->has_legal_moves_remaining(b->get_p2_symbol())) ) {
		// At a leaf node
		return TRUE;
	} else {
		// Not at a leaf node
		return FALSE;
	}
}

// Utility is based on the score differential. Positive means there are more P1
// pieces, whereas negative means more P2 pieces.
int MinimaxPlayer::utility(OthelloBoard* b) {
	int value = b->count_score(b->get_p1_symbol()) - b->count_score(b->get_p2_symbol());
	return value;
}

// 1. Determine if this is player 1 or 2 going.
// 2. Find each board obtainable by one move.
// 3. For each board state run min_value().
// 4. Choose the move that goes to the MIN/MAX value branch.
//    This depends on who is MIN and who is MAX. Given in step 1.
void MinimaxPlayer::get_move(OthelloBoard* b, int& col, int& row) {
	char player;
	int maxvalue = -100;
	int minvalue = 100;
	int best_board = 0;
	int i = 0;
	int num_of_successors = 0;

	current_symbol = symbol;

	MinimaxPlayer::OthelloNode successors[(b->get_num_cols() * b->get_num_rows()) - 4];

	MinimaxPlayer::OthelloNode* successor_list = get_successors(successors, b, num_of_successors);

	printf("There were %d possible moves\n", num_of_successors);

	if (current_symbol == b->get_p1_symbol()) {
		current_symbol = b->get_p2_symbol();
	} else {
		current_symbol = b->get_p1_symbol();
	}

	for(i = 0; i < num_of_successors; i++){

		// IF: Player #1
		if(b->get_p1_symbol() == symbol) {
			int temp_value = min_value(successor_list[i].board);
			if (temp_value > maxvalue){
				maxvalue = temp_value;
				best_board = i;
			}
		// ELSE-IF: Player #2
		} else {
			//std::cout << "LOOP1\n";
			int temp_value = max_value(successor_list[i].board);
			if (temp_value < minvalue){
				minvalue = temp_value;
				best_board = i;
			}
		}
	}

	col = successor_list[best_board].column;
	row = successor_list[best_board].row;
}

MinimaxPlayer* MinimaxPlayer::clone() {
	MinimaxPlayer* result = new MinimaxPlayer(symbol);
	return result;
}
