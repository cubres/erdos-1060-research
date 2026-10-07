#include <algorithm>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <string>
#include <vector>

using u32 = std::uint32_t;
using u64 = std::uint64_t;
using u128 = unsigned __int128;

struct Entry {
  u128 h;
  u32 root;
};

static std::string decimal(u128 x) {
  if (x == 0) return "0";
  std::string out;
  while (x) {
    out.push_back(static_cast<char>('0' + x % 10));
    x /= 10;
  }
  std::reverse(out.begin(), out.end());
  return out;
}

static u128 power(u128 base, unsigned exponent) {
  u128 result = 1;
  while (exponent) {
    if (exponent & 1U) result *= base;
    exponent >>= 1U;
    if (exponent) base *= base;
  }
  return result;
}

int main(int argc, char** argv) {
  const u32 limit = argc > 1
      ? static_cast<u32>(std::strtoull(argv[1], nullptr, 10))
      : 10000000;

  std::vector<u32> least(limit + 1), primes;
  for (u32 i = 2; i <= limit; ++i) {
    if (!least[i]) {
      least[i] = i;
      primes.push_back(i);
    }
    for (u32 p : primes) {
      const u64 product = static_cast<u64>(i) * p;
      if (product > limit || p > least[i]) break;
      least[static_cast<u32>(product)] = p;
    }
  }

  std::vector<Entry> values;
  values.reserve((limit + 1) / 2);
  for (u32 root = 1; root <= limit; root += 2) {
    u32 remaining = root;
    u128 h = 1;
    while (remaining > 1) {
      const u32 p = least[remaining];
      unsigned exponent = 0;
      do {
        remaining /= p;
        ++exponent;
      } while (remaining > 1 && least[remaining] == p);

      const unsigned square_exponent = 2 * exponent;
      const u128 prime_power = power(p, square_exponent);
      u128 sigma = 1;
      u128 term = 1;
      for (unsigned j = 0; j < square_exponent; ++j) {
        term *= p;
        sigma += term;
      }
      h *= prime_power * sigma;
    }
    values.push_back({h, root});
  }

  std::sort(values.begin(), values.end(), [](const Entry& a, const Entry& b) {
    return a.h < b.h || (a.h == b.h && a.root < b.root);
  });
  u64 collisions = 0;
  for (std::size_t i = 1; i < values.size(); ++i) {
    if (values[i - 1].h == values[i].h) {
      ++collisions;
      std::cout << "collision roots=" << values[i - 1].root << ','
                << values[i].root << " inputs="
                << static_cast<u64>(values[i - 1].root) * values[i - 1].root
                << ',' << static_cast<u64>(values[i].root) * values[i].root
                << " h=" << decimal(values[i].h) << '\n';
      break;
    }
  }
  std::cout << "odd_roots_checked=" << values.size()
            << " root_limit=" << limit
            << " collisions=" << collisions << '\n';
  return collisions ? 1 : 0;
}
