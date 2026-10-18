//#include <iostream>
#include <cmath>
#include <algorithm>
#include <vector>
#include <set>
#include <cstdio>

using namespace std;

const long double  mx = 1e9;

int main() {
    //ios_base::sync_with_stdio(false);
    //cin.tie(0);
    //cout.setf(ios::fixed);
    //cout.precision(4);
    int n;
    scanf("%d", &n);
    //cin >> n;
    vector < int > x(n, 0);
    vector < int > sum (n, 0);
    sum[0]++;
    x[0] = 1;
    int k = 1;
    for (int i = 1; i < n; ++i) {
        //cout << "? " << 1 << " " << i + 1 << endl;
        printf("? %d %d\n", 1, i + 1);
        fflush(stdout);
        int a;
        scanf("%d", &a);
        //cin >> a;
        if (a == k + 1) {
            k++;
            x[i] = k;
            for (int j = 0; j <= i; ++j) {
                sum[j]++;
            }
        } else {
            int bg  = 0, ed = i + 1;
            while (bg + 1 != ed) {
                int mid = (bg + ed)/2;
                int pf = sum[mid];
                //cout << "? " << mid + 1 << " " << i + 1 << endl;
                printf("? %d %d\n", mid + 1, i + 1);
                fflush(stdout);
                int b;
                //cin >> b;
                scanf("%d", &b);
                if (pf + 1 == b) {
                    ed = mid;
                } else {
                    bg = mid;
                }
            }
            //cout << bg << endl;
            x[i] = x[bg];
            for (int j = bg + 1; j <= i; ++j) {
                sum[j]++;
            }
            //sum[x[i]]++;
        }
    }
    printf("Ready!\n");
    printf("%d\n", k);
    for (int i = 0; i < n; ++i) {
        printf("%d ", x[i]);
    }
    //cout << "Ready!" << endl;
    //cout << k << endl;
    //for (int i = 0; i < n; ++i) {
    //    cout << x[i] << " ";
    //}
    return 0;
}