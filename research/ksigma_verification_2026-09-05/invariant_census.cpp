#include <algorithm>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <limits>
#include <numeric>
#include <vector>

using u32 = std::uint32_t;
using u64 = std::uint64_t;
using u128 = unsigned __int128;

struct Entry { u64 h; u32 k; };
struct Invariant {
  u64 radical;
  unsigned omega_powerful;
  std::vector<unsigned char> exponent_multiset;
  std::vector<unsigned char> repeated_exponent_multiset;
  unsigned number_of_ones;
  u64 gcd_with_sigma;
};

int main(int argc, char** argv) {
  const u32 K = argc > 1 ? static_cast<u32>(std::strtoull(argv[1], nullptr, 10)) : 10000000;
  const u64 X = static_cast<u64>(K) * K;
  std::vector<u32> least(K), prime_power(K, 1), primes;
  std::vector<u64> sigma(K); sigma[1] = 1;
  for (u32 i = 2; i < K; ++i) {
    if (!least[i]) {
      least[i] = i; prime_power[i] = i; sigma[i] = static_cast<u64>(i) + 1;
      primes.push_back(i);
    }
    for (u32 p : primes) {
      u64 z = static_cast<u64>(i) * p;
      if (z >= K || p > least[i]) break;
      u32 ip = static_cast<u32>(z); least[ip] = p;
      if (p == least[i]) {
        prime_power[ip] = prime_power[i] * p;
        u32 core = i / prime_power[i];
        sigma[ip] = sigma[i] + sigma[core] * prime_power[ip];
      } else {
        prime_power[ip] = p;
        sigma[ip] = sigma[i] * (static_cast<u64>(p) + 1);
      }
    }
  }
  std::vector<Entry> values; values.reserve(K);
  for (u32 k = 1; k < K; ++k) {
    u128 h = static_cast<u128>(k) * sigma[k];
    if (h <= X) values.push_back({static_cast<u64>(h), k});
  }
  std::sort(values.begin(), values.end(), [](const Entry& a, const Entry& b) {
    return a.h < b.h || (a.h == b.h && a.k < b.k);
  });
  auto invariant = [&](u32 k) {
    u64 radical = 1; unsigned omega = 0, ones = 0;
    std::vector<unsigned char> exponents, repeated;
    while (k > 1) {
      u32 p = least[k]; unsigned e = 0;
      do { k /= p; ++e; } while (k > 1 && least[k] == p);
      radical *= p;
      exponents.push_back(static_cast<unsigned char>(e));
      if (e >= 2) { omega += e; repeated.push_back(static_cast<unsigned char>(e)); }
      else ++ones;
    }
    std::sort(exponents.begin(), exponents.end());
    std::sort(repeated.begin(), repeated.end());
    return Invariant{radical, omega, std::move(exponents), std::move(repeated), ones, 0};
  };

  u64 fibers = 0, pairs = 0, equal_radical = 0, equal_omega = 0;
  u64 equal_exponent_multiset = 0, equal_repeated_multiset = 0;
  u64 equal_gcd_sigma = 0, equal_signature_and_gcd = 0;
  bool printed_radical = false, printed_omega = false, printed_exponents = false;
  bool printed_repeated = false;
  for (std::size_t i = 0; i < values.size();) {
    std::size_t j = i + 1;
    while (j < values.size() && values[j].h == values[i].h) ++j;
    if (j - i >= 2) {
      ++fibers;
      std::vector<Invariant> inv(j-i);
      for (std::size_t a=0; a<inv.size(); ++a) {
        inv[a]=invariant(values[i+a].k);
        inv[a].gcd_with_sigma=std::gcd<u64>(values[i+a].k,sigma[values[i+a].k]);
      }
      for (std::size_t a=0; a<inv.size(); ++a) for (std::size_t b=a+1; b<inv.size(); ++b) {
        ++pairs;
        if (inv[a].radical == inv[b].radical) {
          ++equal_radical;
          if (!printed_radical) {
            printed_radical=true;
            std::cout << "first_equal_radical n=" << values[i].h << " k="
                      << values[i+a].k << "," << values[i+b].k
                      << " rad=" << inv[a].radical << "\n";
          }
        }
        if (inv[a].omega_powerful == inv[b].omega_powerful) {
          ++equal_omega;
          if (!printed_omega) {
            printed_omega=true;
            std::cout << "first_equal_omegaF n=" << values[i].h << " k="
                      << values[i+a].k << "," << values[i+b].k
                      << " omegaF=" << inv[a].omega_powerful << "\n";
          }
        }
        if (inv[a].exponent_multiset == inv[b].exponent_multiset) {
          ++equal_exponent_multiset;
          if (!printed_exponents) {
            printed_exponents=true;
            std::cout << "first_equal_exponent_multiset n=" << values[i].h << " k="
                      << values[i+a].k << "," << values[i+b].k << " exponents=";
            for (auto e:inv[a].exponent_multiset) std::cout << static_cast<unsigned>(e) << ",";
            std::cout << "\n";
          }
        }
        if (inv[a].repeated_exponent_multiset == inv[b].repeated_exponent_multiset) {
          ++equal_repeated_multiset;
          if (!printed_repeated) {
            printed_repeated=true;
            std::cout << "first_equal_repeated_exponent_multiset n=" << values[i].h << " k="
                      << values[i+a].k << "," << values[i+b].k << " repeated=";
            for (auto e:inv[a].repeated_exponent_multiset) std::cout << static_cast<unsigned>(e) << ",";
            std::cout << " ones=" << inv[a].number_of_ones << "," << inv[b].number_of_ones << "\n";
          }
        }
        if (inv[a].gcd_with_sigma == inv[b].gcd_with_sigma) {
          ++equal_gcd_sigma;
          if (equal_gcd_sigma==1) std::cout << "first_equal_gcd_sigma n="<<values[i].h<<" k="<<values[i+a].k<<","<<values[i+b].k<<" gcd="<<inv[a].gcd_with_sigma<<"\n";
        }
        if (inv[a].gcd_with_sigma == inv[b].gcd_with_sigma &&
            inv[a].exponent_multiset == inv[b].exponent_multiset) {
          ++equal_signature_and_gcd;
          if (equal_signature_and_gcd==1) std::cout << "first_equal_signature_and_gcd n="<<values[i].h<<" k="<<values[i+a].k<<","<<values[i+b].k<<" gcd="<<inv[a].gcd_with_sigma<<"\n";
        }
      }
    }
    i = j;
  }
  std::cout << "K=" << K << " X=" << X << " retained=" << values.size()
            << " collision_fibers=" << fibers << " pairs=" << pairs
            << " equal_radical_pairs=" << equal_radical
            << " equal_omegaF_pairs=" << equal_omega
            << " equal_exponent_multiset_pairs=" << equal_exponent_multiset
            << " equal_repeated_multiset_pairs=" << equal_repeated_multiset
            << " equal_gcd_sigma_pairs=" << equal_gcd_sigma
            << " equal_signature_and_gcd_pairs=" << equal_signature_and_gcd << "\n";
}
