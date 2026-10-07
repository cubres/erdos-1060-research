#include <algorithm>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <limits>
#include <map>
#include <numeric>
#include <set>
#include <string>
#include <unordered_map>
#include <utility>
#include <vector>

using u32 = std::uint32_t;
using u64 = std::uint64_t;
using u128 = unsigned __int128;

struct Entry {
  u64 h;
  u32 k;
};

struct RatioWitness {
  std::size_t numerator = 0;
  u64 denominator = 1;
  u64 n = 0;
  std::vector<u32> ks;
};

static void update_ratio(RatioWitness& best, std::size_t numerator, u64 denominator,
                         u64 n, const std::vector<u32>& ks) {
  if (best.numerator == 0 ||
      static_cast<u128>(numerator) * best.denominator >
          static_cast<u128>(best.numerator) * denominator) {
    best = {numerator, denominator, n, ks};
  }
}

static std::string join(const std::vector<u32>& values) {
  std::string out = "{";
  for (std::size_t i = 0; i < values.size(); ++i) {
    if (i) out += ",";
    out += std::to_string(values[i]);
  }
  out += "}";
  return out;
}

static unsigned valuation(u32 n, u32 p) {
  unsigned e = 0;
  while (n % p == 0) {
    n /= p;
    ++e;
  }
  return e;
}

static std::vector<std::pair<u64, unsigned>> factor_from_primes(
    u64 n, const std::vector<u32>& primes) {
  std::vector<std::pair<u64, unsigned>> f;
  for (u32 p : primes) {
    if ((u64)p * p > n) break;
    if (n % p != 0) continue;
    unsigned e = 0;
    do {
      n /= p;
      ++e;
    } while (n % p == 0);
    f.push_back({p, e});
  }
  if (n > 1) f.push_back({n, 1});
  return f;
}

static u64 powerful_part(u32 n, const std::vector<u32>& lp) {
  u64 out = 1;
  while (n > 1) {
    const u32 p = lp[n];
    u64 pe = 1;
    unsigned e = 0;
    do {
      n /= p;
      pe *= p;
      ++e;
    } while (n > 1 && lp[n] == p);
    if (e >= 2) out *= pe;
  }
  return out;
}

static u64 repeated_prime_support(u32 n, const std::vector<u32>& lp) {
  u64 out = 1;
  while (n > 1) {
    const u32 p = lp[n];
    unsigned e = 0;
    do {
      n /= p;
      ++e;
    } while (n > 1 && lp[n] == p);
    if (e >= 2) out *= p;
  }
  return out;
}

static unsigned powerful_big_omega(u32 n, const std::vector<u32>& lp) {
  unsigned out = 0;
  while (n > 1) {
    const u32 p = lp[n];
    unsigned e = 0;
    do {
      n /= p;
      ++e;
    } while (n > 1 && lp[n] == p);
    if (e >= 2) out += e;
  }
  return out;
}

static unsigned repeated_prime_count(u32 n, const std::vector<u32>& lp) {
  unsigned out = 0;
  while (n > 1) {
    const u32 p = lp[n];
    unsigned e = 0;
    do {
      n /= p;
      ++e;
    } while (n > 1 && lp[n] == p);
    if (e >= 2) ++out;
  }
  return out;
}

static u64 radical(u32 n, const std::vector<u32>& lp) {
  u64 out = 1;
  while (n > 1) {
    const u32 p = lp[n];
    out *= p;
    do {
      n /= p;
    } while (n > 1 && lp[n] == p);
  }
  return out;
}

static std::map<u64, unsigned> factor_h(u32 k, u64 sigma_k,
                                        const std::vector<u32>& lp,
                                        const std::vector<u32>& primes) {
  std::map<u64, unsigned> out;
  u32 t = k;
  while (t > 1) {
    const u32 p = lp[t];
    unsigned e = 0;
    do {
      t /= p;
      ++e;
    } while (t > 1 && lp[t] == p);
    out[p] += e;
  }
  for (auto [p, e] : factor_from_primes(sigma_k, primes)) out[p] += e;
  return out;
}

