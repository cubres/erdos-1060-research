#include <algorithm>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <numeric>
#include <utility>
#include <vector>

using u32 = std::uint32_t;
using u64 = std::uint64_t;
using u128 = unsigned __int128;

struct Entry { u64 h; u32 k; };
using State = std::pair<u32, unsigned>;
using Profile = std::vector<std::pair<unsigned char, unsigned char>>;

int main(int argc, char** argv) {
  const u32 K = argc > 1
      ? static_cast<u32>(std::strtoull(argv[1], nullptr, 10))
      : 10000000;
  const u64 X = argc > 2
      ? static_cast<u64>(std::strtoull(argv[2], nullptr, 10))
      : static_cast<u64>(K) * K;

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
  std::sort(values.begin(), values.end(), [](const Entry& a, const Entry& b) {
    return a.h < b.h || (a.h == b.h && a.k < b.k);
  });

  auto states = [&](u32 k) {
    std::vector<State> answer;
    while (k > 1) {
      const u32 p = least[k];
      unsigned e = 0;
      do { k /= p; ++e; } while (k > 1 && least[k] == p);
      answer.push_back({p, e});
    }
    return answer;
  };
  auto block = [](u32 p, unsigned e) {
    u64 power = 1, sum = 1;
    for (unsigned j = 0; j < e; ++j) {
      power *= p;
      sum += power;
    }
    return power * sum;
  };
  auto normalized_profiles = [&](u32 a, u32 b, u64 target) {
    const auto as = states(a), bs = states(b);
    std::vector<State> common;
    std::set_intersection(as.begin(), as.end(), bs.begin(), bs.end(),
                          std::back_inserter(common));
    u64 reduced_target = target;
    for (auto [p, e] : common) {
      const u64 local = block(p, e);
      if (reduced_target % local != 0) std::abort();
      reduced_target /= local;
    }
    auto make = [&](const std::vector<State>& all) {
      Profile answer;
      std::vector<State> residual;
      std::set_difference(all.begin(), all.end(), common.begin(), common.end(),
                          std::back_inserter(residual));
      for (auto [p, e] : residual) {
        u64 t = reduced_target;
        unsigned alpha = 0;
        while (t % p == 0) { t /= p; ++alpha; }
        if (alpha > 255 || e > 255 || alpha < e) std::abort();
        answer.push_back({static_cast<unsigned char>(alpha),
                          static_cast<unsigned char>(e)});
      }
      std::sort(answer.begin(), answer.end());
      return answer;
    };
    return std::make_pair(make(as), make(bs));
  };
  auto raw_profile = [&](u32 k, u64 target) {
    Profile answer;
    for (auto [p,e]:states(k)) {
      u64 t=target; unsigned alpha=0;
      while (t%p==0) {t/=p; ++alpha;}
      answer.push_back({static_cast<unsigned char>(alpha),
                        static_cast<unsigned char>(e)});
    }
    std::sort(answer.begin(),answer.end());
    return answer;
  };

  u64 fibers = 0, pairs = 0, equal_normalized_profiles = 0;
  u64 equal_ratio_profiles = 0, equal_saturation_profiles = 0;
  u64 equal_raw_saturation_profiles = 0;
  u64 positive_fibers = 0, violations_v2 = 0;
  std::size_t largest_fiber = 0;
  u64 largest_fiber_target = 0;
  long double largest_fiber_over_v2 = 0;
  std::size_t largest_odd_fiber=0; u64 largest_odd_fiber_target=0;
  bool printed = false;
  bool printed_ratio = false, printed_saturation = false;
  bool printed_raw_saturation = false;
  for (std::size_t i = 0; i < values.size();) {
    std::size_t j = i + 1;
    while (j < values.size() && values[j].h == values[i].h) ++j;
    const std::size_t fiber_size=j-i;
    ++positive_fibers;
    if (fiber_size>largest_fiber) {
      largest_fiber=fiber_size; largest_fiber_target=values[i].h;
    }
    unsigned target_v2=0;
    for (u64 t=values[i].h; t%2==0; t/=2) ++target_v2;
    if (!target_v2 && fiber_size>largest_odd_fiber) {
      largest_odd_fiber=fiber_size; largest_odd_fiber_target=values[i].h;
    }
    if (fiber_size>target_v2) {
      ++violations_v2;
      if (violations_v2<=20)
        std::cout << "f_exceeds_v2 n=" << values[i].h
                  << " f=" << fiber_size << " v2=" << target_v2 << "\n";
    }
    if (target_v2 && (long double)fiber_size/target_v2>largest_fiber_over_v2)
      largest_fiber_over_v2=(long double)fiber_size/target_v2;
    if (j - i >= 2) {
      ++fibers;
      for (std::size_t a = i; a < j; ++a) {
        for (std::size_t b = a + 1; b < j; ++b) {
          ++pairs;
          const auto profiles = normalized_profiles(
              values[a].k, values[b].k, values[i].h);
          if (profiles.first == profiles.second) {
            ++equal_normalized_profiles;
            if (!printed) {
              printed = true;
              std::cout << "first_equal_normalized_profile n=" << values[i].h
                        << " k=" << values[a].k << "," << values[b].k << "\n";
            }
          }
          auto ratio_profile = [](const Profile& profile) {
            Profile answer;
            for (auto [alpha,e]:profile) {
              const unsigned g=std::gcd<unsigned>(alpha,e);
              answer.push_back({static_cast<unsigned char>(alpha/g),
                                static_cast<unsigned char>(e/g)});
            }
            std::sort(answer.begin(),answer.end());
            return answer;
          };
          auto saturation_profile = [](const Profile& profile) {
            Profile answer;
            for (auto [alpha,e]:profile) {
              answer.push_back({e,static_cast<unsigned char>(alpha==e)});
            }
            std::sort(answer.begin(),answer.end());
            return answer;
          };
          if (saturation_profile(raw_profile(values[a].k,values[i].h))==
              saturation_profile(raw_profile(values[b].k,values[i].h))) {
            ++equal_raw_saturation_profiles;
            if (!printed_raw_saturation) {
              printed_raw_saturation=true;
              std::cout << "first_equal_raw_saturation_profile n="
                        << values[i].h << " k=" << values[a].k << ","
                        << values[b].k << "\n";
            }
          }
          if (ratio_profile(profiles.first)==ratio_profile(profiles.second)) {
            ++equal_ratio_profiles;
            if (!printed_ratio) {
              printed_ratio=true;
              std::cout << "first_equal_normalized_ratio_profile n="
                        << values[i].h << " k=" << values[a].k << ","
                        << values[b].k << "\n";
            }
          }
          if (saturation_profile(profiles.first)==
              saturation_profile(profiles.second)) {
            ++equal_saturation_profiles;
            if (!printed_saturation) {
              printed_saturation=true;
              std::cout << "first_equal_normalized_saturation_profile n="
                        << values[i].h << " k=" << values[a].k << ","
                        << values[b].k << "\n";
            }
          }
        }
      }
    }
    i = j;
  }
  std::cout << "K=" << K << " X=" << X << " retained=" << values.size()
            << " collision_fibers=" << fibers << " collision_pairs=" << pairs
            << " equal_pairwise_common_block_normalized_profiles="
            << equal_normalized_profiles
            << " equal_normalized_ratio_profiles=" << equal_ratio_profiles
            << " equal_normalized_saturation_profiles="
            << equal_saturation_profiles
            << " equal_raw_saturation_profiles="
            << equal_raw_saturation_profiles
            << " positive_fibers=" << positive_fibers
            << " largest_fiber=" << largest_fiber
            << " largest_fiber_target=" << largest_fiber_target
            << " violations_f_le_v2=" << violations_v2
            << " max_f_over_v2=" << (double)largest_fiber_over_v2 << "\n";
  std::cout << "largest_odd_fiber=" << largest_odd_fiber
            << " largest_odd_fiber_target=" << largest_odd_fiber_target << "\n";
}
