/**
 * This code solves the n-queens problem for a user specified n. It uses the min-conflicts algorithm.
 * type javac NQueen.java to compile
 * type java Nqueen [N] to run
 */

import java.util.ArrayList;
import java.util.List;
import java.util.Random;
import java.io.PrintWriter;
import java.io.File;

public class NQueen {
	public static int[] genState(int N) {
		Random rd = new Random();
		int[] state = new int[N];
		for (int i = 0; i < state.length; i++) {
			state[i] = rd.nextInt(N);
		}
		return state;
	}

	public static boolean allSafe(int[] state) {
		// checks if all queens are safe in given state

		// check all queens for conflict
		for (int q = 0; q < state.length; q++) {
			for (int i = 0; i < state.length; i++) {
				if (q != i) {
					// check same row conflict
					if (state[i] == state[q]) {
						return false;
					}

					// check diagonal conflict
					if (state[i] == state[q] + (i - q)) {
						return false;
					}

					if (state[i] == state[q] - (i - q)) {
						return false;
					}
				}
			}
		}
		return true;
	}

	public static int countConflict(int q, int[] state) {
		// counts the number of conflicts that occurs at a given state between a given
		// queen and all other queens

		int conflict = 0;
		for (int i = 0; i < state.length; i++) {
			if (q != i) {
				// check same row conflict
				if (state[i] == state[q]) {
					conflict++;
				}

				// check diagonal conflict
				if (state[i] == state[q] + (i - q)) {
					conflict++;
				}

				if (state[i] == state[q] - (i - q)) {
					conflict++;
				}
			}
		}

		return conflict;
	}

	public static boolean minConflict(int[] currState, int N, int maxSteps) {
		/*
		 * min conflict algorithm implementation input: current_state - a list of the
		 * which row each queen is sitting in example: current_state[i]= n the queen in
		 * ith column is in the nth row N - n in n-queen
		 */
		boolean successful = true;
		Random rd = new Random();
		int forbidCount = 3;// max number of steps that a var should be in the forbidden queue forbidden
		int forbidSize = (int) (N * 0.1);// max size of forbidden queue
		List<Integer> forbiden = new ArrayList<Integer>();
		while (allSafe(currState) == false && maxSteps > 0) {
			int var = rd.nextInt(N);
			int minCon = N + 1;

			// System.out.println(forbidSize);
			List<Integer> minVal = new ArrayList<Integer>();
			if (forbiden.contains(var) == false) {// only select var if not in forbidden queue

				int newVal = currState[var];

				// change var to value that minimizes conflict
				for (int val = 0; val < N; val++) {
					currState[var] = val;

					// count how many conflicts this new state will produce
					int newCon = countConflict(var, currState);

					if (newCon < minCon) {
						minVal.clear();
						newVal = val;
						minVal.add(val);
						minCon = newCon;
					} else if (newCon == minCon) {
						minVal.add(val);// add all position that tie for min conflict
					}
				}

				currState[var] = minVal.get(rd.nextInt(minVal.size()));
				maxSteps--;

				// add var to forbidden queue
				if (minCon == 0) {
					forbiden.add(var);
				}
			}
			if (forbiden.size() > forbidSize || forbidCount < 1) {
				// release a var from forbidden queue if size if too large or time expired
				forbiden.remove(0);
				forbidCount = 10;
			}
			forbidCount--;
			
		}

		if (maxSteps < 1) {
			successful = false;
		}

		return successful;
	}

	public static void printBoard(int[] board) {
		for (int i = 0; i < board.length; i++) {
			for (int j = 0; j < board.length; j++) {
				if (board[j] == i) {
					System.out.print("Q ");
				} else {
					System.out.print("_ ");
				}

			}
			System.out.println(" ");
		}
	}

	public static void main(String[] args) {

		int N = 10;

		if (args.length > 0) {
			N = Integer.parseInt(args[0]);
			System.out.print("Running n-queens with n = ");
			System.out.println(N);
		} else {
			System.out.println("No n entered using n=10.");
		}

		int[] state;

		boolean successful = false;
		state = genState(N);
		// retry min conflicts with new init state until succes
		while (successful == false) {
			state = genState(N);
			successful = minConflict(state, N, 10000);

			if (successful) {
				System.out.println("Successful");
			} else {
				System.out.println("Failed, re-initializing");
			}
		}

		// don't bother printing large board
		if (N < 52) {

			printBoard(state);
		}

		
		for (int i = 0; i < state.length; i++) {

			String out = "The queen in column " + Integer.toString(i+1)+" is placed in row "+ Integer.toString(state[i] + 1);
			System.out.println(out);

		}
		

	}
}
