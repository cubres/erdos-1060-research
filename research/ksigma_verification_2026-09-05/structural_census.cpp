#include <algorithm>
#include <cstdint>
#include <cstdlib>
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

using u32 = std::uint32_t;
using u64 = std::uint64_t;
using u128 = unsigned __int128;

struct Entry { u64 h; u32 k; };
using Factor = std::vector<std::pair<u64, unsigned>>;

static std::string join(const std::vector<u32>& a) {
  std::ostringstream s;
  s << "{";
  for (std::size_t i = 0; i < a.size(); ++i) {
    if (i) s << ",";
    s << a[i];
  }
  return s.str() + "}";
}

static Factor factor_any(u64 n, const std::vector<u32>& lp,
                         const std::vector<u32>& primes) {
  Factor out;
  if (n < lp.size()) {
    u32 x = static_cast<u32>(n);
    while (x > 1) {
      const u32 p = lp[x];
      unsigned e = 0;
      do { x /= p; ++e; } while (x > 1 && lp[x] == p);
      out.push_back({p, e});
    }
    return out;
  }
  for (u32 p : primes) {
    if (static_cast<u64>(p) * p > n) break;
    if (n % p) continue;
    unsigned e = 0;
    do { n /= p; ++e; } while (n % p == 0);
    out.push_back({p, e});
  }
  if (n > 1) out.push_back({n, 1});
  return out;
}

static Factor factor_input(u32 k, const std::vector<u32>& lp) {
  Factor out;
  while (k > 1) {
    const u32 p = lp[k];
    unsigned e = 0;
    do { k /= p; ++e; } while (k > 1 && lp[k] == p);
    out.push_back({p, e});
  }
  return out;
}

static unsigned get_exp(const Factor& f, u64 p) {
  for (auto [q,e] : f) if (q == p) return e;
  return 0;
}

static Factor merge_factor(const Factor& a, const Factor& b) {
  std::map<u64,unsigned> m;
  for (auto [p,e] : a) m[p] += e;
  for (auto [p,e] : b) m[p] += e;
  return Factor(m.begin(), m.end());
}

static u64 sigma_pp(u64 p, unsigned e) {
  u128 power = 1, sum = 1;
  for (unsigned i = 0; i < e; ++i) { power *= p; sum += power; }
  if (sum > std::numeric_limits<u64>::max()) std::abort();
  return static_cast<u64>(sum);
}

struct DSU {
  std::vector<int> p;
  explicit DSU(int n) : p(n, -1) {}
  int find(int x) { return p[x] < 0 ? x : p[x] = find(p[x]); }
  void unite(int a, int b) {
    a=find(a); b=find(b); if (a==b) return;
    if (p[a] > p[b]) std::swap(a,b);
    p[a] += p[b]; p[b] = a;
  }
};

struct Column {
  u64 p;
  unsigned e;
  std::vector<std::pair<int,unsigned>> vals;
};

struct GraphStats {
  unsigned columns=0, rows=0, edges=0, components=0, mu=0;
};

static GraphStats graph_stats(const std::vector<Column>& cols, unsigned row_count,
                              bool include_all_rows=true) {
  DSU d(static_cast<int>(cols.size() + row_count));
  std::vector<char> used(cols.size() + row_count, 0);
  unsigned edges=0;
  for (unsigned j=0; j<cols.size(); ++j) {
    used[j]=1;
    for (auto [r,v] : cols[j].vals) {
      (void)v; used[cols.size()+r]=1; d.unite(j, cols.size()+r); ++edges;
    }
  }
  if (include_all_rows) for (unsigned r=0;r<row_count;++r) used[cols.size()+r]=1;
  std::set<int> roots;
  unsigned vertices=0;
  for (unsigned i=0;i<used.size();++i) if (used[i]) { ++vertices; roots.insert(d.find(i)); }
  GraphStats g;
  g.columns=cols.size(); g.rows=vertices-cols.size(); g.edges=edges;
  g.components=roots.size(); g.mu=edges-vertices+roots.size();
  return g;
}

