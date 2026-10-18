#include <bits/stdc++.h>
using namespace std;

int main()
{
    int n, m, k;
    cin >> n >> m >> k;
    k--;
    vector<int> a(n);
    for (int i = 0; i < n; i++)
        cin >> a[i];
    for (int j = 0; j < m; j++)
    {
        int b;
        cin >> b;
        int l = -1, r = -1;
        for (int i = k; i >= 0; i--)
        {
            if (a[i] == b && (l == -1 || a[l] != b))
                l = i;
            if (a[i] > b && l == -1)
                l = i;
        }
        for (int i = k + 1; i < n; i++)
        {
            if (a[i] == b && (r == -1 || a[r] != b))
                r = i;
            if (a[i] > b && r == -1)
                r = i;
        }
        
        int res = -1;
        if (l == -1 && r != -1)
            res = r;
        else if (l != -1 && r == -1)
            res = l;
        else
        {
            res = l;
            if (k - l > r - (k + 1))
                res = r;
        }
        if (res != -1)
        {
            a[res] = 0;
            res++;
        }
        cout << res << ' ';
        
    }
    cout << endl;
    return 0;
}