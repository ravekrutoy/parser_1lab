#include "testlib.h"
#include <iostream>
using namespace std;

const int GROUPS_CNT = 4;
const int MAXN = 1000;
const int MAXX = 1000;

string to_string(int x) 
{
    stringstream ss;
    string s;
    ss << x;
    ss >> s;
    return s;
}

int main(int argc, char * argv[])
{
    registerValidation(argc, argv);
    int group = 0;
    group = atoi(validator.group().c_str());
    int n = inf.readInt(1, MAXN, "n");
    inf.readSpace();
    int m = inf.readInt(1, MAXN, "m");
    inf.readSpace();
    int k = inf.readInt(0, n, "k");
    ensuref(group != 1 || k == 0, "k != 0");
    inf.readEoln();
    for (int i = 0; i < n; i++)
    {
        int a = inf.readInt(1, MAXX, "a[" + to_string(i + 1) + "]");
        ensuref(group != 2 || a == 1, "a[%d] != 1", i + 1);
        if (i < n - 1)
            inf.readSpace();
    }
    inf.readEoln();
    for (int i = 0; i < m; i++)
    {
        int b = inf.readInt(1, MAXX, "b[" + to_string(i + 1) + "]");
        ensuref(group != 3 || b == 1, "b[%d] != 1", i + 1);
        if (i < m - 1)
            inf.readSpace();
    }
    inf.readEoln();


    inf.readEof();
    return 0;
}