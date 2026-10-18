#include <cstdio>
#include <vector>
#include <set>
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
int request(int l, int r) {
  printf("? %d %d\n", l + 1, r + 1);
  fflush(stdout);
  int res;
  scanf("%d",&res);
  if (res == -1) exit(0);
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

    while (r - l > 1) {
      int m = (l + r) / 2;
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
