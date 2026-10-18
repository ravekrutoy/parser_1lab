#include <cstdio>
#include <map>
#include <algorithm>

using namespace std;

enum {
  MAXN = 100 * 1000,
};

int tree[4 * MAXN];

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

int find_class(int node, int l, int r, int sum, int i, bool went_right) {
  if (l == r) {
    if (went_right) {
      return l;
    } else {
      // never went to the right, must do the last check
      if (make_request(l, i) == sum + tree[node] + 1) {
        return 0;
      } else {
        return l;
      }
    }
  }
  int m = (l + r) / 2;  
  if (i <= m) {
    return find_class(node * 2, l, m, sum, i, went_right);
  } else {
    // m < i
    int s_right = sum + tree[node * 2 + 1];
    if (make_request(m + 1, i) == s_right + 1) {
      return find_class(node * 2, l, m, s_right, i, went_right);
    } else {
      return find_class(node * 2 + 1, m + 1, r, sum, i, true);
    }    
  }  
}

int N;
int rightmost_position[MAXN + 1];
int classes[MAXN + 1];

int find_same_class_binsearch(int i) {
  int l = find_class(1, 1, N, 0, i, false);
  return l;  
}

int main() {
  scanf("%d", &N);
  int num_classes = 1;
  classes[1] = 1; 
  rightmost_position[1] = 1;
  add(1, 1, N, rightmost_position[1], 1);  
  for (int i = 2; i <= N; ++i) {
    int same_index = 0;
    if (make_request(1, i) <= num_classes) {
        same_index = find_same_class_binsearch(i);
    }
    
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
