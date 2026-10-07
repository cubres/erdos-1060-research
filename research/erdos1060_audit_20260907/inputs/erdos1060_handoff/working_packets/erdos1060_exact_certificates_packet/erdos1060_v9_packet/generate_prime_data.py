"""Generate local factorizations for subsequent exact certificate checking.
Requires SymPy. Its factorizations are independently checked by the verifiers.
"""
from __future__ import annotations
import argparse,json
from pathlib import Path
from sympy import primerange,factorint

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--limit',type=int,default=1000000)
    parser.add_argument('--output',type=Path,default=Path('prime_graph_1000000.json'))
    args=parser.parse_args()
    if args.limit<5:parser.error('The prime limit must be at least 5.')
    data={'limit':args.limit,'factors':{}}
    for pp in primerange(5,args.limit+1):
        p=int(pp)
        data['factors'][p]={e:{int(q):int(v) for q,v in factorint(sum(p**i for i in range(e+1))).items()}
                            for e in (1,2)}
    args.output.write_text(json.dumps(data)+'\n')
    print(f'Wrote local factorizations for {len(data["factors"])} input primes.')
