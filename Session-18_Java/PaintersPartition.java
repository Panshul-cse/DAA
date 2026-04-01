class PaintersPartition {
    static boolean isPoss(int[] arr, int k, long maxT) {
        int pr = 1;
        long ct = 0;
        for (int i = 0; i < arr.length; i++) {
            if (ct + arr[i] > maxT) { pr++; ct = arr[i]; if (pr > k) return false; }
            else ct += arr[i];
        }
        return true;
    }

    static long minTime(int[] arr, int k) {
        long lo = 0, hi = 0, ans;
        for (int i : arr) { if (arr[i] > lo) lo = arr[i]; hi += arr[i]; }
        ans = hi;
        while (lo <= hi) {
            long mid = lo + (hi - lo) / 2;
            if (isPoss(arr, k, mid)) { ans = mid; hi = mid - 1; }
            else lo = mid + 1;
        }
        return ans;
    }

    public static void main(String[] a) {
        int[] arr = {10, 20, 30, 40};
        System.out.println("Min time: " + minTime(arr, 2));
    }
}
