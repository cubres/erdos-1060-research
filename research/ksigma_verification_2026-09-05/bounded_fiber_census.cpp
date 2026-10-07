#include <algorithm>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <map>
#include <numeric>
#include <sstream>
#include <vector>

// Complete finite census for the bounded-exponent part of h(k)=k*sigma(k).
// If h(k)<=K^2, then k<K (apart from the harmless k=1 endpoint), so the
// retained fibers are complete, not truncations in the input variable.

using u32 = std::uint32_t;
using u64 = std::uint64_t;
using u128 = unsigned __int128;

struct Entry { u64 h; u32 k; };

static std::string join(const std::vector<u32>& xs) {
  std::ostringstream out;
  out << "[";
  for (std::size_t i=0;i<xs.size();++i) {
    if (i) out << ",";
    out << xs[i];
  }
  return out.str()+"]";
}

int main(int argc,char**argv) {
  const u32 K = argc>1 ? static_cast<u32>(std::strtoull(argv[1],nullptr,10)) : 10000000;
  const unsigned R = argc>2 ? static_cast<unsigned>(std::strtoul(argv[2],nullptr,10)) : 3;
  if (K<3 || R<2) return 2;
  const u64 X=static_cast<u64>(K)*K;

  std::vector<u32> least(K), ppow(K,1), primes;
  std::vector<u64> sigma(K);
  std::vector<unsigned char> maxexp(K);
  sigma[1]=1;
  for(u32 i=2;i<K;++i) {
    if(!least[i]) {
      least[i]=i; ppow[i]=i; sigma[i]=static_cast<u64>(i)+1;
      maxexp[i]=1; primes.push_back(i);
    }
    for(u32 p:primes) {
      const u64 z=static_cast<u64>(i)*p;
      if(z>=K || p>least[i]) break;
      const u32 ip=static_cast<u32>(z); least[ip]=p;
      if(p==least[i]) {
        ppow[ip]=ppow[i]*p;
        const u32 core=i/ppow[i];
        sigma[ip]=sigma[i]+sigma[core]*ppow[ip];
        unsigned e=0; for(u32 t=ppow[ip];t>1;t/=p) ++e;
        maxexp[ip]=static_cast<unsigned char>(std::max<unsigned>(maxexp[core],e));
      } else {
        ppow[ip]=p; sigma[ip]=sigma[i]*(static_cast<u64>(p)+1);
        maxexp[ip]=std::max<unsigned char>(maxexp[i],1);
      }
    }
  }

  std::vector<Entry> values; values.reserve(K);
  for(u32 k=1;k<K;++k) if(maxexp[k]<R) {
    const u128 h=static_cast<u128>(k)*sigma[k];
    if(h<=X) values.push_back({static_cast<u64>(h),k});
  }
  std::sort(values.begin(),values.end(),[](const Entry&a,const Entry&b){
    return a.h<b.h || (a.h==b.h && a.k<b.k);
  });

  std::map<unsigned,u64> hist;
  std::map<unsigned,std::pair<u64,std::vector<u32>>> first;
  unsigned maxf=1; u64 fibers=0,pairs=0;
  for(std::size_t i=0;i<values.size();) {
    std::size_t j=i+1; while(j<values.size()&&values[j].h==values[i].h) ++j;
    const unsigned f=static_cast<unsigned>(j-i); ++hist[f];
    if(f>=2) {
      ++fibers; pairs+=static_cast<u64>(f)*(f-1)/2; maxf=std::max(maxf,f);
      std::vector<u32> ks; for(std::size_t z=i;z<j;++z) ks.push_back(values[z].k);
      if(!first.count(f)) first[f]={values[i].h,ks};
      if(f>=3) std::cout << "fiber n=" << values[i].h << " f=" << f << " k=" << join(ks) << "\n";
    }
    i=j;
  }
  std::cout << "summary K="<<K<<" exact_n_max="<<X<<" R="<<R
            <<" retained="<<values.size()<<" collision_fibers="<<fibers
            <<" pairs="<<pairs<<" max_f="<<maxf<<"\n";
  std::cout << "hist"; for(auto [f,c]:hist) std::cout<<" "<<f<<":"<<c; std::cout<<"\n";
  for(auto const& [f,data]:first) std::cout<<"first f="<<f<<" n="<<data.first<<" k="<<join(data.second)<<"\n";
}
