#ifndef BZ
#pragma GCC optimize -O3
#endif
#include <bits/stdc++.h>
using namespace std;
using ll = int64_t;
using ld = double;
using ull = uint64_t;

const int MAXN = 500228;
ll a[MAXN];
ll b[MAXN];
int x[MAXN];

const ll INF = static_cast<ll>(3e18);

bool no(bool cond = false) {
    if (!cond) {
        cout << "No\n";
        exit(0);
    }
}

int main() {
#ifdef BZ
    freopen("input.txt", "r", stdin);
#endif
    ios_base::sync_with_stdio(false); cin.tie(nullptr); cout.tie(nullptr); cout.setf(ios::fixed); cout.precision(20);
    int n;
    ll t;
    cin >> n >> t;
    for (int i = 0; i < n; ++i) {
        cin >> a[i];
    }


    for (int i = 0; i < n; ++i) {
        cin >> x[i];
        --x[i];
    }

    a[n] = INF;
    x[n] = n;
    b[n] = INF;

    for (int i = n - 1; i >= 0; --i) {
        if (x[i] == x[i + 1]) {
            b[i] = b[i + 1] - 1;
            no(b[i] >= a[i + 1] + t);
        } else if (x[i] == i) {
            b[i] =  min(b[i + 1] - 1, a[i + 1] + t - 1);
        } else {
            no();
        }

        no(b[i] >= a[i] + t);
    }

    cout << "Yes\n";
    for (int i = 0; i < n; ++i) {
        cout << b[i] << " ";
    }

    cout << "\n";
}
