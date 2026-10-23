import sympy as sp
b,k,th,D=sp.symbols('beta kappa theta D',positive=True)
zm,zp=(1-D)/2,(1+D)/2
A=lambda z: th-k*z+sp.log(z/(1-z))/b
a_on=th-k/2+sp.Rational(1,2)*(k*D-4/b*sp.atanh(D)); a_off=th-k/2-sp.Rational(1,2)*(k*D-4/b*sp.atanh(D))
print("a_on - A(z-) =",sp.simplify(sp.expand_log(A(zm)-a_on.rewrite(sp.log),force=True)))
print("a_off - A(z+) =",sp.simplify(sp.expand_log(A(zp)-a_off.rewrite(sp.log),force=True)))
z=sp.symbols('z'); print("A'(z)=0 at z(1-z)=1/(beta kappa):",sp.simplify(sp.diff(A(z),z).subs(z,zm).subs(b,4/(k*(1-D**2)))))
W=(k*D-4/b*sp.atanh(D)).subs(b,4/(k*(1-D**2)))
print("width (beta eliminated) =",sp.simplify(W)," series:",sp.series(W,D,0,7))
W2=(k*D-4/b*sp.atanh(D)); print("series at fixed beta:",sp.series(W2,D,0,5))
