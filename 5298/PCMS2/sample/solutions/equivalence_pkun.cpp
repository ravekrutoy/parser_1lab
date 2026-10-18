#include <cstdio>
#include <vector>
#include <set>
#include <map>
#include <algorithm>
using namespace std;

//#define SELF_CHECK

#ifdef SELF_CHECK
vector<int> real;
int request(int l, int r) {
  set<int> s(real.begin()+l, real.begin() + r + 1);
  return s.size();
}
#else

map<pair<int, int>, int> cache;
int request(int l, int r) {
  if (l == r) return 1;
  if (cache.find(make_pair(l, r)) != cache.end())
    return cache[make_pair(l, r)];
  printf("? %d %d\n", l + 1, r + 1);
  fflush(stdout);
  int res;
  scanf("%d",&res);
  if (res == -1) exit(0);
  cache[make_pair(l, r)] = res;
  return res;
}
#endif

int n;
int bit[100000];

void update(int pos, int val) {
  for (; pos < n; pos |= (pos + 1))
    bit[pos] += val;
}

int get(int r) {
  int ans = 0;
  while (r != -1) {
    ans += bit[r];
    r = (r & (r + 1)) - 1;
  }
  return ans;
}

int get(int l, int r) {
  return get(r) - get(l - 1);
}

int main() {
  scanf("%d", &n);
#ifdef SELF_CHECK
  real.resize(n);
  for (int i = 0; i < n; i++)
    scanf("%d", &real[i]);
#endif

  vector<int> ans(n);
  int cur = 0;
  for (int i = 0; i < n; i++) {
    int l = -1;
    int r = i;

    while (r - l > 1) {
      int m = (l + r) / 2;
      if (request(m, i) != get(m, i - 1)) {
        r = m;
      } else {
        l = m;
      }
    }

    if (l == -1) ans[i] = ++cur;
    else ans[i] = ans[l];

    update(i, 1);
    if (l != -1)
      update(l, -1);
  }
  printf("Ready!\n");
  printf("%d\n", cur);
  for (int i = 0; i < (int)ans.size(); i++)
    printf("%d%c", ans[i], " \n"[i==(int)ans.size()-1]);
  return 0;
}
