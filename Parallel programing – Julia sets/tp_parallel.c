#include <stdio.h>
#include <stdlib.h>
#include "gmp.h"
#include "mpi.h"

float scale_value(float old_value, float old_max, float old_min, float new_max,
		float new_min) {
	return ((old_value - old_min) / (old_max - old_min)) * (new_max - new_min)
			+ new_min;
}

int main(int argc, char **argv) {

	int my_rank;
	int p; //processors
	int dest = 0; //destination
	int source;
	int height = 10000;
	int width = 10000;
	double elapsed_time = 0;

	float R = 4; //escape radius

	float cx = -0.8;
	float cy = 0.156;

	//initialize MPI
	MPI_Status status;
	MPI_Init(&argc, &argv);
	MPI_Barrier(MPI_COMM_WORLD);
	elapsed_time = -1 * MPI_Wtime();
	MPI_Comm_rank(MPI_COMM_WORLD, &my_rank);
	MPI_Comm_size(MPI_COMM_WORLD, &p);

	//find starting i and n_p
	int i_start;
	int n_p;
	n_p = height / p;

	if (my_rank < height % p) {
		n_p = n_p + 1;
	}

	i_start = my_rank * (height / p);

	if (my_rank < height % p) {
		i_start = i_start + my_rank;
	} else {
		i_start = i_start + (height % p);
	}

	//create an output file for each proc
	char f_name[12];
	snprintf(f_name, 12, "%d_out.text", my_rank);
	FILE *f = fopen(f_name, "w");

	//this strategy just splits rows into chunks and gives a chunk into each processor
	//each chunk has continuous rows

	for (int i = i_start; i < n_p; i++) {
		for (int j = 0; j < width; j++) {
			int ycord = height - 1 - i;
			//put 0,0 at center
			int y = ycord - height / 2;
			int x = j - width / 2;

			//scale coordinates to be between -R and R
			float zx = scale_value(x, width / 2, -1 * width / 2, R, -1 * R);
			float zy = scale_value(y, height / 2, -1 * height / 2, R, -1 * R);

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

}
