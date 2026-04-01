import java.util.Arrays;

class AggressiveCows {
    static int solve(int[] st, int k) {
        Arrays.sort(st);
        int n = st.length;
        int lo = 1, hi = st[n-1] - st[0], ans = 0;
        while (lo <= hi) {
            int mid = lo + (hi - lo) / 2;
            int cnt = 1, lp = st[0];
            for (int i = 1; i < n; i++) {
                if (st[i] - lp >= mid) { cnt++; lp = st[i]; }
            }
            if (cnt >= k) { ans = mid; lo = mid + 1; }
            else hi = mid - 1;
        }
        return ans;
    }

    public static void main(String[] a) {
        int[] st = {0, 3, 4, 7, 10, 9};
        System.out.println("Max min dist: " + solve(st, 4));
    }
}
