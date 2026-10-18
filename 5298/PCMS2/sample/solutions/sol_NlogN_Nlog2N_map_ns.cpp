#include <cstdio>
#include <map>
#include <algorithm>

using namespace std;

enum {
  MAXN = 100 * 1000,
};

int N;
int rightmost_position[MAXN + 1];
int classes[MAXN + 1];

map<int, int> rightmost_class;

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

int find_unique(int i) {  
  return distance(rightmost_class.lower_bound(i), rightmost_class.end());
}

int find_same_class_binsearch(int i) {
  int l = 0, r = i;
  while (r - l > 1) {
    int m = (l + r) / 2;
    if (make_request(m, i) == find_unique(m) + 1) {
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
  rightmost_class.insert(pair<int, int>(1, 1));
  rightmost_position[1] = 1;
  int num_classes = 1;
  for (int i = 2; i <= N; ++i) {    
    int same_index = find_same_class_binsearch(i);    
    if (same_index == 0) {
      classes[i] = ++num_classes;
      rightmost_class.insert(pair<int, int>(i, classes[i]));
      rightmost_position[classes[i]] = i;
    } else {
      classes[i] = classes[same_index];
      int old_key = rightmost_position[classes[i]];
      rightmost_position[classes[i]] = i;
      int new_key = rightmost_position[classes[i]];
      rightmost_class.erase(old_key);
      rightmost_class.insert(pair<int, int>(new_key, classes[i]));
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
