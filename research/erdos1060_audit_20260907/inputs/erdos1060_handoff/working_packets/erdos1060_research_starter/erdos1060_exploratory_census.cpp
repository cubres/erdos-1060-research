/*
  Exact exploratory census for h(k) = k * sigma(k), 1 <= k <= K.

  Build: c++ -O3 -std=c++17 erdos1060_exploratory_census.cpp -o census
  Run:   ./census 5000000 > census_results.txt

  Reports input-restricted multiplicity records and bounded-exponent records.
  For E = 2 and E = 3 it also reports all distinct collision pairs obtained by
  cancelling equal positive prime-power factors on both sides. This is common
  UNITARY cancellation, not ordinary gcd cancellation. The output does not
  assert a classification of collisions beyond the searched range.

  Completeness: h(k) > k^2 for k > 1. Hence every fiber at target N <= K^2 is
  fully captured. Counts at larger targets may omit inputs above K.

  sigma(k) is computed by its multiplicative prime-power formula, separately
  from a divisor-sum sieve used in an earlier exploratory implementation.
  A direct divisor sum checks every computed sigma(k) for k <= min(K, 5000).

  Uses only exact integer arithmetic. K is capped at 100 million for arithmetic
  safety and practicality. Large K can require several GB of RAM. Allocation
  errors are reported. Defaults to 5 million. No third-party dependencies.
*/
#include <algorithm>
#include <array>
#include <cstdint>
#include <iostream>
#include <set>
#include <stdexcept>
#include <string>
#include <utility>
#include <vector>

struct Entry {
    std::uint64_t target;
    std::uint32_t input;
};

std::uint64_t direct_sigma(std::uint32_t k) {
    std::uint64_t answer = 0;
    for (std::uint32_t d = 1; std::uint64_t(d) * d <= k; ++d) {
        if (k % d != 0) continue;
        answer += d;
        if (d != k / d) answer += k / d;
    }
    return answer;
}

std::pair<std::uint32_t, std::uint32_t> cancel_common_unitary(
    std::uint32_t a, std::uint32_t b,
    const std::vector<std::uint32_t>& spf) {
    std::uint32_t t = a, common = 1;
    while (t > 1) {
        const std::uint32_t p = spf[t];
        std::uint32_t power = 1, ea = 0, eb = 0;
        do { t /= p; power *= p; ++ea; } while (t % p == 0);
        std::uint32_t z = b;
        while (z % p == 0) { z /= p; ++eb; }
        if (ea == eb) common *= power;
    }
    return {a / common, b / common};
}

