#include <algorithm>
#include <cmath>
#include <cstdint>
#include <cstdlib>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <limits>
#include <map>
#include <numeric>
#include <set>
#include <sstream>
#include <string>
#include <unordered_map>
#include <utility>
#include <vector>

// Complete finite census of cubefree fibers of h(k)=k*sigma(k), together with
// the exact state-dependent interaction digraph of each collision fiber.
//
// If h(k)<=K^2, then k<K for k>1, because sigma(k)>k.  Thus retaining exactly
// the cubefree k<K with h(k)<=K^2 gives complete (rather than input-truncated)
// fibers throughout the displayed target interval.

using u8 = std::uint8_t;
using u32 = std::uint32_t;
using u64 = std::uint64_t;
using u128 = unsigned __int128;

struct Entry { u64 h; u32 k; };
using Factor = std::vector<std::pair<u32, u8>>;

static unsigned exponent_at(const Factor& f, u32 p);

static std::string show_u32(const std::vector<u32>& xs) {
  std::ostringstream out;
  out << "[";
  for (std::size_t i=0;i<xs.size();++i) {
    if (i) out << ",";
    out << xs[i];
  }
  return out.str()+"]";
}

static std::string show_factor(const Factor& f) {
  std::ostringstream out;
  out << "[";
  for (std::size_t i=0;i<f.size();++i) {
    if (i) out << ",";
    out << "[" << f[i].first << "," << static_cast<unsigned>(f[i].second) << "]";
  }
  return out.str()+"]";
}

static std::string normalized_relation_signature(const Factor& a,const Factor& b,
                                                 const std::vector<u32>& vertices) {
  auto oriented = [&](bool reverse) {
    std::ostringstream out;
    bool first=true;
    for (u32 p:vertices) {
      const unsigned ea=exponent_at(reverse?b:a,p);
      const unsigned eb=exponent_at(reverse?a:b,p);
      if (ea==eb) continue;
      if (!first) out << ";";
      first=false;
      out << p << ":" << ea << ":" << eb;
    }
    return out.str();
  };
  return std::min(oriented(false),oriented(true));
}

static Factor factor_input(u32 k, const std::vector<u32>& least) {
  Factor out;
  while (k>1) {
    const u32 p=least[k];
    u8 e=0;
    do { k/=p; ++e; } while (k>1 && least[k]==p);
    out.push_back({p,e});
  }
  return out;
}

static unsigned exponent_at(const Factor& f, u32 p) {
  auto it=std::lower_bound(f.begin(),f.end(),std::make_pair(p,static_cast<u8>(0)));
  return it!=f.end() && it->first==p ? it->second : 0;
}

static u64 sigma_prime_power(u32 p, unsigned e) {
  u128 power=1,sum=1;
  for (unsigned j=0;j<e;++j) { power*=p; sum+=power; }
  if (sum>std::numeric_limits<u64>::max()) std::abort();
  return static_cast<u64>(sum);
}

static unsigned valuation(u64 n,u32 p) {
  unsigned v=0;
  while (n%p==0) { n/=p; ++v; }
  return v;
}

struct Digraph {
  std::vector<u32> vertices;
  std::vector<u64> adjacency;
};

// q->p iff a |-> v_p(sigma(q^a)) is nonconstant on the exponent states
// actually present at q in this fiber.  This is exactly the interaction graph
// used by the feedback-set injection lemma, not the larger candidate graph.
static Digraph interaction_graph(const std::vector<Factor>& factors) {
  std::vector<u32> vertices;
  for (const auto& f:factors) for (auto [p,e]:f) {
    (void)e; vertices.push_back(p);
  }
  std::sort(vertices.begin(),vertices.end());
  vertices.erase(std::unique(vertices.begin(),vertices.end()),vertices.end());
  if (vertices.size()>63) std::abort();
  std::vector<u64> adjacency(vertices.size());
  for (std::size_t qi=0;qi<vertices.size();++qi) {
    const u32 q=vertices[qi];
    for (std::size_t pi=0;pi<vertices.size();++pi) {
      const u32 p=vertices[pi];
      unsigned first=0;
      bool initialized=false,nonconstant=false;
      for (const auto& f:factors) {
        const unsigned e=exponent_at(f,q);
        const unsigned v=e ? valuation(sigma_prime_power(q,e),p) : 0;
        if (!initialized) { first=v; initialized=true; }
        else if (v!=first) { nonconstant=true; break; }
      }
      if (nonconstant) adjacency[qi] |= (u64{1}<<pi);
    }
  }
  return {std::move(vertices),std::move(adjacency)};
}

