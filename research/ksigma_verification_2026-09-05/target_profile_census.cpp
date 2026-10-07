#include <algorithm>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <vector>

using u32 = std::uint32_t;
using u64 = std::uint64_t;
using u128 = unsigned __int128;

struct Entry { u64 h; u32 k; };

// For a fixed target n=h(k), equality of the full histograms
//   {(v_p(n),v_p(k)): p|n}
// is equivalent to equality of the following positive part: primes with
// v_p(k)>0.  Indeed, for every a, the number of omitted (a,0) pairs is the
// fixed number #{p:v_p(n)=a} minus the number of displayed pairs (a,b), b>0.
using Profile = std::vector<std::pair<unsigned char, unsigned char>>;

int main(int argc, char** argv) {
  const u32 K = argc > 1
      ? static_cast<u32>(std::strtoull(argv[1], nullptr, 10))
      : 100000000;
  const u64 X = argc > 2
      ? static_cast<u64>(std::strtoull(argv[2], nullptr, 10))
      : 10000000000000000ULL;

  std::vector<u32> least(K), prime_power(K, 1), primes;
  std::vector<u64> sigma(K);
  sigma[1] = 1;
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
  std::sort(values.begin(), values.end(), [](const Entry& x, const Entry& y) {
    return x.h < y.h || (x.h == y.h && x.k < y.k);
  });

  auto profile = [&](u32 k, u64 h) {
    Profile answer;
    while (k > 1) {
      const u32 p = least[k];
      unsigned b = 0;
      do {
        k /= p;
        ++b;
      } while (k > 1 && least[k] == p);
      u64 remaining = h;
      unsigned a = 0;
      while (remaining % p == 0) {
        remaining /= p;
        ++a;
      }
      if (a > 255 || b > 255 || a < b) {
        std::cerr << "exponent encoding failure\n";
        std::exit(2);
      }
      answer.push_back({static_cast<unsigned char>(a),
                        static_cast<unsigned char>(b)});
    }
    std::sort(answer.begin(), answer.end());
    return answer;
  };

  u64 fibers = 0, pairs = 0, equal_profile_pairs = 0;
  std::size_t maximum_fiber = 1;
  bool printed = false;
  for (std::size_t i = 0; i < values.size();) {
    std::size_t j = i + 1;
    while (j < values.size() && values[j].h == values[i].h) ++j;
    if (j - i >= 2) {
      ++fibers;
      maximum_fiber = std::max(maximum_fiber, j - i);
      std::vector<Profile> profiles;
      profiles.reserve(j - i);
      for (std::size_t t = i; t < j; ++t) {
        profiles.push_back(profile(values[t].k, values[t].h));
      }
      for (std::size_t a = 0; a < profiles.size(); ++a) {
        for (std::size_t b = a + 1; b < profiles.size(); ++b) {
          ++pairs;
          if (profiles[a] == profiles[b]) {
            ++equal_profile_pairs;
            if (!printed) {
              printed = true;
              std::cout << "first_equal_target_profile n=" << values[i].h
                        << " k=" << values[i+a].k << "," << values[i+b].k
                        << " positive_profile=";
              for (auto [target_exp, input_exp] : profiles[a]) {
                std::cout << "(" << static_cast<unsigned>(target_exp) << ","
                          << static_cast<unsigned>(input_exp) << ")";
              }
              std::cout << "\n";
            }
          }
        }
      }
    }
    i = j;
  }
  std::cout << "K=" << K << " X=" << X << " retained=" << values.size()
            << " collision_fibers=" << fibers << " collision_pairs=" << pairs
            << " maximum_fiber=" << maximum_fiber
            << " equal_target_profile_pairs=" << equal_profile_pairs << "\n";
}