static unsigned rank_mod(std::vector<std::vector<long long>> a, long long mod) {
  if (a.empty() || a[0].empty()) return 0;
  const int n=a.size(), m=a[0].size(); int row=0;
  auto power=[&](long long x,long long e){ long long r=1; while(e){if(e&1)r=(__int128)r*x%mod;x=(__int128)x*x%mod;e>>=1;}return r;};
  for (int col=0;col<m && row<n;++col) {
    int pivot=row; while(pivot<n && (a[pivot][col]%mod+mod)%mod==0) ++pivot;
    if(pivot==n) continue;
    std::swap(a[pivot],a[row]);
    long long inv=power((a[row][col]%mod+mod)%mod,mod-2);
    for(int j=col;j<m;++j) a[row][j]=(__int128)((a[row][j]%mod+mod)%mod)*inv%mod;
    for(int i=0;i<n;++i) if(i!=row) {
      long long x=(a[i][col]%mod+mod)%mod; if(!x) continue;
      for(int j=col;j<m;++j) a[i][j]=(a[i][j]-(__int128)x*a[row][j])%mod;
    }
    ++row;
  }
  return row;
}

static unsigned rank_two_mods(const std::vector<std::vector<long long>>& a) {
  return std::max(rank_mod(a,1000000007LL),rank_mod(a,1000000009LL));
}

static std::vector<Column> candidate_columns(u64 n, const Factor& nf) {
  std::vector<Column> out;
  for (unsigned ri=0;ri<nf.size();++ri) {
    const u64 p=nf[ri].first; const unsigned a=nf[ri].second;
    u128 pe=1, sig=1;
    for (unsigned e=1;e<=a;++e) {
      if (pe > static_cast<u128>(n)/p) break;
      pe *= p; sig += pe;
      const u128 hh=pe*sig;
      if (hh>n) break;
      const u64 h=static_cast<u64>(hh);
      if (n%h) continue;
      u64 x=h; Column c{p,e,{}};
      for (unsigned r=0;r<nf.size();++r) {
        unsigned v=0; const u64 q=nf[r].first;
        while(x%q==0){x/=q;++v;}
        if(v)c.vals.push_back({static_cast<int>(r),v});
      }
      if(x!=1){std::cerr<<"factor support failure\n";std::abort();}
      out.push_back(std::move(c));
    }
  }
  return out;
}

static std::vector<Column> pair_columns(const Factor& a, const Factor& b,
                                        const Factor& nf, u64 n) {
  std::set<u64> bases; for(auto [p,e]:a){(void)e;bases.insert(p);} for(auto [p,e]:b){(void)e;bases.insert(p);}
  std::vector<Column> out;
  for(u64 p:bases){
    unsigned ea=get_exp(a,p), eb=get_exp(b,p); if(ea==eb)continue;
    for(unsigned e:{ea,eb}) if(e){
      u128 pe=1; for(unsigned j=0;j<e;++j)pe*=p;
      u128 hh=pe*sigma_pp(p,e); if(hh>n || n%static_cast<u64>(hh)){std::cerr<<"bad block\n";std::abort();}
      u64 x=static_cast<u64>(hh); Column c{p,e,{}};
      for(unsigned r=0;r<nf.size();++r){unsigned v=0;u64 q=nf[r].first;while(x%q==0){x/=q;++v;}if(v)c.vals.push_back({static_cast<int>(r),v});}
      if(x!=1)std::abort(); out.push_back(std::move(c));
    }
  }
  return out;
}

