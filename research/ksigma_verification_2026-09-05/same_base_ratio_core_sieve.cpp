// Exact support/leaf-peeling census for
//   R_p = H(p,2)/H(p,1) = p (p^2+p+1)/(p+1),  p prime <= U.
//
// Phi_3(p) is factored for all p simultaneously.  A prime q != 3 divides
// x^2+x+1 iff q == 1 (mod 3) and x is one of the two nontrivial cube roots
// modulo q.  After sieving by every q<=U, the residual is either 1 or one
// prime >U: two factors >U would have product >(U+1)^2, larger than
// p^2+p+1 for p<=U.  Thus the support calculation is exact.

#include <algorithm>
#include <cstdint>
#include <cstdlib>
#include <deque>
#include <iostream>
#include <limits>
#include <string>
#include <unordered_map>
#include <utility>
#include <vector>

using u64 = std::uint64_t;
using u128 = __uint128_t;

static u64 mul_mod(u64 a, u64 b, u64 m) { return (u128)a * b % m; }

static u64 pow_mod(u64 a, u64 e, u64 m) {
  u64 answer = 1;
  while (e) {
    if (e & 1) answer = mul_mod(answer, a, m);
    a = mul_mod(a, a, m);
    e >>= 1;
  }
  return answer;
}

// Tonelli-Shanks.  The caller only asks for values known to be quadratic
// residues; UINT64_MAX is returned defensively on failure.
static u64 sqrt_mod_prime(u64 n, u64 p) {
  n %= p;
  if (n == 0) return 0;
  if (p == 2) return n;
  if (pow_mod(n, (p - 1) / 2, p) != 1)
    return std::numeric_limits<u64>::max();
  if (p % 4 == 3) return pow_mod(n, (p + 1) / 4, p);
  u64 q = p - 1, s = 0;
  while ((q & 1) == 0) q >>= 1, ++s;
  u64 z = 2;
  while (pow_mod(z, (p - 1) / 2, p) != p - 1) ++z;
  u64 c = pow_mod(z, q, p);
  u64 x = pow_mod(n, (q + 1) / 2, p);
  u64 t = pow_mod(n, q, p);
  u64 m = s;
  while (t != 1) {
    u64 i = 1, t2 = mul_mod(t, t, p);
    while (i < m && t2 != 1) t2 = mul_mod(t2, t2, p), ++i;
    if (i == m) return std::numeric_limits<u64>::max();
    u64 b = pow_mod(c, u64(1) << (m - i - 1), p);
    x = mul_mod(x, b, p);
    c = mul_mod(b, b, p);
    t = mul_mod(t, c, p);
    m = i;
  }
  return x;
}

int main(int argc, char** argv) {
  int U = argc >= 2 ? std::stoi(argv[1]) : 10000000;
  if (U < 2) return 2;

  // Linear sieve: lp[n] is the least prime divisor.
  std::vector<int> lp(U + 2, 0), primes;
  primes.reserve(U / 10);
  for (int i = 2; i <= U + 1; ++i) {
    if (!lp[i]) lp[i] = i, primes.push_back(i);
    for (int q : primes) {
      long long x = 1LL * q * i;
      if (x > U + 1 || q > lp[i]) break;
      lp[x] = q;
    }
  }
  std::vector<int> bases;
  for (int p : primes)
    if (p <= U) bases.push_back(p);
  const int column_count = (int)bases.size();
  std::vector<int> index(U + 1, -1);
  std::vector<u64> residual(U + 1, 0);
  std::vector<std::vector<u64>> support(column_count);
  for (int j = 0; j < column_count; ++j) {
    int p = bases[j];
    index[p] = j;
    residual[p] = u64(p) * p + p + 1;
    support[j].push_back(p);
    int x = p + 1;
    while (x > 1) {
      int q = lp[x];
      support[j].push_back(q);
      while (x % q == 0) x /= q;
    }
  }

  auto divide_progression = [&](u64 q, u64 root) {
    for (u64 x = root; x <= (u64)U; x += q) {
      int j = index[x];
      if (j < 0 || residual[x] % q) continue;
      support[j].push_back(q);
      do residual[x] /= q; while (residual[x] % q == 0);
    }
  };

  // q=3 has the single (double) root 1.
  divide_progression(3, 1);
  for (int qi : bases) {
    u64 q = qi;
    if (q <= 3 || q % 3 != 1) continue;
    u64 minus_three = q - 3;
    u64 square_root = sqrt_mod_prime(minus_three, q);
    if (square_root == std::numeric_limits<u64>::max()) {
      std::cerr << "Tonelli failure at q=" << q << "\n";
      return 3;
    }
    u64 inverse_two = (q + 1) / 2;
    u64 root1 = mul_mod((square_root + q - 1) % q, inverse_two, q);
    u64 root2 = (q - 1 - root1) % q;
    if ((mul_mod(root1, root1, q) + root1 + 1) % q != 0 ||
        (mul_mod(root2, root2, q) + root2 + 1) % q != 0) {
      std::cerr << "root verification failure at q=" << q << "\n";
      return 4;
    }
    divide_progression(q, root1);
    if (root2 != root1) divide_progression(q, root2);
  }

  for (int j = 0; j < column_count; ++j) {
    int p = bases[j];
    if (residual[p] > 1) support[j].push_back(residual[p]);
    std::sort(support[j].begin(), support[j].end());
    support[j].erase(std::unique(support[j].begin(), support[j].end()),
                     support[j].end());
  }

  std::unordered_map<u64, int> row_id;
  row_id.reserve(4 * column_count);
  std::vector<std::vector<int>> incidence;
  for (int j = 0; j < column_count; ++j) {
    for (u64 q : support[j]) {
      auto [it, inserted] = row_id.emplace(q, (int)incidence.size());
      if (inserted) incidence.emplace_back();
      incidence[it->second].push_back(j);
    }
  }
  std::vector<int> degree(incidence.size());
  std::deque<int> queue;
  for (int r = 0; r < (int)incidence.size(); ++r) {
    degree[r] = (int)incidence[r].size();
    if (degree[r] == 1) queue.push_back(r);
  }
  std::vector<char> active(column_count, 1);
  int removed = 0;
  while (!queue.empty()) {
    int r = queue.front();
    queue.pop_front();
    if (degree[r] != 1) continue;
    int j = -1;
    for (int candidate : incidence[r])
      if (active[candidate]) { j = candidate; break; }
    if (j < 0) { degree[r] = 0; continue; }
    active[j] = 0;
    ++removed;
    for (u64 q : support[j]) {
      int s = row_id.find(q)->second;
      --degree[s];
      if (degree[s] == 1) queue.push_back(s);
    }
  }
  std::vector<int> core;
  for (int j = 0; j < column_count; ++j)
    if (active[j]) core.push_back(bases[j]);

  std::cout << "{\n"
            << "  \"prime_bound\": " << U << ",\n"
            << "  \"column_count\": " << column_count << ",\n"
            << "  \"valuation_row_count\": " << incidence.size() << ",\n"
            << "  \"peeled_column_count\": " << removed << ",\n"
            << "  \"core_column_count\": " << core.size() << ",\n"
            << "  \"empty_core\": " << (core.empty() ? "true" : "false") << ",\n"
            << "  \"core_bases_sample\": [";
  for (int i = 0; i < (int)core.size() && i < 50; ++i) {
    if (i) std::cout << ", ";
    std::cout << core[i];
  }
  std::cout << "]\n}\n";
}
