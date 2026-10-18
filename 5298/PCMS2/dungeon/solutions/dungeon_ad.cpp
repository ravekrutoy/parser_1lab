#include <bits/stdc++.h>
#define forn(i, n) for (int i = 0; i < n; i++)
#define re return
#define mp make_pair
#define fi first
#define se second
#define sz(a) (int)a.size()
using namespace std;
  
typedef long long ll;
typedef complex<double> cmpl;
  
const int mod = int(1e9) + 7;
ll n, m, k, use[1000], a[1000];
 
bool better(int c, int b) {
    int coor1 = 2 * c + 1, coor2 = 2 * b + 1, coor3 = 2 * k;
    if (abs(coor1 - coor3) < abs(coor2 - coor3)) return true;
    return false;
}
int main() {
    iostream::sync_with_stdio(0), cin.tie(0);
    cin >> n >> m >> k;
    forn (i, n) {
        cin >> a[i];
    }
    forn (i, m) {
        int b;
        cin >> b;

        int num = -1;
        forn (i, n) {
            if (use[i]) continue;
            if (a[i] == b) {
                if (num == -1 || better(i, num)) {
                    num = i;
                }
            }
        }
        if (num != -1) {
            use[num] = 1;
            cout << num + 1 << " ";
            continue;
        }
        forn (i, n) {
            if (use[i] || a[i] < b) continue;
            if (num == -1 || better(i, num)) num = i;
        }
        if (num != -1) {
            use[num] = 1;
            cout << num + 1 << " ";
        } else
            cout << -1 << " ";
    }
    return 0;
}