#include "testlib.h"
#include <cassert>
#include <vector>

using std::vector;

const long long MAX_T = static_cast<long long>(3e18);

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

void verify(InStream& in_stream, TResult fail_res, const vector<long long>& a, const vector<int>& pos, long long t) {
    int n = a.size();
    vector<long long> b(n);
    for (int i = 0; i < n; i++) {
        b[i] = in_stream.readLong(1, MAX_T, "B");
        if (i != 0 && b[i - 1] >= b[i])
            quitf(fail_res, "The output array B must be strictly increasing, but it's not for the position %d.", i); 
    }
    if (get_pos(a, b, t) != pos)
        quitf(fail_res, "The answer for the given A, B and T is different from the desired result.");
}

int main(int argc, char* argv[]) {
    registerTestlibCmd(argc, argv);
    
    int n = inf.readInt();
    long long t = inf.readLong();
    vector<long long> a(n);
    for (auto& x : a)
        x = inf.readLong();
    vector<int> pos(n);
    for (auto & x : pos) {
        x = inf.readInt();
        x--;
    }

    auto j_ans = ans.readToken("Yes|No");
    auto p_ans = ouf.readToken("Yes|No");
    if (j_ans == "Yes") {
        verify(ans, _fail, a, pos, t);
    }
    if (p_ans == "Yes") {
        verify(ouf, _wa, a, pos, t);
    }
    if (j_ans == p_ans)
        quitf(_ok, "");
    if (j_ans == "No") 
        quitf(_fail, "The participant has an answer, but the jury doesn't.");
    quitf(_wa, "The jury has an answer, but the participant doesn't.");
}
