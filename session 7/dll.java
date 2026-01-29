class Node {
    int v;
    Node n, p;

    Node(int d) {
        v = d;
        n = p = null;
    }
}

class DLL {

    Node h, t;

    DLL() {
        h = t = null;
    }

    void ins_beg(int v) {
        Node nn = new Node(v);
        if (h == null) {
            h = t = nn;
            return;
        }
        nn.n = h;
        h.p = nn;
        h = nn;
    }

    void ins_end(int v) {
        Node nn = new Node(v);
        if (t == null) {
            h = t = nn;
            return;
        }
        t.n = nn;
        nn.p = t;
        t = nn;
    }

    void ins_idx(int idx, int v) {
        if (idx == 0) {
            ins_beg(v);
            return;
        }

        Node tmp = h;
        int c = 0;

        while (tmp != null && c < idx - 1) {
            tmp = tmp.n;
            c++;
        }

        if (tmp == null) {
            System.out.println("Idx OOB");
            return;
        }

        if (tmp.n == null) {
            ins_end(v);
            return;
        }

        Node nn = new Node(v);
        nn.n = tmp.n;
        nn.p = tmp;
        tmp.n.p = nn;
        tmp.n = nn;
    }

    void del_beg() {
        if (h == null) return;

        if (h == t) {
            h = t = null;
        } else {
            h = h.n;
            h.p = null;
        }
    }

    void del_end() {
        if (t == null) return;

        if (h == t) {
            h = t = null;
        } else {
            t = t.p;
            t.n = null;
        }
    }

    void del_val(int v) {
        Node tmp = h;

        while (tmp != null) {
            if (tmp.v == v) {
                if (tmp == h)
                    del_beg();
                else if (tmp == t)
                    del_end();
                else {
                    tmp.p.n = tmp.n;
                    tmp.n.p = tmp.p;
                }
                return;
            }
            tmp = tmp.n;
        }
        System.out.println("Val NF");
    }

    void rev() {
        Node cur = h, tmp = null;

        while (cur != null) {
            tmp = cur.p;
            cur.p = cur.n;
            cur.n = tmp;
            cur = cur.p;
        }

        if (tmp != null)
            h = tmp.p;
    }

    void disp() {
        Node tmp = h;
        while (tmp != null) {
            System.out.print(tmp.v + " <-> ");
            tmp = tmp.n;
        }
        System.out.println("NULL");
    }
}

class Main {
    public static void main(String[] args) {

        DLL d = new DLL();

        d.ins_beg(3);
        d.ins_beg(2);
        d.ins_beg(1);
        d.ins_end(4);
        d.ins_end(5);
        d.disp();

        d.ins_idx(2, 99);
        d.disp();

        d.del_val(99);
        d.disp();

        d.rev();
        d.disp();
    }
}
