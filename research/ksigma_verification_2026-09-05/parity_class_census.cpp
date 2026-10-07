#include <algorithm>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <vector>

using u32 = std::uint32_t;
using u64 = std::uint64_t;
using u128 = unsigned __int128;

struct Entry { u64 h; u32 k; };

static std::vector<u32> odd_exponent_support(u32 k,
                                             const std::vector<u32>& least) {
  std::vector<u32> support;
  while (k > 1) {
    const u32 p = least[k];
    unsigned e = 0;
    do {
      k /= p;
      ++e;
    } while (k > 1 && least[k] == p);
    if (e & 1U) support.push_back(p);
  }
  return support;
}

int main(int argc, char** argv) {
  const u32 limit = argc > 1
      ? static_cast<u32>(std::strtoull(argv[1], nullptr, 10))
      : 10000000;
  const u64 target_limit = static_cast<u64>(limit) * limit;
  std::vector<u32> least(limit), prime_power(limit, 1), primes;
  std::vector<u64> sigma(limit);
  sigma[1] = 1;
  for (u32 i = 2; i < limit; ++i) {
    if (!least[i]) {
      least[i] = i;
      prime_power[i] = i;
      sigma[i] = static_cast<u64>(i) + 1;
      primes.push_back(i);
    }
    for (u32 p : primes) {
      const u64 z = static_cast<u64>(i) * p;
      if (z >= limit || p > least[i]) break;
      const u32 ip = static_cast<u32>(z);
      least[ip] = p;
      if (p == least[i]) {
        prime_power[ip] = prime_power[i] * p;
        const u32 core = i / prime_power[i];
        sigma[ip] = sigma[i] + sigma[core] * prime_power[ip];
      } else {
        prime_power[ip] = p;
        sigma[ip] = sigma[i] * (static_cast<u64>(p) + 1);
      }
    }
  }

  std::vector<Entry> values;
  values.reserve(limit);
  for (u32 k = 1; k < limit; ++k) {
    const u128 h = static_cast<u128>(k) * sigma[k];
    if (h <= target_limit) values.push_back({static_cast<u64>(h), k});
  }
  std::sort(values.begin(), values.end(), [](const Entry& x, const Entry& y) {
    return x.h < y.h || (x.h == y.h && x.k < y.k);
  });

  u64 collision_pairs = 0;
  u64 equal_parity_pairs = 0;
  for (std::size_t i = 0; i < values.size();) {
    std::size_t j = i + 1;
    while (j < values.size() && values[j].h == values[i].h) ++j;
    for (std::size_t a = i; a < j; ++a) {
      const auto left = odd_exponent_support(values[a].k, least);
      for (std::size_t b = a + 1; b < j; ++b) {
        ++collision_pairs;
        if (left == odd_exponent_support(values[b].k, least)) {
          ++equal_parity_pairs;
          std::cout << "equal_parity_collision n=" << values[i].h
                    << " k=" << values[a].k << ',' << values[b].k
                    << " odd_exponent_support=";
          for (u32 p : left) std::cout << p << ',';
          std::cout << '\n';
          return 1;
        }
      }
    }
    i = j;
  }
  std::cout << "K=" << limit << " retained=" << values.size()
            << " collision_pairs=" << collision_pairs
            << " equal_parity_pairs=" << equal_parity_pairs << '\n';
  return 0;
}
