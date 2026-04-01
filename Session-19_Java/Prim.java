import java.util.*;

class Prim {
    static int prim(int v, List<List<int[]>> adj) {
        PriorityQueue<int[]> pq = new PriorityQueue<>((a, b) -> a[0] - b[0]);
        boolean[] inMst = new boolean[v];
        int tw = 0;
        pq.offer(new int[]{0, 0});
        while (!pq.isEmpty()) {
            int[] cur = pq.poll();
            int wt = cur[0], nd = cur[1];
            if (inMst[nd]) continue;
            inMst[nd] = true;
            tw += wt;
            for (int[] nb : adj.get(nd)) {
                if (!inMst[nb[1]]) pq.offer(new int[]{nb[0], nb[1]});
            }
        }
        return tw;
    }

    public static void main(String[] a) {
        int v = 5;
        List<List<int[]>> adj = new ArrayList<>();
        for (int i = 0; i < v; i++) adj.add(new ArrayList<>());
        adj.get(0).add(new int[]{2,1}); adj.get(1).add(new int[]{2,0});
        adj.get(0).add(new int[]{6,3}); adj.get(3).add(new int[]{6,0});
        adj.get(1).add(new int[]{3,2}); adj.get(2).add(new int[]{3,1});
        adj.get(1).add(new int[]{8,3}); adj.get(3).add(new int[]{8,1});
        adj.get(1).add(new int[]{5,4}); adj.get(4).add(new int[]{5,1});
        adj.get(2).add(new int[]{7,4}); adj.get(4).add(new int[]{7,2});
        System.out.println("MST Weight: " + prim(v, adj));
    }
}
