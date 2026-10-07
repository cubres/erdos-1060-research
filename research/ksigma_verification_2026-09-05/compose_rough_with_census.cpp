#include <algorithm>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <map>
#include <set>
#include <sstream>
#include <tuple>
#include <utility>
#include <vector>

using u32 = std::uint32_t;
using u64 = std::uint64_t;
using u128 = unsigned __int128;
using State = std::pair<u32, unsigned>;
using Factors = std::vector<std::pair<u64, unsigned>>;
struct Entry { u64 h; u32 k; };

static const std::vector<State> rough_left = {
    {11,2},{13,2},{17,1},{19,1},{31,1},{61,1},{97,1},{127,2},
    {271,1},{307,2},{331,1},{367,1}};
static const std::vector<State> rough_right = {
    {13,1},{17,2},{19,2},{23,1},{31,2},{43,1},{61,2},{83,1},
    {127,1},{307,1},{733,1},{5419,1}};
static const std::vector<State> saturation_left = {
    {2,1},{7,2},{11,2},{13,2},{43,2},{61,1},{79,1},{97,1},
    {307,1},{433,2},{631,1}};
static const std::vector<State> saturation_right = {
    {2,2},{3,2},{7,1},{19,1},{37,1},{43,1},{61,2},{79,2},
    {433,1},{631,2},{1693,1}};
static const std::vector<State> girth_left = {
    {2,1},{5,2},{11,2},{17,1},{37,2},{41,1},{61,2},{73,1},{79,2},
    {137,1},{151,1},{163,1},{307,1},{367,1},{433,1},{547,1},{613,1},
    {733,1},{1093,1},{1693,2},{1723,1},{3463,1}};
static const std::vector<State> girth_right = {
    {11,1},{13,1},{19,1},{23,2},{31,1},{37,1},{41,2},{61,1},{67,1},
    {79,1},{97,1},{137,2},{151,2},{307,2},{367,2},{431,1},{433,2},
    {487,1},{547,2},{1693,1}};

static std::vector<State> states(u32 k, const std::vector<u32>& least) {
  std::vector<State> answer;
  while (k > 1) {
    const u32 p = least[k];
    unsigned e = 0;
    do { k /= p; ++e; } while (k > 1 && least[k] == p);
    answer.push_back({p,e});
  }
  return answer;
}

static Factors factor_any(u64 n, const std::vector<u32>& least,
                          const std::vector<u32>& primes) {
  Factors answer;
  if (n < least.size()) {
    u32 x = static_cast<u32>(n);
    while (x > 1) {
      const u32 p = least[x];
      unsigned e = 0;
      do { x /= p; ++e; } while (x > 1 && least[x] == p);
      answer.push_back({p,e});
    }
    return answer;
  }
  for (u32 p : primes) {
    if (static_cast<u64>(p) * p > n) break;
    if (n % p) continue;
    unsigned e = 0;
    do { n /= p; ++e; } while (n % p == 0);
    answer.push_back({p,e});
  }
  if (n > 1) answer.push_back({n,1});
  return answer;
}

static u64 block_value(u32 p, unsigned e) {
  u64 power = 1, sum = 1;
  for (unsigned i = 0; i < e; ++i) {
    power *= p;
    sum += power;
  }
  return power * sum;
}

static std::string show(const std::vector<State>& states) {
  std::ostringstream out;
  out << "[";
  for (std::size_t i=0; i<states.size(); ++i) {
    if (i) out << ",";
    out << "[" << states[i].first << "," << states[i].second << "]";
  }
  return out.str() + "]";
}

