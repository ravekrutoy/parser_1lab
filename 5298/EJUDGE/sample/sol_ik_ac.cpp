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
    int last_bad = n;
    vector<int> pos(n);
    for (int i = n - 1; i >= 0; i--) {
         pos[i] = last_bad - 1;
         if (i != 0 && a[i] + t > b[i - 1])
             last_bad = i;
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
            b[i] = a[i + 1] + t - 1;
        else 
            b[i] = b[i + 1] - 1;
    }
    return b;
}

vector<long long> solve(const vector<long long>& a, const vector<int>& pos, long long t) {
    auto b = get_ans(a, pos, t);
    for (int i = 1; i < (int)a.size(); i++)
        if (b[i] <= b[i - 1])
            return {};
    auto ans_pos = get_pos(a, b, t);
    return ans_pos == pos ? b : std::vector<long long>{};
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
