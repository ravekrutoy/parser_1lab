#include <cstdio>
#include <map>
#include <algorithm>

using namespace std;

enum {
  MAXN = 100 * 1000,
};

int N;
int classes[MAXN + 1];

int make_request(int i, int j) {
  if (i == j) {
    return 1;
  }
  printf("? %d %d\n", i, j);
  fflush(stdout);
  int result;
  scanf("%d", &result);
  if (result == -1) {
    exit(0);
  }
  return result;
}

int find_same_class_binsearch(int i) {
  int l = 0, r = i;
  while (r - l > 1) {
    int m = (l + r) / 2;
    if (make_request(m, i - 1) != make_request(m, i)) {
      r = m;
    }
    else {
      l = m;
    }
  }
  return l;
}

int main() {
  scanf("%d", &N);
  classes[1] = 1;
  int num_classes = 1;
  for (int i = 2; i <= N; ++i) {
    int same_index = find_same_class_binsearch(i);
    if (same_index == 0) {
      classes[i] = ++num_classes;      
    } else {
      classes[i] = classes[same_index];      
    }
  }
  printf("Ready!\n");
  printf("%d\n", num_classes);
  for (int i = 1; i <= N; ++i) {
    printf("%d ", classes[i]);
  }
  fflush(stdout);  
  return 0;
}
