#include <cstdio>
#include <iostream>
#include <cassert>
#include <vector>
#include <map>
#include <string>
#include <algorithm>
#include <sstream>
#include "testlib.h"

using namespace std;

int cur_test = -1;
const int GROUPS_CNT = 4;
const int MAXN = 1000;
const int MAXX = 1000;
const int MAXA[GROUPS_CNT] = {MAXX, 1, MAXX, MAXX};
const int MAXB[GROUPS_CNT] = {MAXX, MAXX, 1, MAXX};

string itoa(int x) 
{
    stringstream ss;
    string s;
    ss << x;
    ss >> s;
    return s;
}

int atoi(string s) 
{
    stringstream ss;
    int x;
    ss << s;
    ss >> x;
    return x;
}

void write_test(int k, vector<int> a, vector<int> b) 
{
    startTest(cur_test++);
    cerr << cur_test + 3 << endl;
    cout << a.size() << ' ' << b.size() << ' ' << k << endl;
    for (int i = 0; i < (int)a.size() - 1; i++)
        cout << a[i] << ' ';
    cout << a.back() << endl;
    for (int i = 0; i < (int)b.size() - 1; i++)
        cout << b[i] << ' ';
    cout << b.back() << endl;
}

void gen_rand(int n, int m, int k, int maxa, int maxb)
{
    vector<int> a(n);
    for (int i = 0; i < n; i++)
        a[i] = rnd.next(1, maxa);
    vector<int> b(m);
    for (int i = 0; i < m; i++)
        b[i] = rnd.next(1, maxb);
    write_test(k, a, b);
}

void gen_rand_equal(int n, int k, int maxa, int maxb)
{
    vector<int> a(n);
    for (int i = 0; i < n; i++)
        a[i] = rnd.next(1, min(maxa, maxb));
    write_test(k, a, a);
}

void gen_sorted(int n, int m, int k, int maxa, int maxb)
{
    vector<int> a(n);
    for (int i = 0; i < n; i++)
        a[i] = rnd.next(1, maxa);
    vector<int> b(m);
    for (int i = 0; i < m; i++)
        b[i] = rnd.next(1, maxb);
    sort(a.begin(), a.end());
    sort(b.rbegin(), b.rend());
    write_test(k, a, b);
}

void gen_special(int n, int m, int k, int maxa, int maxb)
{
    vector<int> a(n);
    for (int i = 0; i < n / 2; i++)
        a[i] = min(i + 1, maxa);
    for (int i = n / 2; i < n; i++)
        a[i] = min(n - i, maxa);
    vector<int> b = a;
    b.resize(m);
    for (int i = n; i < m; i++)
        b[i] = a[rnd.next(n)];
    for (int i = 0; i < m; i++)
        b[i] = min(b[i], maxb);
    sort(b.begin(), b.end());
    write_test(k, a, b);
}

void gen_special1(int n, int m, int k, int maxa, int maxb)
{
    vector<int> a(n);
    for (int i = 0; i < n / 2; i++)
        a[i] = min(i + 1, maxa);
    for (int i = n / 2; i < n; i++)
        a[i] = min(n - i, maxa);
    vector<int> b = a;
    b.resize(m);
    for (int i = n; i < m; i++)
        b[i] = a[rnd.next(n)];
    for (int i = 0; i < m; i++)
        b[i] = min(b[i], maxb);
    shuffle(b.begin(), b.end());
    write_test(k, a, b);
}


int main(int argc, char * argv[]) 
{
    registerGen(argc, argv, 1);
    cur_test = atoi(argv[1]);
    gen_rand(5, 10, 0, 10, 10);
    gen_rand_equal(6, 0, 10, 10);
    gen_sorted(7, 10, 0, 10, 10);
    gen_special(10, 5, 0, MAXX, MAXX);
    gen_special1(10, 5, 0, MAXX, MAXX);
    
    gen_rand(MAXN, MAXN, 0, MAXX, MAXX);
    gen_rand_equal(MAXN, 0, MAXX, MAXX);
    gen_sorted(MAXN, MAXN, 0, MAXX, MAXX);
    gen_special(MAXN, MAXN, 0, MAXX, MAXX);
    gen_special1(MAXN, MAXN, 0, MAXX, MAXX);
    
    cerr << "END OF GROUP" << endl;
    for (int i = 1; i < GROUPS_CNT; i++)
    {
        int n, m;
        
        n = rnd.next(10, MAXN);
        m = rnd.next(10, MAXN);
        gen_rand(n, m, rnd.next(0, n), MAXA[i], MAXB[i]);
        
        n = rnd.next(10, MAXN);
        gen_rand_equal(n, rnd.next(0, n), MAXA[i], MAXB[i]);
        
        n = rnd.next(10, MAXN);
        m = rnd.next(10, MAXN);
        gen_sorted(n, m, rnd.next(0, n), MAXA[i], MAXB[i]);
        
        n = rnd.next(10, MAXN);
        m = rnd.next(10, MAXN);
        gen_special(n, m, 0, MAXA[i], MAXB[i]);
        n = rnd.next(10, MAXN);
        m = rnd.next(10, MAXN);
        gen_special(n, m, n, MAXA[i], MAXB[i]);
        n = rnd.next(10, MAXN);
        m = rnd.next(10, MAXN);
        gen_special(n, m, n / 2, MAXA[i], MAXB[i]);
        n = rnd.next(10, MAXN);
        m = rnd.next(10, MAXN);
        gen_special(n, m, rnd.next(1, n - 1), MAXA[i], MAXB[i]);
        
        n = rnd.next(10, MAXN);
        m = rnd.next(10, MAXN);
        gen_special1(n, m, 0, MAXA[i], MAXB[i]);
        n = rnd.next(10, MAXN);
        m = rnd.next(10, MAXN);
        gen_special1(n, m, n, MAXA[i], MAXB[i]);
        n = rnd.next(10, MAXN);
        m = rnd.next(10, MAXN);
        gen_special1(n, m, n / 2, MAXA[i], MAXB[i]);
        n = rnd.next(10, MAXN);
        m = rnd.next(10, MAXN);
        gen_special1(n, m, rnd.next(1, n - 1), MAXA[i], MAXB[i]);
        
        cerr << "END OF GROUP" << endl;
    }
    gen_rand(MAXN, MAXN, MAXN / 2, 10, 10);
    gen_rand_equal(MAXN, MAXN / 2, 10, 10);
    gen_sorted(MAXN, MAXN, MAXN / 2, MAXX, MAXX);
    gen_special(MAXN, MAXN, MAXN / 2, MAXX, MAXX);
    gen_special1(MAXN, MAXN, MAXN / 2, MAXX, MAXX);
    cerr << "END OF GROUP" << endl;    
    return 0;
}