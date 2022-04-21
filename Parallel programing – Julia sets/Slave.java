public class Slave implements Runnable {


    private Master master;
    private int maxIterations;
    private int threadNumber;
    private double[] z;

    public Slave(Master master, int maxIterations, int threadNumber, double[] z) {
        this.master = master;
        this.maxIterations = maxIterations;
        this.threadNumber = threadNumber;
        this.z = z;
    }

    @Override
    public void run() {

        int[] point = master.getNextPoint(threadNumber);

        while (point != null) {

            double real = point[0];
            double imag = point[1];
            double magnitude = real * real + imag * imag;

            int iterations = 0;

            while (iterations < maxIterations && magnitude < 4.0) {

                double tempReal = real * real - imag * imag;
                imag = 2 * real * imag;
                real = tempReal;

                real += z[0];
                imag += z[1];

                magnitude = real * real + imag * imag;
                iterations ++;
            }

            master.setValue(iterations, point[0], point[1]);
            point = master.getNextPoint(threadNumber);
        }

        master.updateFinishedCount();
        //System.out.println("Thread " + threadNumber + " has finished");
    }
}
