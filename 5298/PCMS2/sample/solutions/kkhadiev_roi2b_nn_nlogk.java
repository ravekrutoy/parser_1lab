import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.util.*;

/**
 * Created by Kamil Khadiev on 11.08.2015.
 */
public class kkhadiev_roi2b_nn_nlogk {


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
    static int i1,j1,qq1;

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
                List<Bound> boundList = new ArrayList<>();
                boundList.addAll(bounds);
                int l = 0, k = boundList.size(), r = k-1;
                while (l<r-1){
                    int z = (l+r)/2;
                    Bound bound = boundList.get(z);
                    int q1 = query(in, out, bound.x + 1, i);
                    i1 =  bound.x + 1;
                    j1 = i;
                    qq1 = q1;
                    if (k-z-1==q1){
                        l = z+1;
                    }
                    else{
                        r = z;
                    }
                }
                if (check(in, out, boundList.get(l),l,k,i)){
                    isUpdate = true;
                    boundForUpdate = boundList.get(l);
                }
                else
                {
                    if (l!=r){
                        if (check(in, out,boundList.get(r),r,k,i)){
                            isUpdate = true;
                            boundForUpdate = boundList.get(r);
                        }
                    }
                }
                if (isUpdate){
                    bounds.remove(boundForUpdate);
                    bounds.add(new Bound(i,a[i]));
                }

//                for (Bound bound : bounds){
//                    if (bound.x+1 == i) {
//                        a[i] = a[i-1];
//                        isUpdate = true;
//                        boundForUpdate = bound;
//                        break;
//                    } else {
//                        int q1 = query(in, out, bound.x + 1, i);
//                        if (q1 == q) {
//                            a[i] = bound.y;
//                            isUpdate = true;
//                            boundForUpdate = bound;
//                            break;
//                        } else {
//                            q = q1;
//                        }
//                    }
//                }
                if (isUpdate){
                    bounds.remove(boundForUpdate);
                    bounds.add(new Bound(i,a[i]));
                }
            }
        }
    }

    private static boolean check(BufferedReader in, PrintWriter out, Bound bound, int l, int k, int i) throws IOException {
        boolean isUpdate = false;
        if (bound.x+1 == i) {
            a[i] = a[i-1];
            isUpdate = true;
        } else {
            int q1 = query(in, out, bound.x + 1, i);
            if (q1 != k-l-1) {
                a[i] = bound.y;
                isUpdate = true;

            }
        }
        return isUpdate;
    }

    private static int query(BufferedReader in, PrintWriter out, int i, int j) throws IOException {
        if (i == i1 && j==j1) return qq1;
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