static bool conformally_atomic(const Factor& a,const Factor& b,const Factor& nf,u64 n){
  struct Signed { int sign; std::vector<std::pair<int,unsigned>> vals; };
  std::set<u64>bases;for(auto[p,e]:a){(void)e;bases.insert(p);}for(auto[p,e]:b){(void)e;bases.insert(p);}
  std::vector<Signed> cs;
  for(u64 p:bases){unsigned ea=get_exp(a,p),eb=get_exp(b,p);if(ea==eb)continue;for(auto [e,sgn]:{std::pair<unsigned,int>{ea,1},{eb,-1}})if(e){u128 pe=1;for(unsigned z=0;z<e;++z)pe*=p;u64 h=static_cast<u64>(pe*sigma_pp(p,e));if(n%h)std::abort();u64 x=h;Signed s{sgn,{}};for(unsigned r=0;r<nf.size();++r){unsigned v=0;u64 q=nf[r].first;while(x%q==0){x/=q;++v;}if(v)s.vals.push_back({static_cast<int>(r),v});}if(x!=1)std::abort();cs.push_back(std::move(s));}}
  if(cs.size()>=63)return true; // Not reached in the exact census; avoid an unsafe shift.
  const u64 full=(1ULL<<cs.size())-1;
  std::vector<int> bal(nf.size());
  for(u64 mask=1;mask<full;++mask){std::fill(bal.begin(),bal.end(),0);for(unsigned c=0;c<cs.size();++c)if(mask>>c&1)for(auto[r,v]:cs[c].vals)bal[r]+=cs[c].sign*static_cast<int>(v);bool zero=true;for(int x:bal)if(x){zero=false;break;}if(zero)return false;}
  return true;
}

static std::pair<bool,unsigned> two_cycle_and_max_exponent(const Factor&a,const Factor&b){
  std::set<u64>bases;for(auto[p,e]:a){(void)e;bases.insert(p);}for(auto[p,e]:b){(void)e;bases.insert(p);}
  std::map<u64,std::vector<unsigned>> es;unsigned maxe=0;
  for(u64 p:bases){unsigned ea=get_exp(a,p),eb=get_exp(b,p);if(ea==eb)continue;if(ea){es[p].push_back(ea);maxe=std::max(maxe,ea);}if(eb){es[p].push_back(eb);maxe=std::max(maxe,eb);}}
  std::set<std::pair<u64,u64>> edges;
  for(auto const&[p,exps]:es)for(unsigned e:exps){u64 s=sigma_pp(p,e);for(auto const&[q,unused]:es){(void)unused;if(q!=p&&s%q==0)edges.insert({p,q});}}
  for(auto[p,q]:edges)if(edges.count({q,p}))return {true,maxe};
  return {false,maxe};
}

static bool moser_primitive(u32 a,u32 b,const std::vector<u64>& sigma,
                            const std::vector<u32>& lp) {
  u32 g=std::gcd(a,b); Factor gf=factor_input(g,lp); std::vector<u32> divs{1};
  for(auto [pp,ee]:gf){u32 p=static_cast<u32>(pp);std::size_t old=divs.size();u32 pe=1;for(unsigned e=1;e<=ee;++e){pe*=p;for(std::size_t i=0;i<old;++i)divs.push_back(divs[i]*pe);}}
  for(u32 d:divs) if(d>1){u32 x=a/d,y=b/d;if(static_cast<u128>(x)*sigma[x]==static_cast<u128>(y)*sigma[y])return false;}
  return true;
}

struct Extremum { unsigned value=0; u64 n=0; std::vector<u32> ks; std::string note; };
static void update_max(Extremum& e,unsigned v,u64 n,const std::vector<u32>&ks,const std::string&note=""){
  if(v>e.value)e={v,n,ks,note};
}
static void update_min(std::map<unsigned,Extremum>& m,unsigned mult,unsigned v,u64 n,const std::vector<u32>&ks,const std::string&note=""){
  if(!m.count(mult)||v<m[mult].value)m[mult]={v,n,ks,note};
}

