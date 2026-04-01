import java.util.*;

class Kruskal {
    static int[] par, rnk;

    static int find(int x) {
        if (par[x] != x) par[x] = find(par[x]);
        return par[x];
    }

    static void unite(int x, int y) {
        int px = find(x), py = find(y);
        if (px == py) return;
        if (rnk[px] < rnk[py]) par[px] = py;
        else if (rnk[px] > rnk[py]) par[py] = px;
        else { par[py] = px; rnk[px]++; }
    }

    static int kruskal(int v, int[][] edges) {
        Arrays.sort(edges, (a, b) -> a[2] - b[2]);
        par = new int[v]; rnk = new int[v];
        for (int i = 0; i < v; i++) par[i] = i;
        int tw = 0, eu = 0;
        for (int[] e : edges) {
            if (find(e[0]) != find(e[1])) {
                unite(e[0], e[1]);
                tw += e[2]; eu++;
            }
            if (eu == v - 1) break;
        }
        return tw;
    }

    public static void main(String[] a) {
        int v = 5;
        int[][] edges = {{0,1,2},{0,3,6},{1,2,3},{1,3,8},{1,4,5},{2,4,7}};
        System.out.println("MST Weight: " + kruskal(v, edges));
    }
}