int main(int argc, char** argv) {
    try {
        if (argc > 2) throw std::invalid_argument("Usage: census [K]");
        std::uint64_t requested = 5000000;
        if (argc == 2) {
            const std::string text = argv[1];
            if (text.empty() || text.find_first_not_of("0123456789") != std::string::npos)
                throw std::invalid_argument("K must be a positive integer.");
            std::size_t used = 0;
            requested = std::stoull(text, &used);
            if (used != text.size()) throw std::invalid_argument("Invalid K.");
        }
        if (requested == 0 || requested > 100000000)
            throw std::invalid_argument("Require 1 <= K <= 100000000.");
        const auto K = static_cast<std::uint32_t>(requested);
        const std::uint64_t complete_target_limit = requested * requested;
        std::vector<std::uint32_t> spf(std::size_t(K) + 1, 0);
        for (std::uint32_t p = 2; p <= K; ++p) {
            if (spf[p] != 0) continue;
            for (std::uint32_t j = p; j <= K; j += p)
                if (spf[j] == 0) spf[j] = p;
        }
        std::vector<std::uint64_t> sigma(std::size_t(K) + 1, 0);
        std::vector<std::uint8_t> max_exponent(std::size_t(K) + 1, 0);
        std::vector<Entry> entries;
        entries.reserve(K);
        sigma[1] = 1;
        entries.push_back({1, 1});
        for (std::uint32_t k = 2; k <= K; ++k) {
            const std::uint32_t p = spf[k];
            std::uint32_t m = k, exponent = 0;
            std::uint64_t power = 1, geometric_sum = 1;
            do {
                m /= p;
                ++exponent;
                power *= p;
                geometric_sum += power;
            } while (m % p == 0);
            sigma[k] = sigma[m] * geometric_sum;
            max_exponent[k] = static_cast<std::uint8_t>(
                std::max<std::uint32_t>(exponent, max_exponent[m]));
            entries.push_back({std::uint64_t(k) * sigma[k], k});
        }
        for (std::uint32_t k = 1; k <= std::min<std::uint32_t>(K, 5000); ++k)
            if (sigma[k] != direct_sigma(k))
                throw std::runtime_error("Direct sigma cross-check failed.");
        std::sort(entries.begin(), entries.end(), [](const Entry& a, const Entry& b) {
            return a.target < b.target || (a.target == b.target && a.input < b.input);
        });
        std::cout << "INPUT LIMIT K=" << K << '\n'
                  << "COMPLETE TARGET LIMIT=" << complete_target_limit << '\n'
                  << "All records below are input-restricted; target counts above "
                  << "the complete limit may be incomplete.\n";
        std::size_t global_best = 0;
        std::array<std::size_t, 11> best{};
        std::set<std::pair<std::uint32_t, std::uint32_t>> reduced2, reduced3;
        for (std::size_t i = 0; i < entries.size();) {
            std::size_t j = i + 1;
            while (j < entries.size() && entries[j].target == entries[i].target) ++j;
            if (j - i > global_best) {
                global_best = j - i;
                std::cout << "GLOBAL RECORD " << global_best << " N="
                          << entries[i].target << " inputs:";
                for (std::size_t t = i; t < j; ++t) std::cout << ' ' << entries[t].input;
                std::cout << '\n';
            }
            for (int E = 1; E <= 10; ++E) {
                std::size_t count = 0;
                for (std::size_t t = i; t < j; ++t)
                    if (max_exponent[entries[t].input] <= E) ++count;
                if (count > best[E]) {
                    best[E] = count;
                    std::cout << "E=" << E << " RECORD " << count
                              << " N=" << entries[i].target << " inputs:";
                    for (std::size_t t = i; t < j; ++t)
                        if (max_exponent[entries[t].input] <= E)
                            std::cout << ' ' << entries[t].input;
                    std::cout << '\n';
                }
            }
            for (std::size_t u = i; u < j; ++u) {
                if (max_exponent[entries[u].input] > 3) continue;
                for (std::size_t v = u + 1; v < j; ++v) {
                    const auto a = entries[u].input, b = entries[v].input;
                    if (max_exponent[b] > 3) continue;
                    const auto pair = cancel_common_unitary(a, b, spf);
                    if (std::uint64_t(pair.first) * sigma[pair.first] !=
                        std::uint64_t(pair.second) * sigma[pair.second])
                        throw std::runtime_error("Unitary cancellation check failed.");
                    reduced3.insert(pair);
                    if (max_exponent[a] <= 2 && max_exponent[b] <= 2)
                        reduced2.insert(pair);
                }
            }
            i = j;
        }
        std::cout << "CUBEFREE COMMON-UNITARY-REDUCED PAIRS " << reduced2.size() << '\n';
        for (const auto& pair : reduced2) std::cout << pair.first << ' ' << pair.second << '\n';
        std::cout << "FOURTH-POWER-FREE COMMON-UNITARY-REDUCED PAIRS " << reduced3.size() << '\n';
        for (const auto& pair : reduced3) std::cout << pair.first << ' ' << pair.second << '\n';
        return 0;
    } catch (const std::exception& error) {
        std::cerr << "Error: " << error.what() << '\n';
        return 1;
    }
}
