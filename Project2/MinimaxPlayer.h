/*
 * MinimaxPlayer.h
 *
 *  Created on: Apr 17, 2015
 *      Author: wong
 */

#ifndef MINIMAXPLAYER_H
#define MINIMAXPLAYER_H

#include "OthelloBoard.h"
#include "Player.h"
#include <vector>

/**
 * This class represents an AI player that uses the Minimax algorithm to play the game
 * intelligently.
 */
class MinimaxPlayer : public Player {
public:

	struct OthelloNode {
		int column;
		int row;
		int value;
		OthelloBoard* board;
	};

	char current_symbol;

	/**
	 * @param symb This is the symbol for the minimax player's pieces
	 */
	MinimaxPlayer(char symb);

	/**
	 * Destructor
	 */
	virtual ~MinimaxPlayer();

	/**
	 * @param b The board object for the current state of the board
	 * @param col Holds the return value for the column of the move
	 * @param row Holds the return value for the row of the move
	 */
    void get_move(OthelloBoard* b, int& col, int& row);

    /**
     * @return A copy of the MinimaxPlayer object
     * This is a virtual copy constructor
     */
    MinimaxPlayer* clone();

private:
	OthelloNode* get_successors(OthelloNode* successors, OthelloBoard* current_board, int& num_of_successors);
	int max_value(OthelloBoard* b, int depth);
	int min_value(OthelloBoard* b, int depth);
	bool terminal_test(OthelloBoard* b, int depth);
	int utility(OthelloBoard* b);
};


#endif
