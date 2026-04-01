class LowerUpperBound {
    static int lb(int[] v, int val) {
        int st = 0, en = v.length - 1, ans = v.length;
        while (st <= en) {
            int mid = st + (en - st) / 2;
            if (v[mid] >= val) { ans = mid; en = mid - 1; }
            else st = mid + 1;
        }
        return ans;
    }

    static int ub(int[] v, int val) {
        int st = 0, en = v.length - 1, ans = v.length;
        while (st <= en) {
            int mid = st + (en - st) / 2;
            if (v[mid] > val) { ans = mid; en = mid - 1; }
            else st = mid + 1;
        }
        return ans;
    }

    public static void main(String[] a) {
        int[] v = {1, 2, 4, 4, 6, 8};
        System.out.println("LB of 4: " + lb(v, 4));
        System.out.println("UB of 4: " + ub(v, 4));
    }
}
