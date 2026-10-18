#include <cstdio>
#include <algorithm>

using namespace std;

enum {
  MAXN = 100 * 1000,
};

int tree[4 * MAXN];

int sum(int node, int l, int r, int sum_left, int sum_right) {
  if (sum_left > sum_right) {
    return 0;
  }
  if (sum_left == l && sum_right == r) {
    return tree[node];
  }
  int m = (l + r) / 2;
  return sum(node * 2, l, m, sum_left, min(sum_right, m)) +
         sum(node * 2 + 1, m + 1, r, max(sum_left, m + 1), sum_right);
}

void add(int node, int l, int r, int pos, int val) {    
  tree[node] += val;
  if (l == r) {    
    return;
  }
  int m = (l + r) / 2;
  if (pos <= m) {
    add(node * 2, l, m, pos, val);
  } else {
    add(node * 2 + 1, m + 1, r, pos, val);
  }
}

int N;
int rightmost_position[MAXN + 1];
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

int find_unique(int l, int r) { 
  return sum(1, 1, N, l, r);
}

int find_same_class_binsearch(int i) {
  int l = 0, r = i;
  while (r - l > 1) {
    int m = (l + r) / 2;
    if (make_request(m, i) == find_unique(m, i - 1) + 1) {
      r = m;
    } else {
      l = m;
    }
  }
  return l;
}

int main() {
  scanf("%d", &N);
  classes[1] = 1; 
  rightmost_position[1] = 1;
  add(1, 1, N, rightmost_position[1], 1);
  int num_classes = 1;
  for (int i = 2; i <= N; ++i) {
    int same_index = find_same_class_binsearch(i);
    if (same_index == 0) {
      classes[i] = ++num_classes;
    } else {
      classes[i] = classes[same_index];
      add(1, 1, N, rightmost_position[classes[i]], -1);      
    }    

    rightmost_position[classes[i]] = i;
    add(1, 1, N, rightmost_position[classes[i]], 1);
  }
  printf("Ready!\n");
  printf("%d\n", num_classes);
  for (int i = 1; i <= N; ++i) {
    printf("%d ", classes[i]);
  }
  fflush(stdout);
  return 0;
}