int main(int argc, char** argv) {
  u32 K = 5'000'000;
  if (argc >= 2) {
    const unsigned long long parsed = std::strtoull(argv[1], nullptr, 10);
    if (parsed < 2 || parsed > std::numeric_limits<u32>::max()) {
      std::cerr << "K must be in [2, 2^32-1]\n";
      return 2;
    }
    K = static_cast<u32>(parsed);
  }
  const u64 X = static_cast<u64>(K) * K;
  const bool retain_all = argc >= 3 && std::string(argv[2]) == "all";

  // Linear sieve for exact sigma values on [1,K).
  std::vector<u32> lp(K, 0), prime_power(K, 1), primes;
  std::vector<u64> sigma(K, 0);
  sigma[1] = 1;
  for (u32 i = 2; i < K; ++i) {
    if (lp[i] == 0) {
      lp[i] = i;
      prime_power[i] = i;
      sigma[i] = static_cast<u64>(i) + 1;
      primes.push_back(i);
    }
    for (u32 p : primes) {
      const u64 ip64 = static_cast<u64>(i) * p;
      if (ip64 >= K || p > lp[i]) break;
      const u32 ip = static_cast<u32>(ip64);
      lp[ip] = p;
      if (p == lp[i]) {
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
  values.reserve(K - 1);
  for (u32 k = 1; k < K; ++k) {
    const u128 h128 = static_cast<u128>(k) * sigma[k];
    if (h128 > std::numeric_limits<u64>::max()) {
      std::cerr << "h(k) exceeds uint64 at k=" << k << "\n";
      return 4;
    }
    if (retain_all || h128 <= X) values.push_back({static_cast<u64>(h128), k});
  }
  std::sort(values.begin(), values.end(), [](const Entry& a, const Entry& b) {
    return a.h < b.h || (a.h == b.h && a.k < b.k);
  });

  std::map<std::size_t, u64> fiber_histogram;
  std::map<std::size_t, std::pair<u64, std::vector<u32>>> least_by_multiplicity;
  std::size_t max_mult = 0;
  u64 max_mult_count = 0;
  u64 collision_fibers = 0;
  u64 powerful_part_violations = 0;
  u64 repeated_support_collisions = 0;
  u64 radical_collisions = 0;
  u64 powerful_big_omega_collisions = 0;
  u64 repeated_prime_count_collisions = 0;
  u64 odd_collision_fibers = 0;
  u64 all_odd_argument_collision_fibers = 0;
  u64 f_gt_v2 = 0;
  u64 f_gt_omega = 0;
  u64 f_gt_Omega = 0;
  u64 f_gt_max_alpha = 0;
  u64 f_gt_product_alpha_minus_one = 0;
  std::string first_powerful_part_violation;
  std::string first_repeated_support_collision;
  std::string first_radical_collision;
  std::string first_powerful_big_omega_collision;
  std::string first_repeated_prime_count_collision;
  std::string first_odd_collision;
  std::string first_all_odd_argument_collision;
  std::string first_odd_pair_disjoint_from_315_351;
  std::string first_pair_avoiding_2_3_5_7;
  std::string first_coprime_pair;
  std::string first_coprime_pair_avoiding_2_3_5_7;
  std::string first_pair_coprime_to_6;
  std::string first_pair_coprime_to_2;
  std::string first_pair_coprime_to_3;
  std::string first_pair_coprime_to_5;
  std::string first_pair_coprime_to_7;
  std::string first_fiber_with_gcd_one;
  std::string first_v2_projection_collision;
  std::string first_v2_v3_projection_collision;
  std::string first_v2_v3_v5_projection_collision;
  std::string first_v2_plus_v3_collision;
  std::string first_2v2_plus_v3_collision;
  std::string first_v2_plus_2v3_collision;
  std::string first_f_gt_v2;
  std::string first_f_gt_omega;
  std::string first_f_gt_product_alpha_minus_one;
  std::map<std::size_t, std::pair<unsigned, u64>> minimum_v2_by_multiplicity;
  std::map<std::size_t, std::pair<unsigned, u64>> minimum_max_alpha_by_multiplicity;
  RatioWitness best_f_over_v2, best_f_over_max_alpha, best_f_over_omega;

  for (std::size_t i = 0; i < values.size();) {
    std::size_t j = i + 1;
    while (j < values.size() && values[j].h == values[i].h) ++j;
    const std::size_t mult = j - i;
    ++fiber_histogram[mult];
    std::vector<u32> ks;
    ks.reserve(mult);
    for (std::size_t z = i; z < j; ++z) ks.push_back(values[z].k);
    if (!least_by_multiplicity.count(mult)) {
      least_by_multiplicity[mult] = {values[i].h, ks};
    }
    if (mult > max_mult) {
      max_mult = mult;
      max_mult_count = 1;
    } else if (mult == max_mult) {
      ++max_mult_count;
    }

    if (mult >= 2) {
      ++collision_fibers;
      if (values[i].h & 1) {
        ++odd_collision_fibers;
        if (first_odd_collision.empty()) {
          first_odd_collision = "n=" + std::to_string(values[i].h) + " k=" + join(ks);
        }
      }
      std::unordered_map<u64, u32> seen_full, seen_support, seen_radical;
      std::unordered_map<unsigned, u32> seen_full_Omega, seen_repeated_count;
      std::unordered_map<unsigned, u32> seen_v2, seen_v2_v3, seen_v2_v3_v5;
      std::unordered_map<unsigned, u32> seen_sum23, seen_2e2_e3, seen_e2_2e3;
      std::vector<u32> odd_ks;
      std::vector<u64> radicals;
      for (u32 k : ks) {
        if (k & 1) odd_ks.push_back(k);
        const u64 full = powerful_part(k, lp);
        const u64 support = repeated_prime_support(k, lp);
        const u64 rad = radical(k, lp);
        radicals.push_back(rad);
        const unsigned full_Omega = powerful_big_omega(k, lp);
        const unsigned repeated_count = repeated_prime_count(k, lp);
        const unsigned e2 = valuation(k, 2);
        const unsigned e3 = valuation(k, 3);
        const unsigned e5 = valuation(k, 5);
        const unsigned key23 = e2 * 64 + e3;
        const unsigned key235 = key23 * 64 + e5;
        auto projection_witness = [&](u32 previous, const char* label) {
          return "n=" + std::to_string(values[i].h) + " k={" +
              std::to_string(previous) + "," + std::to_string(k) + "} " + label;
        };
        auto [p2it, p2ins] = seen_v2.emplace(e2, k);
        if (!p2ins && first_v2_projection_collision.empty()) {
          first_v2_projection_collision = projection_witness(
              p2it->second, ("v2=" + std::to_string(e2)).c_str());
        }
        auto [p23it, p23ins] = seen_v2_v3.emplace(key23, k);
        if (!p23ins && first_v2_v3_projection_collision.empty()) {
          const std::string label = "(v2,v3)=(" + std::to_string(e2) + "," +
              std::to_string(e3) + ")";
          first_v2_v3_projection_collision = projection_witness(p23it->second, label.c_str());
        }
        auto [p235it, p235ins] = seen_v2_v3_v5.emplace(key235, k);
        if (!p235ins && first_v2_v3_v5_projection_collision.empty()) {
          const std::string label = "(v2,v3,v5)=(" + std::to_string(e2) + "," +
              std::to_string(e3) + "," + std::to_string(e5) + ")";
          first_v2_v3_v5_projection_collision =
              projection_witness(p235it->second, label.c_str());
        }
        auto check_scalar = [&](std::unordered_map<unsigned, u32>& seen,
                                unsigned value, std::string& first,
                                const std::string& label) {
          auto [it, inserted] = seen.emplace(value, k);
          if (!inserted && first.empty()) {
            first = projection_witness(it->second, label.c_str());
          }
        };
        check_scalar(seen_sum23, e2 + e3, first_v2_plus_v3_collision,
                     "v2+v3=" + std::to_string(e2 + e3));
        check_scalar(seen_2e2_e3, 2 * e2 + e3, first_2v2_plus_v3_collision,
                     "2v2+v3=" + std::to_string(2 * e2 + e3));
        check_scalar(seen_e2_2e3, e2 + 2 * e3, first_v2_plus_2v3_collision,
                     "v2+2v3=" + std::to_string(e2 + 2 * e3));
        auto [fit, fins] = seen_full.emplace(full, k);
        if (!fins) {
          ++powerful_part_violations;
          if (first_powerful_part_violation.empty()) {
            first_powerful_part_violation = "n=" + std::to_string(values[i].h) +
                " k={" + std::to_string(fit->second) + "," + std::to_string(k) +
                "} full=" + std::to_string(full);
          }
        }
        auto [sit, sins] = seen_support.emplace(support, k);
        if (!sins) {
          ++repeated_support_collisions;
          if (first_repeated_support_collision.empty()) {
            first_repeated_support_collision = "n=" + std::to_string(values[i].h) +
                " k={" + std::to_string(sit->second) + "," + std::to_string(k) +
                "} repeated_support=" + std::to_string(support);
          }
        }
        auto [rit, rins] = seen_radical.emplace(rad, k);
        if (!rins) {
          ++radical_collisions;
          if (first_radical_collision.empty()) {
            first_radical_collision = "n=" + std::to_string(values[i].h) +
                " k={" + std::to_string(rit->second) + "," + std::to_string(k) +
                "} radical=" + std::to_string(rad);
          }
        }
        auto [oit, oins] = seen_full_Omega.emplace(full_Omega, k);
        if (!oins) {
          ++powerful_big_omega_collisions;
          if (first_powerful_big_omega_collision.empty()) {
            first_powerful_big_omega_collision =
                "n=" + std::to_string(values[i].h) + " k={" +
                std::to_string(oit->second) + "," + std::to_string(k) +
                "} Omega(full)=" + std::to_string(full_Omega);
          }
        }
        auto [cit, cins] = seen_repeated_count.emplace(repeated_count, k);
        if (!cins) {
          ++repeated_prime_count_collisions;
          if (first_repeated_prime_count_collision.empty()) {
            first_repeated_prime_count_collision =
                "n=" + std::to_string(values[i].h) + " k={" +
                std::to_string(cit->second) + "," + std::to_string(k) +
                "} omega(full)=" + std::to_string(repeated_count);
          }
        }
      }
      constexpr u64 small_support = 2ULL * 3 * 5 * 7;
      u32 fiber_gcd = 0;
      for (u32 k : ks) fiber_gcd = std::gcd(fiber_gcd, k);
      if (fiber_gcd == 1 && first_fiber_with_gcd_one.empty()) {
        first_fiber_with_gcd_one =
            "n=" + std::to_string(values[i].h) + " k=" + join(ks);
      }
      for (std::size_t aidx = 0; aidx < ks.size(); ++aidx) {
        for (std::size_t bidx = aidx + 1; bidx < ks.size(); ++bidx) {
          const u64 support = std::lcm(radicals[aidx], radicals[bidx]);
          const bool coprime_arguments = std::gcd(ks[aidx], ks[bidx]) == 1;
          const bool avoids_small = std::gcd(support, small_support) == 1;
          const std::string witness =
              "n=" + std::to_string(values[i].h) + " k={" +
              std::to_string(ks[aidx]) + "," + std::to_string(ks[bidx]) +
              "} support=" + std::to_string(support);
          if (coprime_arguments && first_coprime_pair.empty()) first_coprime_pair = witness;
          if (avoids_small && first_pair_avoiding_2_3_5_7.empty()) {
            first_pair_avoiding_2_3_5_7 = witness;
          }
          if (coprime_arguments && avoids_small &&
              first_coprime_pair_avoiding_2_3_5_7.empty()) {
            first_coprime_pair_avoiding_2_3_5_7 = witness;
          }
          if (std::gcd(support, 6ULL) == 1 && first_pair_coprime_to_6.empty()) {
            first_pair_coprime_to_6 = witness;
          }
          if (std::gcd(support, 2ULL) == 1 && first_pair_coprime_to_2.empty()) {
            first_pair_coprime_to_2 = witness;
          }
          if (std::gcd(support, 3ULL) == 1 && first_pair_coprime_to_3.empty()) {
            first_pair_coprime_to_3 = witness;
          }
          if (std::gcd(support, 5ULL) == 1 && first_pair_coprime_to_5.empty()) {
            first_pair_coprime_to_5 = witness;
          }
          if (std::gcd(support, 7ULL) == 1 && first_pair_coprime_to_7.empty()) {
            first_pair_coprime_to_7 = witness;
          }
        }
      }
      if (odd_ks.size() >= 2) {
        ++all_odd_argument_collision_fibers;
        if (first_all_odd_argument_collision.empty()) {
          first_all_odd_argument_collision =
              "n=" + std::to_string(values[i].h) + " odd_k=" + join(odd_ks);
        }
        if (first_odd_pair_disjoint_from_315_351.empty()) {
          constexpr u64 base_support = 3ULL * 5 * 7 * 13;
          for (std::size_t aidx = 0; aidx < odd_ks.size(); ++aidx) {
            for (std::size_t bidx = aidx + 1; bidx < odd_ks.size(); ++bidx) {
              const u64 support = std::lcm(radical(odd_ks[aidx], lp),
                                           radical(odd_ks[bidx], lp));
              if (std::gcd(support, base_support) == 1) {
                first_odd_pair_disjoint_from_315_351 =
                    "n=" + std::to_string(values[i].h) + " k={" +
                    std::to_string(odd_ks[aidx]) + "," +
                    std::to_string(odd_ks[bidx]) + "} support=" +
                    std::to_string(support);
              }
            }
          }
        }
      }

      const auto nf = factor_h(ks.front(), sigma[ks.front()], lp, primes);
      u64 omega = nf.size(), Omega = 0, max_alpha = 0;
      u128 product_alpha = 1, product_alpha_minus_one = 1;
      for (auto [p, e] : nf) {
        (void)p;
        Omega += e;
        max_alpha = std::max<u64>(max_alpha, e);
        product_alpha *= e;
        product_alpha_minus_one *= std::max<unsigned>(1, e - 1);
      }
      if (mult > omega) {
        ++f_gt_omega;
        if (first_f_gt_omega.empty()) first_f_gt_omega =
            "n=" + std::to_string(values[i].h) + " f=" + std::to_string(mult) +
            " omega=" + std::to_string(omega) + " k=" + join(ks);
      }
      const unsigned v2 = nf.count(2) ? nf.at(2) : 0;
      auto min_it = minimum_v2_by_multiplicity.find(mult);
      if (min_it == minimum_v2_by_multiplicity.end() || v2 < min_it->second.first) {
        minimum_v2_by_multiplicity[mult] = {v2, values[i].h};
      }
      if (mult > v2) {
        ++f_gt_v2;
        if (first_f_gt_v2.empty()) first_f_gt_v2 =
            "n=" + std::to_string(values[i].h) + " f=" + std::to_string(mult) +
            " v2=" + std::to_string(v2) + " k=" + join(ks);
      }
      auto max_it = minimum_max_alpha_by_multiplicity.find(mult);
      if (max_it == minimum_max_alpha_by_multiplicity.end() ||
          max_alpha < max_it->second.first) {
        minimum_max_alpha_by_multiplicity[mult] =
            {static_cast<unsigned>(max_alpha), values[i].h};
      }
      update_ratio(best_f_over_v2, mult, std::max<unsigned>(1, v2), values[i].h, ks);
      update_ratio(best_f_over_max_alpha, mult, max_alpha, values[i].h, ks);
      update_ratio(best_f_over_omega, mult, omega, values[i].h, ks);
      if (mult > Omega) ++f_gt_Omega;
      if (mult > max_alpha) ++f_gt_max_alpha;
      if (static_cast<u128>(mult) > product_alpha_minus_one) {
        ++f_gt_product_alpha_minus_one;
        if (first_f_gt_product_alpha_minus_one.empty()) {
          first_f_gt_product_alpha_minus_one =
              "n=" + std::to_string(values[i].h) + " f=" + std::to_string(mult) +
              " product_max(1,alpha-1)=" +
              std::to_string(static_cast<u64>(product_alpha_minus_one)) +
              " k=" + join(ks);
        }
      }
      if (static_cast<u128>(mult) > product_alpha) {
        std::cerr << "THEOREM VIOLATION at n=" << values[i].h << "\n";
        return 3;
      }
    }
    i = j;
  }

  std::cout << "K=" << K << " mode=" << (retain_all ? "all_k" : "exact_n")
            << " exact_n_upper_bound=" << (retain_all ? 0 : X)
            << " retained_preimages=" << values.size() << "\n";
  std::cout << "max_f=" << max_mult << " number_of_values_at_max=" << max_mult_count
            << " collision_fibers=" << collision_fibers << "\n";
  std::cout << "fiber_histogram";
  for (auto [m, count] : fiber_histogram) std::cout << " " << m << ":" << count;
  std::cout << "\n";
  std::cout << "least_exact_f_values\n";
  for (auto const& [m, data] : least_by_multiplicity) {
    std::cout << "f=" << m << " n=" << data.first << " k=" << join(data.second) << "\n";
  }
  std::cout << "powerful_part_violations=" << powerful_part_violations;
  if (!first_powerful_part_violation.empty()) std::cout << " first=" << first_powerful_part_violation;
  std::cout << "\n";
  std::cout << "repeated_support_collisions=" << repeated_support_collisions;
  if (!first_repeated_support_collision.empty()) std::cout << " first=" << first_repeated_support_collision;
  std::cout << "\n";
  std::cout << "radical_collisions=" << radical_collisions;
  if (!first_radical_collision.empty()) std::cout << " first=" << first_radical_collision;
  std::cout << "\n";
  std::cout << "powerful_big_omega_collisions=" << powerful_big_omega_collisions;
  if (!first_powerful_big_omega_collision.empty()) {
    std::cout << " first=" << first_powerful_big_omega_collision;
  }
  std::cout << "\n";
  std::cout << "repeated_prime_count_collisions=" << repeated_prime_count_collisions;
  if (!first_repeated_prime_count_collision.empty()) {
    std::cout << " first=" << first_repeated_prime_count_collision;
  }
  std::cout << "\n";
  std::cout << "odd_collision_fibers=" << odd_collision_fibers;
  if (!first_odd_collision.empty()) std::cout << " first=" << first_odd_collision;
  std::cout << "\n";
  std::cout << "all_odd_argument_collision_fibers=" << all_odd_argument_collision_fibers;
  if (!first_all_odd_argument_collision.empty()) {
    std::cout << " first=" << first_all_odd_argument_collision;
  }
  std::cout << "\n";
  std::cout << "odd_pair_disjoint_from_support_315_351=";
  if (first_odd_pair_disjoint_from_315_351.empty()) std::cout << "none";
  else std::cout << first_odd_pair_disjoint_from_315_351;
  std::cout << "\n";
  std::cout << "first_pair_avoiding_2_3_5_7="
            << (first_pair_avoiding_2_3_5_7.empty() ? "none" : first_pair_avoiding_2_3_5_7)
            << "\n";
  std::cout << "first_coprime_pair="
            << (first_coprime_pair.empty() ? "none" : first_coprime_pair) << "\n";
  std::cout << "first_coprime_pair_avoiding_2_3_5_7="
            << (first_coprime_pair_avoiding_2_3_5_7.empty()
                    ? "none"
                    : first_coprime_pair_avoiding_2_3_5_7)
            << "\n";
  std::cout << "first_pair_both_coprime_to_6="
            << (first_pair_coprime_to_6.empty() ? "none" : first_pair_coprime_to_6)
            << "\n";
  std::cout << "first_pair_both_odd="
            << (first_pair_coprime_to_2.empty() ? "none" : first_pair_coprime_to_2)
            << "\n";
  std::cout << "first_pair_both_not_divisible_by_3="
            << (first_pair_coprime_to_3.empty() ? "none" : first_pair_coprime_to_3)
            << "\n";
  std::cout << "first_pair_both_not_divisible_by_5="
            << (first_pair_coprime_to_5.empty() ? "none" : first_pair_coprime_to_5)
            << "\n";
  std::cout << "first_pair_both_not_divisible_by_7="
            << (first_pair_coprime_to_7.empty() ? "none" : first_pair_coprime_to_7)
            << "\n";
  std::cout << "first_fiber_with_gcd_all_preimages_1="
            << (first_fiber_with_gcd_one.empty() ? "none" : first_fiber_with_gcd_one)
            << "\n";
  std::cout << "first_v2_projection_collision="
            << (first_v2_projection_collision.empty() ? "none" : first_v2_projection_collision)
            << "\n";
  std::cout << "first_v2_v3_projection_collision="
            << (first_v2_v3_projection_collision.empty()
                    ? "none"
                    : first_v2_v3_projection_collision)
            << "\n";
  std::cout << "first_v2_v3_v5_projection_collision="
            << (first_v2_v3_v5_projection_collision.empty()
                    ? "none"
                    : first_v2_v3_v5_projection_collision)
            << "\n";
  std::cout << "first_v2_plus_v3_collision="
            << (first_v2_plus_v3_collision.empty() ? "none" : first_v2_plus_v3_collision)
            << "\n";
  std::cout << "first_2v2_plus_v3_collision="
            << (first_2v2_plus_v3_collision.empty() ? "none" : first_2v2_plus_v3_collision)
            << "\n";
  std::cout << "first_v2_plus_2v3_collision="
            << (first_v2_plus_2v3_collision.empty() ? "none" : first_v2_plus_2v3_collision)
            << "\n";
  std::cout << "f_gt_v2=" << f_gt_v2;
  if (!first_f_gt_v2.empty()) std::cout << " first=" << first_f_gt_v2;
  std::cout << "\n";
  std::cout << "minimum_v2_by_multiplicity";
  for (auto const& [m, data] : minimum_v2_by_multiplicity) {
    std::cout << " f=" << m << ":v2=" << data.first << "@n=" << data.second;
  }
  std::cout << "\n";
  std::cout << "minimum_max_alpha_by_multiplicity";
  for (auto const& [m, data] : minimum_max_alpha_by_multiplicity) {
    std::cout << " f=" << m << ":max_alpha=" << data.first << "@n=" << data.second;
  }
  std::cout << "\n";
  auto print_ratio = [](const char* label, const RatioWitness& w) {
    std::cout << label << "=" << w.numerator << "/" << w.denominator
              << "@n=" << w.n << " k=" << join(w.ks) << "\n";
  };
  print_ratio("best_f_over_max_1_v2", best_f_over_v2);
  print_ratio("best_f_over_max_alpha", best_f_over_max_alpha);
  print_ratio("best_f_over_omega", best_f_over_omega);
  std::cout << "f_gt_omega=" << f_gt_omega;
  if (!first_f_gt_omega.empty()) std::cout << " first=" << first_f_gt_omega;
  std::cout << "\n";
  std::cout << "f_gt_Omega=" << f_gt_Omega << " f_gt_max_alpha=" << f_gt_max_alpha << "\n";
  std::cout << "f_gt_product_max_1_alpha_minus_1=" << f_gt_product_alpha_minus_one;
  if (!first_f_gt_product_alpha_minus_one.empty()) {
    std::cout << " first=" << first_f_gt_product_alpha_minus_one;
  }
  std::cout << "\n";
  return 0;
}
