#!/usr/bin/env python3
"""High-precision and finite-range checks for the Rankin variational constant."""

from decimal import Decimal, getcontext


getcontext().prec = 80
D = Decimal


def polynomial(x: Decimal) -> Decimal:
    return D(3) - x * x - D(3) * x**3


def newton_root() -> Decimal:
    x = D("0.9")
    for _ in range(30):
        x -= polynomial(x) / (-D(2) * x - D(9) * x * x)
    return x


def main() -> None:
    x = newton_root()
    lam = -x.ln()
    s3 = D(1) + x**2 + x**3
    constant = lam / D(2) + s3.ln() / D(3)
    print(f"x={x}")
    print(f"lambda={lam}")
    print(f"C={constant}")

    # Exact-sign rational enclosure for the unique root (the polynomial is
    # strictly decreasing on (0,1)).
    lo, hi = D("0.9"), D("0.91")
    assert polynomial(lo) > 0 > polynomial(hi)

    # A certificate for x < log(S_3): for 0<=u<=0.91,
    # exp(u) <= 1+u+u^2/[2(1-u/3)], since j! >= 2*3^(j-2), j>=2.
    exp_upper = D(1) + hi + hi**2 / (D(2) * (D(1) - hi / D(3)))
    s3_lower = D(1) + lo**2 + lo**3
    assert exp_upper < s3_lower
    assert x.exp() < s3
    print(f"certificate: exp(x)<={exp_upper}<={s3_lower}<=S3")

    # a=2 comparison: S_3^2-S_2^3 = x^2*g(x), and g is increasing
    # because g'(x)=2-4x+6x^2 has negative discriminant.
    g_lo = -D(1) + D(2) * lo - D(2) * lo**2 + D(2) * lo**3
    assert g_lo > 0
    assert s3**2 > (D(1) + x**2) ** 3

    # Empirical supplement to the infinite monotonicity proof: at the root,
    # log(S_a)/a decreases from a=3 onward.  The proof uses
    # S_a>=a*x^a and x<log(S_3), not this loop.
    s = D(1)
    previous = None
    best = (D(-1), -1)
    for a in range(2, 100_001):
        s += x**a
        phi = s.ln() / D(a)
        if phi > best[0]:
            best = (phi, a)
        if a >= 4:
            assert phi < previous
        previous = phi
    assert best[1] == 3
    print(f"finite sup check through a=100000: maximizing a={best[1]}")


if __name__ == "__main__":
    main()
