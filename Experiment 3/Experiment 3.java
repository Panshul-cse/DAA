import java.util.*;

class Exp3 {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        int n = sc.nextInt();
        char[] a = new char[n];

        for (int i = 0; i < n; i++)
            a[i] = sc.next().charAt(0);

        HashMap<Integer, Integer> mp = new HashMap<>();

        int sum = 0;
        int max = 0;

        mp.put(0, -1);

        for (int i = 0; i < n; i++) {
            if (a[i] == 'P')
                sum++;
            else
                sum--;

            if (mp.containsKey(sum)) {
                max = Math.max(max, i - mp.get(sum));
            } else {
                mp.put(sum, i);
            }
        }

        System.out.println(max);
        sc.close();
    }
}
