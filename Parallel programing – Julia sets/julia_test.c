/*
 -------------------------------------
 File:    julia_test.c
 Project: TP_serial
 file description
 -------------------------------------
 Author:  Amardeep Sarang
 ID:      160112080
 Email:   sara2080@mylaurier.ca
 Version  2019-11-18
 -------------------------------------
 */

#include <stdio.h>
#include <stdlib.h>

float scale_value(float old_value, float old_max, float old_min, float new_max,
		float new_min) {
	return ((old_value - old_min) / (old_max - old_min)) * (new_max - new_min)
			+ new_min;
}

int main() {
	/*
	 ---------------------
	 Changeable parameters
	 --------- -----------
	 */
	//==============================
	float WIDTH = 5000;
	float HEIGHT = 5000;
	float R = 4; //escape radius

	float cx = 0.3;
	float cy = -0.4;
	//==============================
	FILE *f = fopen("julia_out.txt", "w");
	for (int i = 0; i < HEIGHT; i++) {
		for (int j = 0; j < WIDTH; j++) {
			int ycord = HEIGHT - 1 - i;
			//put 0,0 at center
			int y = ycord - HEIGHT / 2;
			int x = j - WIDTH / 2;

			//scale coordinates to be between -R and R
			float zx = scale_value(x, WIDTH / 2, -1 * WIDTH / 2, R, -1 * R);
			float zy = scale_value(y, HEIGHT / 2, -1 * HEIGHT / 2, R, -1 * R);

			int iteration = 0;
			int max_iteration = 50;

			while ((zx * zx + zy * zy < R * R) && (iteration < max_iteration)) {
				float xtemp = zx * zx - zy * zy;
				zy = 2 * zx * zy + cy;
				zx = xtemp + cx;

				iteration = iteration + 1;
			}
			fprintf(f, "%d %d %d\n", i, j, iteration);
		}
	}
	printf("Done");
	fclose(f);
}
