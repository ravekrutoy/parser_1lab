#include <cassert>
#include <iostream>
#include <vector>

using std::vector;
using std::cin;
using std::cout;
using std::min;

vector<int> get_pos(const vector<long long>& a, const vector<long long>& b, long long t) {
    assert(a.size() == b.size());
    int n = a.size();
    vector<int> pos(n);
    for (int i = 0; i < n; i++) {
        int j = i + 1;
        while (j < n && a[j] + t <= b[j - 1])
            j++;
        pos[i] = j - 1;
    }
    return pos;
}

vector<long long> get_ans(const vector<long long>& a, const vector<int>& pos, long long t) {
    int n = a.size();
    vector<bool> bad(n, false);
    for (int i = 0; i < n; i++) {
        int p = pos[i] + 1;
        if (p != n)
            bad[p] = true;
    }
    vector<long long> b(n);
    b.back() = a.back() + t + n;
    for (int i = n - 2; i >= 0; i--) {
        if (bad[i + 1])
            b[i] = min(b[i + 1] - 1, a[i + 1] + t - 1);
        else 
            b[i] = b[i + 1] - 1;
    }
    return b;
}

vector<long long> solve(const vector<long long>& a, const vector<int>& pos, long long t) {
    auto b = get_ans(a, pos, t);
    int n = a.size();
    for (int i = 0; i < n; i++)
        if (a[i] + t > b[i])
            return {};
    for (int i = 1; i < n; i++)
        if (b[i] <= b[i - 1])
            return {};
    auto ans_pos = get_pos(a, b, t);
    return ans_pos == pos ? b : std::vector<long long>{};
}

int non_trivial = 0;

int stress() {
    int n = rand() % 10 + 1;
    vector<long long> a(n);
    a[0] = 1;
    for (int i = 1; i < n; i++)
        a[i] = a[i - 1] + rand() % 2 + 1;
    int t = rand() % 10 + 1;
    vector<long long> b(n);
    b.back() = a.back() + t + rand() % n;
    for (int i = n - 2; i >= 0; i--)
        if (rand() % 2 != 0)
            b[i] = b[i + 1] - 1;
        else
            b[i] = min(b[i + 1] - 1, a[i + 1] + t - 1);
    for (int i = 1; i < n; i++)
        if (b[i] <= b[i - 1])
            return 0;
    for (int i = 0; i < n; i++)
        if (a[i] + t > b[i])
            return 0;
    auto pp = get_pos(a, b, t);
    if (pp[0] != n - 1 && pp[0] > 0)
        non_trivial++;
    auto bb = solve(a, get_pos(a, b, t), t);
    assert(!bb.empty());
    return 1;
}

int main() {
    std::ios_base::sync_with_stdio(0);
    cin.tie(nullptr);
    int n;
    cin >> n;
    long long t;
    cin >> t;
    vector<long long> a(n);
    for (auto& x : a)
        cin >> x;
    vector<int> pos(n);
    for (auto& x : pos) {
        cin >> x;
        x--;
    }

    auto b = solve(a, pos, t);
    if (b.empty()) {
        cout << "No\n";
        return 0;
    }
    cout << "Yes\n";
    for (auto x : b)
        cout << x << " ";
    cout << "\n";
}
