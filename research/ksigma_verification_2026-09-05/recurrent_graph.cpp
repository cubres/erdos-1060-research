#include <algorithm>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <numeric>
#include <set>
#include <utility>
#include <vector>

using u64 = std::uint64_t;

static u64 powmod(u64 a, u64 e, u64 mod) {
  u64 r = 1;
  while (e) {
    if (e & 1) r = static_cast<u64>((__uint128_t)r * a % mod);
    a = static_cast<u64>((__uint128_t)a * a % mod);
    e >>= 1;
  }
  return r;
}

static int primitive_root(int p, const std::vector<int>& least) {
  if (p == 2) return 1;
  int x = p - 1;
  std::vector<int> factors;
  while (x > 1) {
    int q = least[x]; factors.push_back(q);
    while (x % q == 0) x /= q;
  }
  for (int g = 2;; ++g) {
    bool ok = true;
    for (int q : factors) if (powmod(g, (p-1)/q, p) == 1) { ok=false; break; }
    if (ok) return g;
  }
}

struct SCCResult {
  std::vector<int> component;
  std::vector<int> size, minimum, maximum;
};

static SCCResult kosaraju(const std::vector<std::vector<int>>& graph,
                          const std::vector<std::vector<int>>& reverse) {
  const int n = static_cast<int>(graph.size());
  std::vector<char> seen(n, 0);
  std::vector<int> order; order.reserve(n);
  for (int start=0; start<n; ++start) if (!seen[start]) {
    std::vector<std::pair<int,std::size_t>> stack;
    seen[start]=1; stack.push_back({start,0});
    while (!stack.empty()) {
      int v=stack.back().first;
      std::size_t &next=stack.back().second;
      if (next < graph[v].size()) {
        int w=graph[v][next++];
        if (!seen[w]) { seen[w]=1; stack.push_back({w,0}); }
      } else {
        order.push_back(v); stack.pop_back();
      }
    }
  }
  std::vector<int> component(n,-1), sizes, mins, maxs;
  for (auto it=order.rbegin(); it!=order.rend(); ++it) if (component[*it] < 0) {
    int id=static_cast<int>(sizes.size()), count=0, lo=n, hi=-1;
    std::vector<int> stack{*it}; component[*it]=id;
    while (!stack.empty()) {
      int v=stack.back(); stack.pop_back(); ++count; lo=std::min(lo,v); hi=std::max(hi,v);
      for (int w:reverse[v]) if (component[w]<0) {component[w]=id;stack.push_back(w);}
    }
    sizes.push_back(count); mins.push_back(lo); maxs.push_back(hi);
  }
  return {std::move(component),std::move(sizes),std::move(mins),std::move(maxs)};
}

