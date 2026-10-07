#include <algorithm>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <vector>

using u32 = std::uint32_t;
using u64 = std::uint64_t;
using u128 = unsigned __int128;

struct Entry { u64 h; u32 k; };

static std::vector<unsigned char> exponent_pattern(u32 k,
                                                   const std::vector<u32>& least,
                                                   bool powerful_only) {
  std::vector<unsigned char> pattern;
  while (k > 1) {
    const u32 p = least[k];
    unsigned e = 0;
    do { k /= p; ++e; } while (k > 1 && least[k] == p);
    if (!powerful_only || e >= 2) pattern.push_back(static_cast<unsigned char>(e));
  }
  std::sort(pattern.begin(), pattern.end());
  return pattern;
}

int main(int argc, char** argv) {
  const u32 K = argc > 1 ? static_cast<u32>(std::strtoull(argv[1], nullptr, 10))
                         : 10000000;
  const u64 X = static_cast<u64>(K) * K;
  std::vector<u32> least(K), prime_power(K, 1), primes;
  std::vector<u64> sigma(K); sigma[1] = 1;
  for (u32 i = 2; i < K; ++i) {
    if (!least[i]) {
      least[i] = i;
      prime_power[i] = i;
      sigma[i] = static_cast<u64>(i) + 1;
      primes.push_back(i);
    }
    for (u32 p : primes) {
      const u64 z = static_cast<u64>(i) * p;
      if (z >= K || p > least[i]) break;
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
  values.reserve(K);
  for (u32 k = 1; k < K; ++k) {
    const u128 h = static_cast<u128>(k) * sigma[k];
    if (h <= X) values.push_back({static_cast<u64>(h), k});
  }
  std::sort(values.begin(), values.end(), [](const Entry& a, const Entry& b) {
    return a.h < b.h || (a.h == b.h && a.k < b.k);
  });

  u64 collision_fibers = 0, pairs = 0;
  u64 equal_full = 0, equal_powerful = 0;
  bool printed_full = false, printed_powerful = false;
  for (std::size_t i = 0; i < values.size();) {
    std::size_t j = i + 1;
    while (j < values.size() && values[j].h == values[i].h) ++j;
    if (j - i >= 2) {
      ++collision_fibers;
      std::vector<std::vector<unsigned char>> full(j - i), powerful(j - i);
      for (std::size_t a = 0; a < j - i; ++a) {
        full[a] = exponent_pattern(values[i + a].k, least, false);
        powerful[a] = exponent_pattern(values[i + a].k, least, true);
      }
      for (std::size_t a = 0; a < j - i; ++a) {
        for (std::size_t b = a + 1; b < j - i; ++b) {
          ++pairs;
          if (full[a] == full[b]) {
            ++equal_full;
            if (!printed_full) {
              printed_full = true;
              std::cout << "first_equal_full_pattern n=" << values[i].h
                        << " k=" << values[i + a].k << ',' << values[i + b].k
                        << " pattern=";
              for (auto e : full[a]) std::cout << static_cast<unsigned>(e) << ',';
              std::cout << '\n';
            }
          }
          if (powerful[a] == powerful[b]) {
            ++equal_powerful;
            if (!printed_powerful) {
              printed_powerful = true;
              std::cout << "first_equal_powerful_pattern n=" << values[i].h
                        << " k=" << values[i + a].k << ',' << values[i + b].k
                        << " pattern=";
              for (auto e : powerful[a]) std::cout << static_cast<unsigned>(e) << ',';
              std::cout << '\n';
            }
          }
        }
      }
    }
    i = j;
  }
  std::cout << "K=" << K << " X=" << X << " retained=" << values.size()
            << " collision_fibers=" << collision_fibers << " pairs=" << pairs
            << " equal_full_pattern_pairs=" << equal_full
            << " equal_powerful_pattern_pairs=" << equal_powerful << '\n';
}
