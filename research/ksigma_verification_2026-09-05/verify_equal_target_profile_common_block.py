#!/usr/bin/env python3
"""Verify an explicit cubefree equal-target-profile h-collision exactly."""

from collections import Counter
from math import gcd

from sympy import divisor_sigma, factorint, isprime


A = 60629697601617236747379985403
B = 61655391632564660609643619057
R = 5503


def h(k: int) -> int:
    return k * int(divisor_sigma(k))


def positive_profile(k: int, target_factorization: dict[int, int]):
    return sorted(
        (target_factorization[p], e) for p, e in factorint(k).items()
    )


def main() -> None:
    x, y = A * R, B * R
    hx, hy = h(x), h(y)
    assert hx == hy
    assert isprime(R) and factorint(R + 1) == {2: 7, 43: 1}
    assert gcd(A * B, R) == 1
    xf, yf = factorint(x), factorint(y)
    assert max(xf.values()) == max(yf.values()) == 2
    nf = {int(p): int(e) for p, e in factorint(hx).items()}
    xp, yp = positive_profile(x, nf), positive_profile(y, nf)
    assert xp == yp
    assert Counter(xp) == Counter({(1, 1): 5, (2, 1): 4, (2, 2): 4})
    print("PASS exact common h")
    print("PASS both inputs cubefree")
    print("PASS equal positive target profiles")
    print(f"x={x}")
    print(f"y={y}")
    print(f"n={hx}")
    print(f"gcd(x,y)={gcd(x,y)}")
    print(f"profile={xp}")


if __name__ == "__main__":
    main()