int main(int argc, char** argv) {
  const u32 K = argc > 1
      ? static_cast<u32>(std::strtoull(argv[1], nullptr, 10)) : 10000000;
  const u64 X = static_cast<u64>(K) * K;
  std::vector<u32> least(K), prime_power(K,1), primes;
  std::vector<u64> sigma(K); sigma[1]=1;
  for (u32 i=2; i<K; ++i) {
    if (!least[i]) {
      least[i]=i; prime_power[i]=i; sigma[i]=static_cast<u64>(i)+1;
      primes.push_back(i);
    }
    for (u32 p:primes) {
      const u64 z=static_cast<u64>(i)*p;
      if (z>=K || p>least[i]) break;
      const u32 ip=static_cast<u32>(z); least[ip]=p;
      if (p==least[i]) {
        prime_power[ip]=prime_power[i]*p;
        const u32 core=i/prime_power[i];
        sigma[ip]=sigma[i]+sigma[core]*prime_power[ip];
      } else {
        prime_power[ip]=p; sigma[ip]=sigma[i]*(static_cast<u64>(p)+1);
      }
    }
  }
  std::vector<Entry> values; values.reserve(K);
  for (u32 k=1; k<K; ++k) {
    const u128 h=static_cast<u128>(k)*sigma[k];
    if (h<=X) values.push_back({static_cast<u64>(h),k});
  }
  std::sort(values.begin(),values.end(),[](const Entry&a,const Entry&b){
    return a.h<b.h || (a.h==b.h && a.k<b.k);
  });

  std::map<State,Factors> factor_cache;
  auto block_factors = [&](State state) -> const Factors& {
    auto it=factor_cache.find(state);
    if (it!=factor_cache.end()) return it->second;
    return factor_cache.emplace(
        state, factor_any(block_value(state.first,state.second),least,primes)
    ).first->second;
  };
  auto try_composition = [&](const std::vector<State>& a,
                             const std::vector<State>& b,
                             bool reverse, u64 candidate_target) {
    std::map<State,int> signed_count;
    for (State z:rough_left) ++signed_count[z];
    for (State z:rough_right) --signed_count[z];
    for (State z:(reverse?b:a)) ++signed_count[z];
    for (State z:(reverse?a:b)) --signed_count[z];
    std::vector<State> left,right;
    std::set<u32> left_bases,right_bases;
    for (auto [z,c]:signed_count) {
      if (c==0) continue;
      if (c!=1 && c!=-1) return false;
      auto& used = c==1 ? left_bases : right_bases;
      if (!used.insert(z.first).second) return false;
      (c==1?left:right).push_back(z);
    }
    if (left.empty() || right.empty()) return false;

    std::map<u64,unsigned> target_left,target_right;
    for (State z:left) for (auto [p,e]:block_factors(z)) target_left[p]+=e;
    for (State z:right) for (auto [p,e]:block_factors(z)) target_right[p]+=e;
    if (target_left!=target_right) std::abort();
    using Pair = std::pair<unsigned,unsigned>;
    std::vector<Pair> lp,rp;
    for (auto [p,e]:left) lp.push_back({target_left[p],e});
    for (auto [p,e]:right) rp.push_back({target_left[p],e});
    std::sort(lp.begin(),lp.end()); std::sort(rp.begin(),rp.end());
    std::vector<Pair> lsat,rsat;
    for (auto [alpha,e]:lp) lsat.push_back({e,alpha==e});
    for (auto [alpha,e]:rp) rsat.push_back({e,alpha==e});
    std::sort(lsat.begin(),lsat.end()); std::sort(rsat.begin(),rsat.end());
    if (lp!=rp) return false;
    std::cout << "HIT_EXACT_PROFILE candidate_target=" << candidate_target
              << " candidate=" << show(a) << " -- " << show(b)
              << " reverse=" << reverse << "\nLEFT=" << show(left)
              << "\nRIGHT=" << show(right) << "\nPROFILE=";
    for (auto [alpha,e]:lp) std::cout << "(" << alpha << "," << e << ")";
    std::cout << "\n";
    return true;
  };

  u64 pairs=0, valid_compositions=0;
  using SignedState = std::tuple<u32,unsigned,int>;
  std::set<std::vector<SignedState>> normalized_relations;
  for (std::size_t i=0;i<values.size();) {
    std::size_t j=i+1; while (j<values.size()&&values[j].h==values[i].h) ++j;
    if (j-i>1) {
      for (std::size_t x=i;x<j;++x) for (std::size_t y=x+1;y<j;++y) {
        ++pairs;
        const auto a=states(values[x].k,least), b=states(values[y].k,least);
        std::map<State,int> relation;
        for (State z:a) ++relation[z];
        for (State z:b) --relation[z];
        std::vector<SignedState> signature, opposite;
        for (auto [z,c]:relation) if (c) {
          signature.push_back({z.first,z.second,c});
          opposite.push_back({z.first,z.second,-c});
        }
        normalized_relations.insert(std::min(signature,opposite));
        for (bool reverse:{false,true}) {
          // Count a composition as structurally valid before the profile test
          // by reproducing the inexpensive state-map conditions here only in
          // the final aggregate would add noise; the searched-pair count is
          // the auditable finite scope.
          if (try_composition(a,b,reverse,values[i].h)) return 0;
          ++valid_compositions;
        }
      }
    }
    i=j;
  }
  auto insert_relation = [&](const std::vector<State>& left,
                             const std::vector<State>& right) {
    std::map<State,int> relation;
    for (State z:left) ++relation[z];
    for (State z:right) --relation[z];
    std::vector<SignedState> signature,opposite;
    for (auto [z,c]:relation) if (c) {
      signature.push_back({z.first,z.second,c});
      opposite.push_back({z.first,z.second,-c});
    }
    normalized_relations.insert(std::min(signature,opposite));
  };
  insert_relation(rough_left,rough_right);
  insert_relation(saturation_left,saturation_right);
  insert_relation(girth_left,girth_right);
  auto test_relation_map = [&](const std::map<State,int>& signed_count,
                               const char* label, std::size_t first,
                               std::size_t second, int orientation) {
    std::vector<State> left,right;
    std::set<u32> left_bases,right_bases;
    for (auto [z,c]:signed_count) {
      if (c==0) continue;
      if (c!=1 && c!=-1) return false;
      auto& used = c==1 ? left_bases : right_bases;
      if (!used.insert(z.first).second) return false;
      (c==1?left:right).push_back(z);
    }
    if (left.empty() || right.empty()) return false;
    std::map<u64,unsigned> target_left,target_right;
    for (State z:left) for (auto [p,e]:block_factors(z)) target_left[p]+=e;
    for (State z:right) for (auto [p,e]:block_factors(z)) target_right[p]+=e;
    if (target_left!=target_right) std::abort();
    using Pair=std::pair<unsigned,unsigned>;
    std::vector<Pair> lp,rp;
    for (auto [p,e]:left) lp.push_back({target_left[p],e});
    for (auto [p,e]:right) rp.push_back({target_left[p],e});
    std::sort(lp.begin(),lp.end()); std::sort(rp.begin(),rp.end());
    std::vector<Pair> lsat,rsat;
    for (auto [alpha,e]:lp) lsat.push_back({e,alpha==e});
    for (auto [alpha,e]:rp) rsat.push_back({e,alpha==e});
    std::sort(lsat.begin(),lsat.end()); std::sort(rsat.begin(),rsat.end());
    if (lp!=rp) return false;
    std::cout << "HIT_EXACT_" << label << " first=" << first << " second=" << second
              << " orientation=" << orientation << "\nLEFT=" << show(left)
              << "\nRIGHT=" << show(right) << "\nPROFILE=";
    for (auto [alpha,e]:lp) std::cout << "(" << alpha << "," << e << ")";
    std::cout << "\n";
    return true;
  };
  const std::vector<std::vector<SignedState>> relations(
      normalized_relations.begin(),normalized_relations.end());
  // Two relations on disjoint base sets give a four-corner fiber.  Its global
  // common exact-state core is empty (each relation was normalized).  Search
  // all six pairs of corners for equal *raw* full target profiles.  A hit here
  // is therefore a direct counterexample to global-core-normalized profile
  // injectivity, rather than merely to pairwise-normalized injectivity.
  u64 disjoint_relation_pairs=0, four_corner_profile_pairs=0;
  auto relation_sides = [&](const std::vector<SignedState>& relation) {
    std::pair<std::vector<State>,std::vector<State>> answer;
    for (auto [p,e,c]:relation)
      (c>0 ? answer.first : answer.second).push_back({p,e});
    return answer;
  };
  auto relation_target = [&](const std::vector<State>& side) {
    std::map<u64,unsigned> target;
    for (State z:side) for (auto [p,e]:block_factors(z)) target[p]+=e;
    return target;
  };
  for (std::size_t i=0;i<relations.size();++i) {
    auto ai=relation_sides(relations[i]);
    std::set<u32> ai_bases;
    for (State z:ai.first) ai_bases.insert(z.first);
    for (State z:ai.second) ai_bases.insert(z.first);
    for (std::size_t j=i+1;j<relations.size();++j) {
      auto bj=relation_sides(relations[j]);
      bool disjoint=true;
      for (State z:bj.first) if (ai_bases.count(z.first)) disjoint=false;
      for (State z:bj.second) if (ai_bases.count(z.first)) disjoint=false;
      if (!disjoint) continue;
      ++disjoint_relation_pairs;
      auto target=relation_target(ai.first);
      for (auto [p,e]:relation_target(bj.first)) target[p]+=e;
      std::vector<std::vector<State>> corners;
      for (const auto& as:{ai.first,ai.second})
        for (const auto& bs:{bj.first,bj.second}) {
          std::vector<State> corner=as;
          corner.insert(corner.end(),bs.begin(),bs.end());
          corners.push_back(std::move(corner));
        }
      using Pair=std::pair<unsigned,unsigned>;
      std::vector<std::vector<Pair>> profiles;
      for (const auto& corner:corners) {
        std::vector<Pair> profile;
        for (State z:corner) profile.push_back({target[z.first],z.second});
        std::sort(profile.begin(),profile.end());
        profiles.push_back(std::move(profile));
      }
      for (int a=0;a<4;++a) for (int b=a+1;b<4;++b) {
        ++four_corner_profile_pairs;
        if (profiles[a]!=profiles[b]) continue;
        std::cout << "HIT_EMPTY_GLOBAL_CORE relation_i=" << i
                  << " relation_j=" << j << " corner_a=" << a
                  << " corner_b=" << b << "\nA=" << show(corners[a])
                  << "\nB=" << show(corners[b]) << "\nPROFILE=";
        for (auto [alpha,e]:profiles[a])
          std::cout << "(" << alpha << "," << e << ")";
        std::cout << "\nATOM_I_PLUS=" << show(ai.first)
                  << "\nATOM_I_MINUS=" << show(ai.second)
                  << "\nATOM_J_PLUS=" << show(bj.first)
                  << "\nATOM_J_MINUS=" << show(bj.second) << "\n";
        return 0;
      }
    }
  }
  u64 pair_compositions=0;
  for (std::size_t i=0;i<relations.size();++i) {
    for (std::size_t j=i+1;j<relations.size();++j) {
      for (int orientation:{-1,1}) {
        ++pair_compositions;
        std::map<State,int> combined;
        for (auto [p,e,c]:relations[i]) combined[{p,e}]+=c;
        for (auto [p,e,c]:relations[j]) combined[{p,e}]+=orientation*c;
        if (test_relation_map(combined,"CENSUS_PAIR",i,j,orientation)) return 0;
      }
    }
  }
  u64 triple_compositions=0;
  for (std::size_t i=0;i<relations.size();++i) {
    for (std::size_t j=i+1;j<relations.size();++j) {
      for (std::size_t k=j+1;k<relations.size();++k) {
        for (int orientation_j:{-1,1}) for (int orientation_k:{-1,1}) {
          ++triple_compositions;
          std::map<State,int> combined;
          for (auto [p,e,c]:relations[i]) combined[{p,e}]+=c;
          for (auto [p,e,c]:relations[j]) combined[{p,e}]+=orientation_j*c;
          for (auto [p,e,c]:relations[k]) combined[{p,e}]+=orientation_k*c;
          if (test_relation_map(combined,"CENSUS_TRIPLE",i,
                                j*relations.size()+k,
                                10*orientation_j+orientation_k)) return 0;
        }
      }
    }
  }
  u64 quadruple_compositions=0;
  for (std::size_t i=0;i<relations.size();++i) {
    for (std::size_t j=i+1;j<relations.size();++j) {
      for (std::size_t k=j+1;k<relations.size();++k) {
        for (std::size_t l=k+1;l<relations.size();++l) {
          for (int oj:{-1,1}) for (int ok:{-1,1}) for (int ol:{-1,1}) {
            ++quadruple_compositions;
            std::map<State,int> combined;
            for (auto [p,e,c]:relations[i]) combined[{p,e}]+=c;
            for (auto [p,e,c]:relations[j]) combined[{p,e}]+=oj*c;
            for (auto [p,e,c]:relations[k]) combined[{p,e}]+=ok*c;
            for (auto [p,e,c]:relations[l]) combined[{p,e}]+=ol*c;
            if (test_relation_map(combined,"CENSUS_QUADRUPLE",i,
                                  (j*relations.size()+k)*relations.size()+l,
                                  100*oj+10*ok+ol)) return 0;
          }
        }
      }
    }
  }
  std::cout << "NO_HIT K=" << K << " X=" << X
            << " collision_pairs=" << pairs
            << " oriented_compositions_tested=" << valid_compositions
            << " distinct_normalized_relations=" << normalized_relations.size()
            << " disjoint_relation_pairs=" << disjoint_relation_pairs
            << " four_corner_profile_pairs=" << four_corner_profile_pairs
            << " relation_pair_compositions_tested=" << pair_compositions
            << " relation_triple_compositions_tested=" << triple_compositions
            << " relation_quadruple_compositions_tested="
            << quadruple_compositions
            << "\n";
}
