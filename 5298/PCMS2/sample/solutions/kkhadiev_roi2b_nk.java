import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.util.List;
import java.util.Set;
import java.util.StringTokenizer;
import java.util.TreeSet;

/**
 * Created by Kamil Khadiev on 11.08.2015.
 */
public class kkhadiev_roi2b_nk {


    public static void main(String[] args) throws IOException {
        BufferedReader in = new BufferedReader(new InputStreamReader(System.in));
        init(in);


        PrintWriter out = new PrintWriter(System.out);
        solve(in, out);
        print(out);
        in.close();
        out.close();

    }
    public static int n,m , g;
    public static int[]d,a;

    static Set<Bound> bounds;
    static String s;


    private static void init(BufferedReader in) throws IOException {
        StringTokenizer st = new StringTokenizer(in.readLine().trim());
        n = Integer.parseInt(st.nextToken());

    }

    private static void solve(BufferedReader in, PrintWriter out) throws IOException {
        a = new int[n+1];
        a[1] = 1;
        bounds = new TreeSet<>();
        bounds.add(new Bound(1,1));
        for (int i = 2; i<=n; i++){
            int q = query(in, out, 1, i);
            if (q>bounds.size()){
                bounds.add(new Bound(i, q));
                a[i] = q;
            }
            else
            {
                boolean isUpdate = false;
                Bound boundForUpdate = null;
                for (Bound bound : bounds){
                    if (bound.x+1 == i) {
                        a[i] = a[i-1];
                        isUpdate = true;
                        boundForUpdate = bound;
                        break;
                    } else {
                        int q1 = query(in, out, bound.x + 1, i);
                        if (q1 == q) {
                            a[i] = bound.y;
                            isUpdate = true;
                            boundForUpdate = bound;
                            break;
                        } else {
                            q = q1;
                        }
                    }
                }
                if (isUpdate){
                    bounds.remove(boundForUpdate);
                    bounds.add(new Bound(i,a[i]));
                }
            }
        }
    }

    private static int query(BufferedReader in, PrintWriter out, int i, int j) throws IOException {
        out.println("? " + i + " " + j);
        out.flush();

        return  Integer.parseInt(in.readLine().trim());
    }


    static class Bound implements Comparable<Bound>{
        int x,y;

        public Bound(int x, int y) {
            this.x = x;
            this.y = y;
        }

        @Override
        public String toString() {
            return "Bound{" +
                    "x=" + x +
                    ", y=" + y +
                    '}';
        }

        @Override
        public boolean equals(Object o) {
            if (this == o) return true;
            if (o == null || getClass() != o.getClass()) return false;

            Bound bound = (Bound) o;

            return x == bound.x;

        }

        @Override
        public int hashCode() {
            return x;
        }

        @Override
        public int compareTo(Bound o) {
            return Integer.compare(x,o.x);
        }
    }

    private static void print(PrintWriter out) throws IOException {
        out.println("Ready!");
        out.println(bounds.size());
        for (int i = 1; i < n+1; i++) {
            out.print(a[i] + " ");
        }

    }
}
