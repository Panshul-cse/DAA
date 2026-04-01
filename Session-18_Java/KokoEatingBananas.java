class KokoEatingBananas {
    static int solve(int[] p, int h) {
        long tot = 0;
        int rt = 0;
        for (int i : p) { tot += i; if (i > rt) rt = i; }
        int lt = (int)((tot + h - 1) / h);
        while (lt < rt) {
            int mid = lt + (rt - lt) / 2;
            long sum = 0;
            for (int i : p) {
                sum += (i + mid - 1) / mid;
                if (sum > h) break;
            }
            if (sum <= h) rt = mid;
            else lt = mid + 1;
        }
        return lt;
    }

    public static void main(String[] a) {
        int[] p = {3, 6, 7, 11};
        System.out.println("Min speed: " + solve(p, 8));
    }
}