static u64 find_directed_cycle(const Digraph& g,u64 alive) {
  const unsigned n=g.vertices.size();
  std::vector<u8> color(n);
  std::vector<int> parent(n,-1);
  auto visit = [&](auto&& self,unsigned u)->u64 {
    color[u]=1;
    u64 todo=g.adjacency[u]&alive;
    while (todo) {
      const unsigned v=__builtin_ctzll(todo);
      todo&=todo-1;
      if (color[v]==0) {
        parent[v]=static_cast<int>(u);
        if (u64 c=self(self,v)) return c;
      } else if (color[v]==1) {
        u64 cycle=u64{1}<<v;
        int x=static_cast<int>(u);
        while (x!=static_cast<int>(v)) {
          if (x<0) std::abort();
          cycle|=u64{1}<<x;
          x=parent[x];
        }
        return cycle;
      }
    }
    color[u]=2;
    return 0;
  };
  for (unsigned u=0;u<n;++u) if ((alive>>u&1) && color[u]==0) {
    if (u64 c=visit(visit,u)) return c;
  }
  return 0;
}

struct FvsAnswer { unsigned size; u64 vertices; };

static FvsAnswer minimum_fvs(const Digraph& g) {
  std::unordered_map<u64,FvsAnswer> memo;
  auto solve = [&](auto&& self,u64 alive)->FvsAnswer {
    auto it=memo.find(alive);
    if (it!=memo.end()) return it->second;
    const u64 cycle=find_directed_cycle(g,alive);
    if (!cycle) return memo.emplace(alive,FvsAnswer{0,0}).first->second;
    FvsAnswer best{std::numeric_limits<unsigned>::max(),0};
    u64 choices=cycle;
    while (choices) {
      const unsigned v=__builtin_ctzll(choices);
      choices&=choices-1;
      FvsAnswer child=self(self,alive&~(u64{1}<<v));
      if (child.size+1<best.size) best={child.size+1,child.vertices|(u64{1}<<v)};
    }
    return memo.emplace(alive,best).first->second;
  };
  const u64 all=g.vertices.size()==64 ? ~u64{0} : ((u64{1}<<g.vertices.size())-1);
  FvsAnswer answer=solve(solve,all);
  if (find_directed_cycle(g,all&~answer.vertices)) std::abort();
  return answer;
}

static unsigned directed_girth(const Digraph& g) {
  const unsigned n=g.vertices.size(),inf=std::numeric_limits<unsigned>::max()/2;
  unsigned best=inf;
  for (unsigned source=0;source<n;++source) {
    std::vector<unsigned> distance(n,inf),queue;
    distance[source]=0; queue.push_back(source);
    for (std::size_t head=0;head<queue.size();++head) {
      const unsigned u=queue[head];
      u64 todo=g.adjacency[u];
      while (todo) {
        const unsigned v=__builtin_ctzll(todo); todo&=todo-1;
        if (v==source) best=std::min(best,distance[u]+1);
        if (distance[v]==inf) { distance[v]=distance[u]+1; queue.push_back(v); }
      }
    }
  }
  return best==inf ? 0 : best;
}

struct Witness {
  bool set=false;
  u64 n=0;
  std::vector<u32> ks;
  std::vector<Factor> factors;
  std::vector<u32> differing;
  long double mass=0;
  unsigned fvs=0,girth=0;
  std::vector<u32> fvs_vertices;
  Digraph graph;
};

static Witness make_witness(u64 n,const std::vector<u32>& ks,
                            const std::vector<Factor>& factors,
                            const std::vector<u32>& differing,long double mass,
                            const Digraph& graph,const FvsAnswer& fvs) {
  Witness w; w.set=true; w.n=n; w.ks=ks; w.factors=factors;
  w.differing=differing; w.mass=mass; w.fvs=fvs.size;
  w.girth=directed_girth(graph); w.graph=graph;
  for (unsigned i=0;i<graph.vertices.size();++i)
    if (fvs.vertices>>i&1) w.fvs_vertices.push_back(graph.vertices[i]);
  return w;
}

static void print_witness(const char* name,const Witness& w) {
  std::cout << name << "=";
  if (!w.set) { std::cout << "none\n"; return; }
  std::cout << "n=" << w.n << " k=" << show_u32(w.ks)
            << " factors=[";
  for (std::size_t i=0;i<w.factors.size();++i) {
    if (i) std::cout << ",";
    std::cout << show_factor(w.factors[i]);
  }
  std::cout << "] delta=" << show_u32(w.differing)
            << " mass=" << std::setprecision(18) << static_cast<double>(w.mass)
            << " fvs=" << w.fvs << " fvs_vertices=" << show_u32(w.fvs_vertices)
            << " girth=" << w.girth << " edges=[";
  bool first=true;
  for (unsigned u=0;u<w.graph.vertices.size();++u) {
    u64 todo=w.graph.adjacency[u];
    while (todo) {
      unsigned v=__builtin_ctzll(todo); todo&=todo-1;
      if (!first) std::cout << ",";
      first=false;
      std::cout << "[" << w.graph.vertices[u] << "," << w.graph.vertices[v] << "]";
    }
  }
  std::cout << "]\n";
}

