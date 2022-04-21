import java.sql.Time;
import java.text.DateFormat;
import java.text.SimpleDateFormat;
import java.time.Duration;
import java.time.Instant;

public class Master {

    private int x = 5000;
    private int y = 5000;
    private int xOffset = x / 2;
    private int yOffset = y / 2;
    private int[][] points;

    private double[] z = new double[] {0.0, 0.0};

    private int lastAssignedX = 0;
    private int lastAssignedY = 0;
    private int assignedCount = 0;

    private int[] threadRequestCount;
    private Thread[] threads;
    private int finishedCount = 0;

    private final int THREAD_COUNT = 10;
    private final int MAX_ITERATIONS = 1000;

    private Instant startingTime;

    public static void main(String... arags) {

        new Master();
    }

    private Master() {

        points = new int[x][y];
        threadRequestCount = new int[THREAD_COUNT];
        threads = new Thread[THREAD_COUNT];


        startThreads();
        startingTime = Instant.now();
    }

    private void startThreads() {

        for (int i = 0; i < THREAD_COUNT; i++) {

            Thread thread = new Thread(new Slave(this, MAX_ITERATIONS, i, z));
            threads[i] = thread;
            thread.start();
        }
    }

    public synchronized void updateFinishedCount() {

        finishedCount ++;

        if (finishedCount == THREAD_COUNT) {

            Instant finishTime = Instant.now();

            System.out.println("Thread #\t\t\tRequests");
            for (int i = 0; i < THREAD_COUNT; i++) {

                System.out.println(i + "\t\t\t\t" + threadRequestCount[i]);
            }

            System.out.println("Time to complete: " + Duration.between(startingTime, finishTime));
        }
    }

    public synchronized void setValue(int value, int x, int y) {

        points[x + xOffset][y + yOffset] = value;
        return;
    }

    public synchronized int[] getNextPoint(int threadNumber) {

        int[] point = null;
        if (assignedCount != x * y) {
            point = new int[] {lastAssignedX - xOffset, lastAssignedY - yOffset};

            if (lastAssignedX == x - 1) {

                lastAssignedY += 1;
                lastAssignedX = 0;
            } else {

                lastAssignedX ++;
            }

            assignedCount ++;
            threadRequestCount[threadNumber] += 1;
            //System.out.println("Passing point [" + point[0] + ", " + point[1] +"] to thread " + threadNumber);
        }

        return point;
    }
}

