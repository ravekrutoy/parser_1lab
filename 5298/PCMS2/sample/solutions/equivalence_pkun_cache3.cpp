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

int main() {
  int n;
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

    if (request(0, i) == cur + 1) {
      r = 0;
    }

    for (int bit = 20; bit >= 0; bit--) {
      if (l + (1 << bit) >= r) continue;
      int m = l + (1 << bit);
      if (request(m, i) != request(m, i - 1)) {
        r = m;
      } else {
        l = m;
      }
    }

    if (l == -1) ans[i] = ++cur;
    else ans[i] = ans[l];
  }
  printf("Ready!\n");
  printf("%d\n", cur);
  for (int i = 0; i < (int)ans.size(); i++)
    printf("%d%c", ans[i], " \n"[i==(int)ans.size()-1]);
  return 0;
}
