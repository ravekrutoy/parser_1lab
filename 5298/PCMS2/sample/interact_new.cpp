#include "testlib.h"
#include <cstdio>
#include <string>
#include <algorithm>

#define PCMS2
using namespace std;

enum {
  MAXN = 3 * 1000,
  LOGN = 16,
};

int MAX_QUERIES[] = {
   72 * 1000,
   72 * 1000,
   72 * 1000,
   72 * 1000,
   72 * 1000,
   36 * 1000,
};

int N, K, group;
int a[MAXN + 1];

// persistent interval tree

struct Node {
  int left;
  int right;
  int sum;
};

Node nodes[2 * (LOGN + 1) * MAXN]; // max number of copy operations
int num_nodes = 1; // zero node is special

int copy_node(int node) {
  nodes[num_nodes] = nodes[node];
  return num_nodes++;
}

void add(int node, int l, int r, int pos, int val) {
  // we are already in the copy
  nodes[node].sum += val;
  if (l == r) {
    return;
  }
  int m = (l + r) / 2;
  if (pos <= m) {
    add(nodes[node].left = copy_node(nodes[node].left), l, m, pos, val);
  }
  else {
    add(nodes[node].right = copy_node(nodes[node].right), m + 1, r, pos, val);
  }
}

int sum(int node, int l, int r, int sum_left, int sum_right) {
  if (sum_left > sum_right) {
    return 0;
  }
  if (sum_left == l && sum_right == r) {
    return nodes[node].sum;
  }
  int m = (l + r) / 2;
  return sum(nodes[node].left, l, m, sum_left, min(sum_right, m)) +
    sum(nodes[node].right, m + 1, r, max(sum_left, m + 1), sum_right);
}

int roots[MAXN + 1];
int n_roots;
int rightmost_position[MAXN + 1];

void read_test() {
  group = inf.readInt();
  N = inf.readInt(1, MAXN, "N");
  K = inf.readInt(1, N, "K");
  for (int i = 1; i <= N; ++i) {
    a[i] = inf.readInt(1, K, "a[i]");

    roots[i] = copy_node(roots[i - 1]);
    if (rightmost_position[a[i]]) {
      add(roots[i], 1, N, rightmost_position[a[i]], -1);
    }

    rightmost_position[a[i]] = i;
    add(roots[i], 1, N, rightmost_position[a[i]], 1);
  }
}

int main(int argc, char **argv) {
  registerInteraction(argc, argv);
  read_test();

  printf("%d\n", N);
  fflush(stdout);
  string s;
  int i, j;
  int n_queries = 0;
  int max_q = MAX_QUERIES[group];
  while (true) {
    ouf.readTokenTo(s, "(\?|Ready!)", "query");
    if (s == "Ready!") {
      break;
    }
    else {      
      ++n_queries;
      i = ouf.readInt(1, N, "i");
      j = ouf.readInt(i, N, "j");      
      if (n_queries <= max_q) {
        printf("%d\n", sum(roots[j], 1, N, i, j));
        fflush(stdout);
      } else {
#ifndef PCMS2          
        printf("%d\n", -1);
        fflush(stdout);
#endif
        break;
      }
    }
  }

  if (n_queries > max_q) {
    quitf(_wa, "Query limit is reached and no answer is found");
  }

  // checking the results
  int pK = ouf.readInt(1, N, "K");
  if (pK != K) {
    quitf(_wa, "Incorrect number of symbols found");
  }
  int n_classes = 0;
  map<int, int> colors;
  int cc = 0;
  for (int i = 1; i <= N; ++i) {
    int pa = ouf.readInt(1, K, "a[i]");
    if (colors.find(pa) == colors.end()) {
        colors[pa] = ++cc;
    }
    pa = colors[pa];
    if (pa != a[i]) {
      quitf(_wa, "Wrong message!");
    }
  }

  quitf(_ok, "Message was extracted in %d queries", n_queries);
}