int main(int argc,char**argv) {
  const u32 K=argc>1 ? static_cast<u32>(std::strtoull(argv[1],nullptr,10)) : 10000000;
  const std::string pair_path=argc>2 ? argv[2] : "";
  if (K<3 || static_cast<u64>(K)*K>std::numeric_limits<u64>::max()) return 2;
  const u64 X=static_cast<u64>(K)*K;

  std::vector<u32> least(K),ppow(K,1),primes;
  std::vector<u64> sigma(K); sigma[1]=1;
  std::vector<u8> maxexp(K);
  for (u32 i=2;i<K;++i) {
    if (!least[i]) {
      least[i]=i; ppow[i]=i; sigma[i]=static_cast<u64>(i)+1;
      maxexp[i]=1; primes.push_back(i);
    }
    for (u32 p:primes) {
      const u64 z=static_cast<u64>(i)*p;
      if (z>=K || p>least[i]) break;
      const u32 ip=static_cast<u32>(z); least[ip]=p;
      if (p==least[i]) {
        ppow[ip]=ppow[i]*p;
        const u32 core=i/ppow[i];
        sigma[ip]=sigma[i]+sigma[core]*ppow[ip];
        unsigned e=0; for (u32 t=ppow[ip];t>1;t/=p) ++e;
        maxexp[ip]=static_cast<u8>(std::max<unsigned>(maxexp[core],e));
      } else {
        ppow[ip]=p; sigma[ip]=sigma[i]*(static_cast<u64>(p)+1);
        maxexp[ip]=std::max<u8>(maxexp[i],1);
      }
    }
  }

  std::vector<Entry> values; values.reserve(K);
  for (u32 k=1;k<K;++k) if (maxexp[k]<=2) {
    const u128 h=static_cast<u128>(k)*sigma[k];
    if (h<=X) values.push_back({static_cast<u64>(h),k});
  }
  std::sort(values.begin(),values.end(),[](const Entry&a,const Entry&b){
    return a.h<b.h || (a.h==b.h && a.k<b.k);
  });

  std::ofstream pairs_out;
  if (!pair_path.empty()) {
    pairs_out.open(pair_path);
    pairs_out << "n\tk1\tk2\tdelta_size\troughness\teuler_mass\tfvs\tgirth\tsame_radical\n";
  }

  u64 collision_fibers=0,collision_pairs=0,same_radical_pairs=0;
  u64 support_disjoint_pairs=0;
  std::map<unsigned,u64> fiber_hist,fvs_hist,girth_hist,delta_hist;
  std::map<u32,u64> roughness_hist;
  std::map<std::string,u64> normalized_relation_hist;
  const std::vector<u32> thresholds={2,3,5,7,11,17,31,100,1000};
  std::map<u32,u64> avoiding_count;
  std::map<u32,Witness> minimum_mass_avoiding;
  Witness minimum_mass,maximum_roughness,maximum_fvs,maximum_delta;
  Witness first_same_radical,first_fvs_two,minimum_disjoint_mass;
  long double best_fvs_scale=-1;
  Witness maximum_fvs_scale;

  for (std::size_t i=0;i<values.size();) {
    std::size_t j=i+1;
    while (j<values.size() && values[j].h==values[i].h) ++j;
    const unsigned f=j-i; ++fiber_hist[f];
    if (f>=2) {
      ++collision_fibers;
      std::vector<u32> ks;
      std::vector<Factor> factors;
      for (std::size_t z=i;z<j;++z) {
        ks.push_back(values[z].k);
        factors.push_back(factor_input(values[z].k,least));
      }
      const Digraph graph=interaction_graph(factors);
      const FvsAnswer fvs=minimum_fvs(graph);
      if (!fvs.size) { std::cerr << "acyclic collision fiber n=" << values[i].h << "\n"; return 3; }
      ++fvs_hist[fvs.size];
      ++girth_hist[directed_girth(graph)];
      for (unsigned a=0;a<f;++a) for (unsigned b=a+1;b<f;++b) {
        ++collision_pairs;
        std::vector<u32> differing;
        std::set<u32> support_a,support_b;
        for (auto [p,e]:factors[a]) { (void)e; support_a.insert(p); }
        for (auto [p,e]:factors[b]) { (void)e; support_b.insert(p); }
        for (u32 p:graph.vertices)
          if (exponent_at(factors[a],p)!=exponent_at(factors[b],p)) differing.push_back(p);
        if (differing.empty()) std::abort();
        ++normalized_relation_hist[
            normalized_relation_signature(factors[a],factors[b],graph.vertices)];
        long double mass=0;
        for (u32 p:differing) mass-=std::log1pl(-1.0L/p);
        ++delta_hist[differing.size()];
        ++roughness_hist[differing.front()];
        const bool same_radical=support_a==support_b;
        if (same_radical) {
          ++same_radical_pairs;
          if (!first_same_radical.set)
            first_same_radical=make_witness(values[i].h,ks,factors,differing,mass,graph,fvs);
        }
        bool disjoint=true;
        for (u32 p:support_a) if (support_b.count(p)) { disjoint=false; break; }
        if (disjoint) {
          ++support_disjoint_pairs;
          if (!minimum_disjoint_mass.set || mass<minimum_disjoint_mass.mass)
            minimum_disjoint_mass=make_witness(values[i].h,ks,factors,differing,mass,graph,fvs);
          if (!(std::exp(mass)>4.0L)) {
            std::cerr << "coprime Euler-product bound failure n=" << values[i].h << "\n";
            return 4;
          }
        }
        Witness w=make_witness(values[i].h,ks,factors,differing,mass,graph,fvs);
        if (!minimum_mass.set || mass<minimum_mass.mass) minimum_mass=w;
        if (!maximum_roughness.set || differing.front()>maximum_roughness.differing.front()) maximum_roughness=w;
        if (!maximum_fvs.set || fvs.size>maximum_fvs.fvs) maximum_fvs=w;
        if (!maximum_delta.set || differing.size()>maximum_delta.differing.size()) maximum_delta=w;
        if (fvs.size>=2 && !first_fvs_two.set) first_fvs_two=w;
        const long double scale=static_cast<long double>(fvs.size)*std::log(std::log(static_cast<long double>(values[i].h)))/std::log(static_cast<long double>(values[i].h));
        if (scale>best_fvs_scale) { best_fvs_scale=scale; maximum_fvs_scale=w; }
        for (u32 t:thresholds) if (differing.front()>t) {
          ++avoiding_count[t];
          auto& old=minimum_mass_avoiding[t];
          if (!old.set || mass<old.mass) old=w;
        }
        if (pairs_out)
          pairs_out << values[i].h << '\t' << values[i+a].k << '\t' << values[i+b].k
                    << '\t' << differing.size() << '\t' << differing.front()
                    << '\t' << std::setprecision(18) << static_cast<double>(mass)
                    << '\t' << fvs.size << '\t' << directed_girth(graph)
                    << '\t' << same_radical << '\n';
      }
    }
    i=j;
  }

  std::cout << "scope K=" << K << " exact_target_max=" << X
            << " exponent_cap=2 retained=" << values.size()
            << " collision_fibers=" << collision_fibers
            << " collision_pairs=" << collision_pairs
            << " same_radical_pairs=" << same_radical_pairs
            << " support_disjoint_pairs=" << support_disjoint_pairs << "\n";
  std::cout << "fiber_hist"; for (auto [x,c]:fiber_hist) std::cout << " " << x << ":" << c; std::cout << "\n";
  std::cout << "fvs_hist"; for (auto [x,c]:fvs_hist) std::cout << " " << x << ":" << c; std::cout << "\n";
  std::cout << "girth_hist"; for (auto [x,c]:girth_hist) std::cout << " " << x << ":" << c; std::cout << "\n";
  std::cout << "delta_size_hist"; for (auto [x,c]:delta_hist) std::cout << " " << x << ":" << c; std::cout << "\n";
  std::cout << "roughness_hist"; for (auto [x,c]:roughness_hist) std::cout << " " << x << ":" << c; std::cout << "\n";
  std::cout << "normalized_relation_count=" << normalized_relation_hist.size() << "\n";
  if (normalized_relation_hist.size()<=100) {
    for (const auto& [signature,count]:normalized_relation_hist)
      std::cout << "normalized_relation count=" << count << " signature=" << signature << "\n";
  }
  std::cout << "avoidance_counts"; for (u32 t:thresholds) std::cout << " >" << t << ":" << avoiding_count[t]; std::cout << "\n";
  std::cout << "maximum_fvs_scale=" << std::setprecision(18) << static_cast<double>(best_fvs_scale) << "\n";
  print_witness("minimum_euler_mass",minimum_mass);
  print_witness("maximum_roughness",maximum_roughness);
  print_witness("maximum_fvs",maximum_fvs);
  print_witness("maximum_delta_size",maximum_delta);
  print_witness("maximum_fvs_normalized_scale",maximum_fvs_scale);
  print_witness("first_same_radical",first_same_radical);
  print_witness("first_fvs_at_least_two",first_fvs_two);
  print_witness("minimum_support_disjoint_mass",minimum_disjoint_mass);
  for (u32 t:thresholds) {
    const std::string label="minimum_mass_avoiding_through_"+std::to_string(t);
    print_witness(label.c_str(),minimum_mass_avoiding[t]);
  }
}
