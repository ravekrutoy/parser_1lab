#ifndef BZ
#pragma GCC optimize "-O3"
#endif
#include <bits/stdc++.h>

#define FASTIO
#define ALL(v) (v).begin(), (v).end()
#define rep(i, l, r) for (int i = (l); i < (r); ++i)

#ifdef FASTIO
#define scanf abacaba
#define printf abacaba
#endif

typedef long long ll;
typedef long double ld;
typedef unsigned long long ull;

using namespace std;


/*
ll pw(ll a, ll b) {
	ll ans = 1; while (b) {
		while (!(b & 1)) b >>= 1, a = (a * a) % MOD;
		ans = (ans * a) % MOD, --b;
	} return ans;
}
*/

const int MAXN = 220000;

int n;
ll t;
ll a[MAXN];
int x[MAXN];
int ad[MAXN];
int fl[MAXN];
ll b[MAXN];

void no() {
	cout << "No\n";
	exit(0);
}

int main() {
#ifdef FASTIO
	ios_base::sync_with_stdio(false), cin.tie(0), cout.tie(0);
#endif
	cin >> n >> t;
	rep(i, 0, n) {
		cin >> a[i];
	}
	rep(i, 0, n) {
		cin >> x[i];
		--x[i];
		if (x[i] < i)
			no();
		++ad[i + 1];
		--ad[x[i] + 1];
	}
	int now = 0;
	rep(i, 0, n) {
		now += ad[i];
		if (now)
			fl[i] = 1;
		else
			fl[i] = 0;
	}
	for (int i = 0; i < n; ++i)
		b[i] = a[i];
	for (int i = 0; i < n - 1; ++i)
		if (fl[i + 1])
			b[i] = max(b[i], a[i + 1]);
	for (int i = 1; i < n; ++i)
		b[i] = max(b[i], b[i - 1] + 1);
	int cur = 0;
	for (int i = n - 2; i >= 0; --i) {
		if (a[i + 1] <= b[i])
			++cur;
		else
			cur = 0;
		if (x[i] != i + cur)
			no();
	}
	cout << "Yes\n";
	for (int i = 0; i < n; ++i)
		cout << b[i] + t << " ";
	cout << "\n";
	return 0;
}


