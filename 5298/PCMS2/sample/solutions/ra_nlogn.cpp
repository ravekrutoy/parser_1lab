#include <bits/stdc++.h>
using namespace std;
const int sh = 1 << 17;
int rm[2 * sh + 10];
int a[sh];
int pr[sh];
int get(int l, int r) {
  if (l > r) return -1;
  if (l == r) return 1;
  printf("? %d %d\n", l + 1, r + 1);
  fflush(stdout);
  int res;
  scanf("%d", &res);
  if (res == -1) exit(0);
  return res;
}
void upd(int x, int v) {
  x += sh;
  while (x >= 1) {
    rm[x] += v;
    x >>= 1;
  }
}
int cnt = 0;
int v0 = sh;
int r0 = 0;
int calc(int i) {
  if (i > r0) {
    r0 = 2 * r0 + 1;
    v0 >>= 1;
  }
  int v = v0;
  int l = 0;
  int r = r0;  
  int cur = 0;
  while (l < r) {
    int m = (l + r) >> 1;
    int vr = (v << 1) + 1;
    if (cur + rm[vr] == get(m + 1, i)) {
      l = m + 1;      
      v = vr; 
    } else {       
      cur += rm[vr];
      r = m;
      v <<= 1;
    }
  }
  cur += rm[v];
  if (l == 0 && cur + 1 == get(l, i)) {
    return cnt++;
  }
  return a[l];
}
int main(){
  int n;
  scanf("%d", &n);
  for (int i = 0; i < n; i++) {
    pr[i] = -1;
  }
  for (int i = 0; i < n; i++) {
    a[i] = calc(i);
    if (pr[a[i]] != -1) {
      upd(pr[a[i]], -1);
    }
    pr[a[i]] = i;
    upd(i, 1);
  }
  printf("Ready!\n");
  printf("%d\n", cnt);
  for (int i = 0; i < n; i++) {
    printf("%d%c", a[i] + 1, " \n"[i + 1 == n]);
  }
  return 0;
}
