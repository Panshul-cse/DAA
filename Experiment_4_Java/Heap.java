class Heap {
    static int[] h = new int[100];
    static int sz = 0;

    static void hUp(int i) {
        while (i > 0 && h[(i-1)/2] > h[i]) {
            int tmp = h[(i-1)/2]; h[(i-1)/2] = h[i]; h[i] = tmp;
            i = (i-1)/2;
        }
    }

    static void hDown(int i) {
        int sm = i, l = 2*i+1, r = 2*i+2;
        if (l < sz && h[sm] > h[l]) sm = l;
        if (r < sz && h[sm] > h[r]) sm = r;
        if (sm != i) {
            int tmp = h[sm]; h[sm] = h[i]; h[i] = tmp;
            hDown(sm);
        }
    }

    static int srch(int val) {
        for (int i = 0; i < sz; i++) if (h[i] == val) return i;
        return -1;
    }

    static void del(int idx) {
        if (idx < 0 || idx >= sz) { System.out.println("Invalid idx"); return; }
        h[idx] = h[sz-1]; sz--;
        if (idx > 0 && h[idx] < h[(idx-1)/2]) hUp(idx);
        else hDown(idx);
    }

    static void ins(int val) {
        if (sz == 100) { System.out.println("Overflow"); return; }
        h[sz++] = val;
        hUp(sz-1);
    }

    static void delRoot() {
        if (sz == 0) { System.out.println("Underflow"); return; }
        h[0] = h[sz-1]; sz--;
        hDown(0);
    }

    static void print() {
        for (int i = 0; i < sz; i++) System.out.print(h[i] + " ");
        System.out.println();
    }

    public static void main(String[] a) {
        ins(10); ins(30); ins(1);
        print();
    }
}
