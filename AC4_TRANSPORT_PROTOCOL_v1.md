# AC4 spatial transport prerequisite

2026-09-14, before transport results. AC3 is frozen. This experiment tests a
physical transport kernel needed for the produced-boundary stage; it is not an
integrated autopoietic system and cannot satisfy that stage by itself.

Particles occupy integer coordinates in a 5 by 5 interior square surrounded
by an exterior medium. At each tick each particle proposes one unbiased cardinal
step. Twenty explicit membrane links span the square's perimeter. A positive
link lifetime reflects a crossing proposal; an absent link allows it. Particles
outside can return. Reaching absolute coordinate 6 exports a particle into an
absorbing external bath, recorded separately. There is no mortality function.

Particles retain identity and position. A species-selectivity mask determines
which particles a membrane reflects; permeant substrate is never reflected.
Selectivity, lattice geometry and diffusion are supplied physical assumptions.
No energy, production or controller is present in this prerequisite. In the
integrated stage, boundary creation must consume material and C-derived energy,
require local W, and be selected by vulnerable acquired information. That stage
must also replace W/C protected slots with transported, aging constituents.

Predeclared transport grid: seeds 0–15, 512 particles initially distributed
uniformly in the interior, 256 ticks, common proposal streams across arms.
Arms: open; intact (all links lifetime 512); decaying (lifetime 32); one-hole
(one absent link); permeant (intact but particles not reflected); retention
rescue (no membrane but explicitly imposed reflection at all perimeter links).
The last is an external intervention, never internal boundary production.

Report interior occupancy, unexported fraction, first crossing times, crossing
attempts and blocks. Preserve full per-seed rows and source/protocol hashes.
Required invariants: intact retains all impermeant particles; permeant matches
open exactly; retention rescue matches intact exactly; decaying matches intact
before expiry and permits later escape; every proposal is applied once or
reflected; interior, exterior and exported inventories sum to initial count.
One-hole versus open is descriptive, not a tuned pass criterion.

After this kernel is checked, integrate paid local boundary production and
measure its effect on real W/C inventories and controller information. A
boundary protecting only inert tracer particles will not establish closure.
