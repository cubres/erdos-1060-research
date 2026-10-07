#include <algorithm>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <numeric>
#include <set>
#include <sstream>
#include <string>
#include <vector>

using u32=std::uint32_t;using u64=std::uint64_t;using u128=unsigned __int128;
struct Entry{u64 h;u32 k;};
struct Candidate{u64 n;u32 a,b;std::vector<u32> support;unsigned v2,maxv;};

static std::vector<std::pair<u64,unsigned>> factor_any(u64 n,const std::vector<u32>&lp,const std::vector<u32>&primes){
 std::vector<std::pair<u64,unsigned>> f;if(n<lp.size()){u32 x=n;while(x>1){u32 p=lp[x];unsigned e=0;do{x/=p;++e;}while(x>1&&lp[x]==p);f.push_back({p,e});}return f;}
 for(u32 p:primes){if((u64)p*p>n)break;if(n%p)continue;unsigned e=0;do{n/=p;++e;}while(n%p==0);f.push_back({p,e});}if(n>1)f.push_back({n,1});return f;
}
static std::vector<u32> support(u32 a,u32 b,const std::vector<u32>&lp){std::vector<u32>s;for(u32 x:{a,b})while(x>1){u32 p=lp[x];s.push_back(p);while(x%p==0)x/=p;}std::sort(s.begin(),s.end());s.erase(std::unique(s.begin(),s.end()),s.end());return s;}
static bool disjoint(const std::vector<u32>&a,const std::vector<u32>&b){std::size_t i=0,j=0;while(i<a.size()&&j<b.size()){if(a[i]==b[j])return false;if(a[i]<b[j])++i;else++j;}return true;}
static bool primitive(u32 a,u32 b,const std::vector<u64>&sigma,const std::vector<u32>&lp){u32 g=std::gcd(a,b);std::vector<u32>divs{1};while(g>1){u32 p=lp[g],pe=1;unsigned e=0;while(g%p==0){g/=p;++e;}std::size_t old=divs.size();for(unsigned z=1;z<=e;++z){pe*=p;for(std::size_t i=0;i<old;++i)divs.push_back(divs[i]*pe);}}for(u32 d:divs)if(d>1){u32 x=a/d,y=b/d;if((u128)x*sigma[x]==(u128)y*sigma[y])return false;}return true;}
static std::string show(const std::vector<u32>&s){std::ostringstream o;o<<"{";for(std::size_t i=0;i<s.size();++i){if(i)o<<",";o<<s[i];}return o.str()+"}";}

int main(int argc,char**argv){u32 K=argc>1?std::strtoull(argv[1],nullptr,10):10000000;u64 X=(u64)K*K;
 std::vector<u32>lp(K),ppow(K,1),primes;std::vector<u64>sigma(K);sigma[1]=1;
 for(u32 i=2;i<K;++i){if(!lp[i]){lp[i]=i;ppow[i]=i;sigma[i]=(u64)i+1;primes.push_back(i);}for(u32 p:primes){u64 z=(u64)i*p;if(z>=K||p>lp[i])break;u32 ip=z;lp[ip]=p;if(p==lp[i]){ppow[ip]=ppow[i]*p;u32 core=i/ppow[i];sigma[ip]=sigma[i]+sigma[core]*ppow[ip];}else{ppow[ip]=p;sigma[ip]=sigma[i]*((u64)p+1);}}}
 std::vector<Entry>values;values.reserve(K);for(u32 k=1;k<K;++k){u128 h=(u128)k*sigma[k];if(h<=X)values.push_back({(u64)h,k});}std::sort(values.begin(),values.end(),[](auto&a,auto&b){return a.h<b.h||(a.h==b.h&&a.k<b.k);});
 std::vector<Candidate>cs;u64 pairs=0;
 for(std::size_t i=0;i<values.size();){std::size_t j=i+1;while(j<values.size()&&values[j].h==values[i].h)++j;if(j-i>1)for(std::size_t a=i;a<j;++a)for(std::size_t b=a+1;b<j;++b){++pairs;if(!primitive(values[a].k,values[b].k,sigma,lp))continue;auto nf=factor_any(values[a].h,lp,primes);unsigned v2=0,mx=0;for(auto[p,e]:nf){if(p==2)v2=e;mx=std::max(mx,e);}cs.push_back({values[a].h,values[a].k,values[b].k,support(values[a].k,values[b].k,lp),v2,mx});}i=j;}
 std::vector<std::vector<char>>ok(cs.size(),std::vector<char>(cs.size()));for(std::size_t i=0;i<cs.size();++i)for(std::size_t j=i+1;j<cs.size();++j)ok[i][j]=ok[j][i]=disjoint(cs[i].support,cs[j].support);
 std::vector<int>best,current;
 auto dfs=[&](auto&&self,int start){if(current.size()>best.size())best=current;if(current.size()+cs.size()-start<=best.size())return;for(int i=start;i<(int)cs.size();++i){bool good=true;for(int j:current)if(!ok[i][j]){good=false;break;}if(good){current.push_back(i);self(self,i+1);current.pop_back();}}};dfs(dfs,0);
 u64 compatible_pairs=0,compatible_triples=0;for(std::size_t i=0;i<cs.size();++i)for(std::size_t j=i+1;j<cs.size();++j)if(ok[i][j]){++compatible_pairs;for(std::size_t k=j+1;k<cs.size();++k)if(ok[i][k]&&ok[j][k])++compatible_triples;}
 std::cout<<"K="<<K<<" X="<<X<<" all_pairs="<<pairs<<" primitive_pairs="<<cs.size()<<" compatible_pairs="<<compatible_pairs<<" compatible_triples="<<compatible_triples<<" max_pack="<<best.size()<<"\n";
 for(int i:best){auto&c=cs[i];std::cout<<"PACK n="<<c.n<<" pair="<<c.a<<","<<c.b<<" v2="<<c.v2<<" maxv="<<c.maxv<<" support="<<show(c.support)<<"\n";}
 std::cout<<"COMPATIBLE_PAIRS\n";for(std::size_t i=0;i<cs.size();++i)for(std::size_t j=i+1;j<cs.size();++j)if(ok[i][j])std::cout<<cs[i].a<<","<<cs[i].b<<" @"<<cs[i].n<<" -- "<<cs[j].a<<","<<cs[j].b<<" @"<<cs[j].n<<" total_v2="<<cs[i].v2+cs[j].v2<<"\n";
 std::cout<<"PRIMITIVE_LIST\n";for(auto&c:cs)std::cout<<c.n<<" "<<c.a<<" "<<c.b<<" v2="<<c.v2<<" maxv="<<c.maxv<<" support="<<show(c.support)<<"\n";
}