int main(int argc,char**argv){
  u32 K=2000000; if(argc>1)K=static_cast<u32>(std::strtoull(argv[1],nullptr,10));
  const u64 X=static_cast<u64>(K)*K;
  std::vector<u32> lp(K),ppow(K,1),primes; std::vector<u64> sigma(K); sigma[1]=1;
  for(u32 i=2;i<K;++i){if(!lp[i]){lp[i]=i;ppow[i]=i;sigma[i]=static_cast<u64>(i)+1;primes.push_back(i);}for(u32 p:primes){u64 z=static_cast<u64>(i)*p;if(z>=K||p>lp[i])break;u32 ip=z;lp[ip]=p;if(p==lp[i]){ppow[ip]=ppow[i]*p;u32 core=i/ppow[i];sigma[ip]=sigma[i]+sigma[core]*ppow[ip];}else{ppow[ip]=p;sigma[ip]=sigma[i]*(static_cast<u64>(p)+1);}}}
  std::vector<Entry> values; values.reserve(K);
  for(u32 k=1;k<K;++k){u128 h=static_cast<u128>(k)*sigma[k];if(h<=X)values.push_back({static_cast<u64>(h),k});}
  std::sort(values.begin(),values.end(),[](auto&a,auto&b){return a.h<b.h||(a.h==b.h&&a.k<b.k);});

  u64 fibers=0,pairs=0,primitive_pairs=0,atomic_pairs=0,primitive_atomic_pairs=0,multi_candidate_components=0,parallelogram_fibers=0;
  Extremum max_mu,max_nullity,max_affdim,max_pair_blocks,max_pair_mu,max_pair_components,max_predecessors,max_primitive_blocks,max_atomic_blocks;
  std::map<unsigned,Extremum> min_mu_by_f,min_nullity_by_f,min_affdim_by_f;
  std::string first_largest_both_positive,first_largest_jump,first_multiple_predecessor,first_primitive_pair;
  std::string first_primitive_nonatomic,first_nonprimitive_atomic;
  std::string first_atomic_without_2cycle,first_primitive_atomic_cubefree_without_2cycle;
  std::vector<std::string> primitive_pair_lines;
  std::map<std::pair<unsigned,unsigned>,u64> affdim_hist;

  for(std::size_t i=0;i<values.size();){std::size_t j=i+1;while(j<values.size()&&values[j].h==values[i].h)++j;unsigned f=j-i;if(f<2){i=j;continue;}++fibers;
    u64 n=values[i].h;std::vector<u32> ks;std::vector<Factor> kfs;for(std::size_t t=i;t<j;++t){ks.push_back(values[t].k);kfs.push_back(factor_input(values[t].k,lp));}
    Factor nf=merge_factor(kfs[0],factor_any(sigma[ks[0]],lp,primes));
    auto cols=candidate_columns(n,nf);auto gs=graph_stats(cols,nf.size());
    std::vector<std::vector<long long>> A(nf.size(),std::vector<long long>(cols.size()));
    for(unsigned c=0;c<cols.size();++c)for(auto[r,v]:cols[c].vals)A[r][c]=v;
    unsigned rank=rank_two_mods(A),nullity=cols.size()-rank;
    if(f>(1ULL<<std::min(63u,gs.mu))){std::cerr<<"cycle bound violation\n";return 3;}
    update_max(max_mu,gs.mu,n,ks);update_max(max_nullity,nullity,n,ks);update_min(min_mu_by_f,f,gs.mu,n,ks);update_min(min_nullity_by_f,f,nullity,n,ks);
    if(gs.components>1)++multi_candidate_components;

    std::map<std::pair<u64,unsigned>,unsigned> colidx;for(unsigned c=0;c<cols.size();++c)colidx[{cols[c].p,cols[c].e}]=c;
    std::vector<std::vector<long long>> words(f,std::vector<long long>(cols.size()));
    for(unsigned a=0;a<f;++a)for(auto[p,e]:kfs[a]){auto it=colidx.find({p,e});if(it==colidx.end()){std::cerr<<"missing candidate\n";return 4;}words[a][it->second]=1;}
    std::vector<std::vector<long long>> diffs;for(unsigned a=1;a<f;++a){diffs.push_back(words[a]);for(unsigned c=0;c<cols.size();++c)diffs.back()[c]-=words[0][c];}
    unsigned affdim=rank_two_mods(diffs);affdim_hist[{f,affdim}]++;update_max(max_affdim,affdim,n,ks);update_min(min_affdim_by_f,f,affdim,n,ks);
    if(f>(1ULL<<affdim)){std::cerr<<"cube affine bound violation\n";return 5;}
    bool parallelogram=false;
    for(unsigned a=0;a<f&&!parallelogram;++a)for(unsigned b=a+1;b<f&&!parallelogram;++b)for(unsigned c=b+1;c<f&&!parallelogram;++c)for(unsigned d=c+1;d<f&&!parallelogram;++d){unsigned ids[4]={a,b,c,d};int pairings[3][4]={{0,1,2,3},{0,2,1,3},{0,3,1,2}};for(auto &pa:pairings){bool ok=true;for(unsigned z=0;z<cols.size();++z)if(words[ids[pa[0]]][z]+words[ids[pa[1]]][z]!=words[ids[pa[2]]][z]+words[ids[pa[3]]][z]){ok=false;break;}if(ok){parallelogram=true;break;}}}
    if(parallelogram)++parallelogram_fibers;

    unsigned primitive_edges=0;
    for(unsigned a=0;a<f;++a)for(unsigned b=a+1;b<f;++b){++pairs;bool prim=moser_primitive(ks[a],ks[b],sigma,lp);if(prim){++primitive_pairs;++primitive_edges;if(first_primitive_pair.empty())first_primitive_pair="n="+std::to_string(n)+" k={"+std::to_string(ks[a])+","+std::to_string(ks[b])+"}";primitive_pair_lines.push_back(std::to_string(n)+" "+std::to_string(ks[a])+" "+std::to_string(ks[b]));}
      auto pc=pair_columns(kfs[a],kfs[b],nf,n);bool atom=conformally_atomic(kfs[a],kfs[b],nf,n);if(atom){++atomic_pairs;update_max(max_atomic_blocks,pc.size(),n,ks,"pair="+std::to_string(ks[a])+","+std::to_string(ks[b]));if(prim)++primitive_atomic_pairs;else if(first_nonprimitive_atomic.empty())first_nonprimitive_atomic="n="+std::to_string(n)+" pair={"+std::to_string(ks[a])+","+std::to_string(ks[b])+"}";}else if(prim&&first_primitive_nonatomic.empty())first_primitive_nonatomic="n="+std::to_string(n)+" pair={"+std::to_string(ks[a])+","+std::to_string(ks[b])+"}";
      auto [has2,maxe]=two_cycle_and_max_exponent(kfs[a],kfs[b]);if(atom&&!has2&&first_atomic_without_2cycle.empty())first_atomic_without_2cycle="n="+std::to_string(n)+" pair={"+std::to_string(ks[a])+","+std::to_string(ks[b])+"} maxe="+std::to_string(maxe);if(atom&&prim&&maxe<=2&&!has2&&first_primitive_atomic_cubefree_without_2cycle.empty())first_primitive_atomic_cubefree_without_2cycle="n="+std::to_string(n)+" pair={"+std::to_string(ks[a])+","+std::to_string(ks[b])+"}";
      auto pg=graph_stats(pc,nf.size(),false);update_max(max_pair_blocks,pc.size(),n,ks,"pair="+std::to_string(ks[a])+","+std::to_string(ks[b]));update_max(max_pair_mu,pg.mu,n,ks);update_max(max_pair_components,pg.components,n,ks);if(prim)update_max(max_primitive_blocks,pc.size(),n,ks,"pair="+std::to_string(ks[a])+","+std::to_string(ks[b]));
      std::set<u64>bases;for(auto[p,e]:kfs[a]){(void)e;bases.insert(p);}for(auto[p,e]:kfs[b]){(void)e;bases.insert(p);}u64 P=0;unsigned eaP=0,ebP=0;for(u64 p:bases){unsigned ea=get_exp(kfs[a],p),eb=get_exp(kfs[b],p);if(ea!=eb){P=p;eaP=ea;ebP=eb;}}
      unsigned pred=0;std::vector<u64> predq;for(u64 q:bases)if(q<P){unsigned ea=get_exp(kfs[a],q),eb=get_exp(kfs[b],q);if(ea==eb)continue;bool hit=(ea&&sigma_pp(q,ea)%P==0)||(eb&&sigma_pp(q,eb)%P==0);if(hit){++pred;predq.push_back(q);}}
      if(!pred){std::cerr<<"predecessor violation n="<<n<<"\n";return 6;}update_max(max_predecessors,pred,n,ks,"P="+std::to_string(P));
      if(eaP&&ebP&&first_largest_both_positive.empty())first_largest_both_positive="n="+std::to_string(n)+" pair={"+std::to_string(ks[a])+","+std::to_string(ks[b])+"} P="+std::to_string(P)+" exps="+std::to_string(eaP)+","+std::to_string(ebP);
      if((eaP>ebP?eaP-ebP:ebP-eaP)>1&&first_largest_jump.empty())first_largest_jump="n="+std::to_string(n)+" pair={"+std::to_string(ks[a])+","+std::to_string(ks[b])+"} P="+std::to_string(P)+" exps="+std::to_string(eaP)+","+std::to_string(ebP);
      if(pred>1&&first_multiple_predecessor.empty()){first_multiple_predecessor="n="+std::to_string(n)+" pair={"+std::to_string(ks[a])+","+std::to_string(ks[b])+"} P="+std::to_string(P)+" q=";for(u64 q:predq)first_multiple_predecessor+=std::to_string(q)+",";}
    }
    (void)primitive_edges;i=j;
  }
  auto pe=[&](const char*name,const Extremum&e){std::cout<<name<<"="<<e.value<<" n="<<e.n<<" k="<<join(e.ks);if(!e.note.empty())std::cout<<" "<<e.note;std::cout<<"\n";};
  std::cout<<"K="<<K<<" X="<<X<<" collision_fibers="<<fibers<<" pairs="<<pairs<<" primitive_pairs="<<primitive_pairs<<" atomic_pairs="<<atomic_pairs<<" primitive_atomic_pairs="<<primitive_atomic_pairs<<"\n";
  pe("max_candidate_cycle_rank",max_mu);pe("max_candidate_modular_nullity",max_nullity);pe("max_fiber_affine_dim",max_affdim);pe("max_pair_differing_blocks",max_pair_blocks);pe("max_pair_cycle_rank",max_pair_mu);pe("max_pair_components",max_pair_components);pe("max_largest_predecessor_count",max_predecessors);pe("max_Moser_primitive_pair_blocks",max_primitive_blocks);pe("max_conformally_atomic_pair_blocks",max_atomic_blocks);
  std::cout<<"min_candidate_mu_by_f";for(auto const&[f,e]:min_mu_by_f)std::cout<<" f="<<f<<":"<<e.value<<"@"<<e.n;std::cout<<"\n";
  std::cout<<"min_candidate_nullity_by_f";for(auto const&[f,e]:min_nullity_by_f)std::cout<<" f="<<f<<":"<<e.value<<"@"<<e.n;std::cout<<"\n";
  std::cout<<"min_affdim_by_f";for(auto const&[f,e]:min_affdim_by_f)std::cout<<" f="<<f<<":"<<e.value<<"@"<<e.n;std::cout<<"\n";
  std::cout<<"affdim_hist";for(auto const&[key,c]:affdim_hist)std::cout<<" f="<<key.first<<",d="<<key.second<<":"<<c;std::cout<<"\n";
  std::cout<<"multi_candidate_components="<<multi_candidate_components<<" parallelogram_fibers="<<parallelogram_fibers<<"\n";
  std::cout<<"first_Moser_primitive_pair="<<first_primitive_pair<<"\n";
  std::cout<<"first_largest_both_positive="<<first_largest_both_positive<<"\n";
  std::cout<<"first_largest_exponent_jump="<<first_largest_jump<<"\n";
  std::cout<<"first_multiple_predecessors="<<first_multiple_predecessor<<"\n";
  std::cout<<"first_Moser_primitive_but_conformally_decomposable="<<first_primitive_nonatomic<<"\n";
  std::cout<<"first_Moser_nonprimitive_but_conformally_atomic="<<first_nonprimitive_atomic<<"\n";
  std::cout<<"first_conformal_atom_without_directed_2cycle="<<first_atomic_without_2cycle<<"\n";
  std::cout<<"first_Moser_primitive_cubefree_atom_without_directed_2cycle="<<first_primitive_atomic_cubefree_without_2cycle<<"\n";
  std::cout<<"primitive_pair_list\n";for(const auto&s:primitive_pair_lines)std::cout<<s<<"\n";
}