int main(int argc, char** argv) {
  if (argc < 3) {
    std::cerr << "usage: recurrent_graph R X\n";
    return 2;
  }
  const int R=std::atoi(argv[1]);
  const int X=std::atoi(argv[2]);
  if (!(R==3 || R==4) || X<3) return 2;

  // Linear sieve, with an integer least-prime-factor table also used to find
  // primitive roots modulo target primes.
  std::vector<int> least(X+1), primes;
  for (int i=2;i<=X;++i) {
    if (!least[i]) {least[i]=i;primes.push_back(i);}
    for (int p:primes) {
      long long z=1LL*i*p;
      if (z>X || p>least[i]) break;
      least[z]=p;
    }
  }
  std::vector<int> prime_index(X+1,-1);
  for (int i=0;i<(int)primes.size();++i) prime_index[primes[i]]=i;
  std::vector<std::vector<int>> graph(primes.size()), reverse(primes.size());
  u64 edge_count=0;

  // Generate edges in reverse, by the exact roots modulo q of
  // 1+x+...+x^e for e<R.  This avoids factoring O(pi(X)) quadratic-size
  // polynomial values.
  for (int qi=0; qi<(int)primes.size(); ++qi) {
    const int q=primes[qi];
    std::vector<int> roots;
    roots.push_back(q-1);                         // e=1: x+1
    if (q==3) roots.push_back(1);                 // e=2, exceptional root
    else if (q%3==1) {
      int g=primitive_root(q,least);
      int w=static_cast<int>(powmod(g,(q-1)/3,q));
      roots.push_back(w); roots.push_back(static_cast<int>((u64)w*w%q));
    }
    if (R==4) {
      // e=3: (x+1)(x^2+1); -1 is already present.
      if (q==2) roots.push_back(1);
      else if (q%4==1) {
        int g=primitive_root(q,least);
        int root=static_cast<int>(powmod(g,(q-1)/4,q));
        roots.push_back(root); roots.push_back(q-root);
      }
    }
    std::sort(roots.begin(),roots.end());
    roots.erase(std::unique(roots.begin(),roots.end()),roots.end());
    for (int root:roots) {
      int p=root;
      if (p<2) p += ((2-p+q-1)/q)*q;
      for (;p<=X;p+=q) if (prime_index[p]>=0 && p!=q) {
        int pi=prime_index[p]; graph[pi].push_back(qi); reverse[qi].push_back(pi); ++edge_count;
      }
    }
  }
  // Roots are distinct for fixed q, but sort for deterministic diagnostics.
  for (auto &a:graph) std::sort(a.begin(),a.end());
  for (auto &a:reverse) std::sort(a.begin(),a.end());

  SCCResult scc=kosaraju(graph,reverse);
  int nontrivial_components=0, recurrent=0, largest=0, component_of_two=scc.component[prime_index[2]];
  std::vector<int> ids;
  for (int c=0;c<(int)scc.size.size();++c) if (scc.size[c]>1) {
    ++nontrivial_components; recurrent+=scc.size[c]; largest=std::max(largest,scc.size[c]);ids.push_back(c);
  }
  std::sort(ids.begin(),ids.end(),[&](int a,int b){return scc.size[a]>scc.size[b];});
  std::cout << "R="<<R<<" X="<<X<<" primes="<<primes.size()<<" edges="<<edge_count
            <<" recurrent="<<recurrent<<" ratio="<<(double)recurrent/primes.size()
            <<" nontrivial_SCCs="<<nontrivial_components<<" largest_SCC="<<largest
            <<" SCC_of_2="<<scc.size[component_of_two]<<"\n";
  for (int pos=0;pos<std::min<int>(20,ids.size());++pos) {
    int c=ids[pos];
    std::cout << "component rank="<<pos+1<<" size="<<scc.size[c]
              <<" min="<<primes[scc.minimum[c]]<<" max="<<primes[scc.maximum[c]]
              <<" contains2="<<(c==component_of_two)<<"\n";
  }

  // Dyadic prime/recurrent counts in the graph truncated at this X.  The
  // final two fields separate SCCs wholly contained in a bin cutoff B from
  // recurrent vertices <=B whose SCC extends past B.
  for (long long upper=4; upper/2<X; upper*=2) {
    int hi=static_cast<int>(std::min<long long>(upper,X));
    int lo=static_cast<int>(upper/2);
    int total_bin=0, recurring_bin=0, internal_vertices_le=0, extending_vertices_le=0;
    for (int i=0;i<(int)primes.size();++i) {
      int p=primes[i], c=scc.component[i]; bool rec=scc.size[c]>1;
      if (p>lo && p<=hi) {++total_bin;if(rec)++recurring_bin;}
      if (p<=hi && rec) {
        if (primes[scc.maximum[c]]<=hi) ++internal_vertices_le;
        else ++extending_vertices_le;
      }
    }
    std::cout << "bin=("<<lo<<","<<hi<<"] primes="<<total_bin
              <<" recurrent="<<recurring_bin
              <<" bin_ratio="<<(total_bin?(double)recurring_bin/total_bin:0.0)
              <<" recurrent_le="<<internal_vertices_le+extending_vertices_le
              <<" whole_SCC_le="<<internal_vertices_le
              <<" SCC_extends_past="<<extending_vertices_le<<"\n";
    if (hi==X) break;
  }

  // Decimal checkpoints are convenient for comparing this larger ambient
  // cutoff with separately recomputed induced graphs at the same checkpoint.
  for (long long bound=10; bound<=X; bound*=10) {
    int total=0, rec=0, wholly=0, extending=0;
    for (int i=0;i<(int)primes.size() && primes[i]<=bound;++i) {
      ++total; int c=scc.component[i];
      if (scc.size[c]>1) {
        ++rec;
        if (primes[scc.maximum[c]]<=bound) ++wholly; else ++extending;
      }
    }
    std::cout << "checkpoint_le="<<bound<<" primes="<<total<<" recurrent_in_X_graph="<<rec
              <<" whole_SCC_le="<<wholly<<" SCC_extends_past="<<extending<<"\n";
    if (bound > X/10) break;
  }
  std::cout << "nonrecurrent_primes_le_1000=";
  bool first=true;
  for (int i=0;i<(int)primes.size() && primes[i]<=1000;++i) {
    if (scc.size[scc.component[i]]>1) continue;
    if (!first) std::cout << ",";
    first=false; std::cout << primes[i];
  }
  std::cout << "\n";
}
