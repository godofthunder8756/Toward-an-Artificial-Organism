# SUB-A0 prior art v1

2026-10-01. Targeted primary-source review performed AFTER the
[supplied-substrate boundary](SUB_A0_SUBSTRATE_BOUNDARY_v1.md) was frozen.
This is a design review, not experimental evidence or a novelty claim.

## Requested precedents

### P1. Schmidhuber (1993): self-referential weight matrices

J. Schmidhuber, *A "Self-Referential" Weight Matrix*, ICANN '93, Springer
London. [Publisher-deposited Crossref metadata](https://api.crossref.org/works/10.1007/978-1-4471-2063-6_107)
and [DOI](https://doi.org/10.1007/978-1-4471-2063-6_107).
Crossref gives pages 446-450; the author's bibliography gives 446-451.
These are recorded as a bibliographic discrepancy, not silently reconciled.

Primary full text: [author-hosted article](https://people.idsia.ch/~juergen/selfref/selfref.html),
including [mechanism](https://people.idsia.ch/~juergen/selfref/node1.html),
[formal description](https://people.idsia.ch/~juergen/selfref/node2.html),
[training](https://people.idsia.ch/~juergen/selfref/node4.html) and
[discussion](https://people.idsia.ch/~juergen/selfref/node5.html).

**Mechanism:** connections have addresses; analyzing outputs select weights
to read, and modifying outputs select connections and weight changes. The
network can modify the connections implementing its own modification process.
Differentiable read/write/address mechanisms and external gradient training of
initial weights are specified. This is not self-originating learning.

**Evidence boundary:** discussion presents a theoretical possibility/thought
experiment, not acquired-skill repair under shared damage. Self-modifiable
does not mean damage-tested. Generic read/write machinery is supplied.
No disproportionate repair-allocation assay is reported.

### P2. Irie, Schlag, Csordas and Schmidhuber (2022)

*A Modern Self-Referential Weight Matrix That Learns to Modify Itself*,
ICML, PMLR 162:9660-9677.
[Official record](https://proceedings.mlr.press/v162/irie22b.html),
[primary paper](https://proceedings.mlr.press/v162/irie22b/irie22b.pdf),
[arXiv record](https://arxiv.org/abs/2202.05780).

**Mechanism:** section 3, equations 5-8 (PDF page 3), and Appendix A
(PDF page 13): the live matrix generates output, key, query and update-rate
signals. It reads itself at key/query locations and performs a delta-rule
outer-product update. Thus the updated matrix includes the computations
generating future keys, queries and update rates. The implemented version
uses separate rates for four submatrices. Initial parameters are gradient-
trained externally.

**Evidence boundary:** experiments establish useful self-modification for
task adaptation, not restoration of arbitrarily corrupted acquired weights.
The full agents also contain learned layers outside the SRWM, such as visual
components; "all of itself" refers to the layer, not automatically every
learned coefficient in the agent. Sections 4.1-4.3 and Appendix B describe
these distinctions. Episodic runtime state resets and learned initialization
must not become a protected acquired template in SUB-A0.

No shared corruption of every learned task/repair coefficient, allocation-
enrichment endpoint or functional repair-versus-write assay is established.
A0 can borrow the mechanism, not inherit the missing evidence.

### P3. von Neumann (1956): multiplexing

*Probabilistic Logics and the Synthesis of Reliable Organisms from Unreliable
Components*, in Shannon and McCarthy (eds.), *Automata Studies*, Annals of
Mathematics Studies 34, Princeton University Press, pp. 43-98.
[Crossref metadata](https://api.crossref.org/works/10.1515/9781400882618-003),
[DOI](https://doi.org/10.1515/9781400882618-003),
[published chapter scan](https://www.dna.caltech.edu/courses/cs191/paperscs191/VonNeumann56.pdf).

**Access qualification:** the image-only published scan was visually spot-
checked, not extracted as a fully machine-readable article. The closely
related 1952 lecture [original scan](https://archive.org/details/vonNeumann_Prob_Logics_Rel_Org_Unrel_Comp_Caltech_1952)
and [identified corrected transcription](https://archive.org/details/von_Neumann_Probabilistic_Logics_Caltech_Lecture_1952)
provided readable corroboration. The transcription is editorial, not a new
1956 publication.

**Mechanism:** published sections 9.2.2-9.3, pp. 71-73: signals are carried by
bundles; executive organs implement logic and restoring organs reduce a
minority of errors. Majority restoration has idealized error mapping
`3 p^2 - 2 p^3`. The restoration components need not be perfect. The stipulated
component-failure assumptions, including independence, are consequential
(published section 7.1, pp. 61-62; related lecture sections 9-11).

**Evidence boundary:** prescribed noisy-component restoration is not learned
allocation to mutable repair parameters. Signal restoration is not replacement
of the learned coefficients implementing repair. Correlated recurrent failures
cannot be treated as covered by an independent-fault calculation.

## Supporting reduction anchors

- [Fauth and van Rossum (2019)](https://pmc.ncbi.nlm.nih.gov/articles/PMC6546393/),
  *Self-organized reactivation maintains and reinforces memories despite
  synaptic turnover*: recurrent assemblies reactivate and maintain connectivity.
  Results/Figs. 1, 4-7 distinguish synapse replacement from retrieval-cue
  robustness. Plasticity and activity laws remain prescribed.
- [Fauth, Woergoetter and Tetzlaff (2015)](https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1004684),
  *Formation and Maintenance of Robust Long-Term Information Storage in the
  Presence of Synaptic Turnover*: multi-synapse bistability is a strong simpler
  maintenance rival, not evidence against maintenance itself. Models and
  Methods specify the supplied formation/deletion laws. The ASCII reference
  uses Woergoetter for the author's surname.

## What A0 adds, relative to these studies

The proposed empirical conjunction, NOT demonstrated here, is:

1. Every learned coefficient that computes repair, including self-updates, is
   damageable under the pre-frozen boundary.
2. The controller is trained only on task/prediction outcomes, with no term for
   repair volume, preservation, survival or preferential repair of its own
   machinery.
3. Allocation is measured per available write opportunity, contrasting balanced
   damage with sham, rather than counting raw writes to a larger bank.
4. Performing-machinery priority must follow functional role across randomized
   physical locations and matter for subsequent repair capacity and task use.
5. Ordinary coding and task-value-sensitive control remain live explanations.
   A result may establish bounded instrumental self-maintenance without
   establishing a new source of priorities or a consciousness-specific mechanism.

This is a sharper experiment than self-modification alone, not a claim of
historical priority. No reviewed source proves the whole conjunction impossible
or sufficient for consciousness.

## Retrieval discipline

Metadata retrieval used API/proceedings/author records rather than search-engine
scraping. HTTPS verification remained enabled; there was no insecure flag or
TLS-bypass retry. Browser/tool retrieval used verified HTTPS transports.
This design package configures no custom HTTP client or certificate override.
Any later Python retrieval must use the system trust store through `truststore`
or an appropriate `REQUESTS_CA_BUNDLE`, with verification enabled. No credentials
or private repository content were transmitted in literature queries.
Failed retrieval is an access limitation, never a reason to disable verification.
