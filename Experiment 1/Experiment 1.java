//Name- Panshul Srivastava
//UID- 24BCS10792

import java.util.*;
import java.time.*;

class ExpRec {

    static int dpth = 0;

    static void complexRec(int n) {

        dpth++;

        if (n <= 2) {
            System.out.println(dpth);
            return;
        }

        int p = n;

        while (p > 0) {
            int[] temp = new int[n];
            for (int i = 0; i < n; i++) {
                temp[i] = i ^ p;
            }
            p = p >> 1;
        }

        int[] small = new int[n];
        for (int i = 0; i < n; i++) {
            small[i] = i * i;
        }

        if (n % 3 == 0) {
            for (int i = 0; i < n / 2; i++) {
                int t = small[i];
                small[i] = small[n - i - 1];
                small[n - i - 1] = t;
            }
        } else {
            for (int i = 0; i < n / 2; i++) {
                int t = small[i];
                small[i] = small[n - i - 1];
                small[n - i - 1] = t;
            }
        }

        complexRec(n / 2);
        complexRec(n / 2);
        complexRec(n / 2);
    }

    public static void main(String[] args) {

        Scanner sc = new Scanner(System.in);
        int n = sc.nextInt();

        long start = System.currentTimeMillis();

        complexRec(n);

        long end = System.currentTimeMillis();

        System.out.println("Recursion Depth = " + dpth);
        System.out.println("Time  = " + (end - start));

        sc.close();
    }
}

