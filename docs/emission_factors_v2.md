# CO2 Emission Factors for Concrete / UHPC Mix Ingredients (v2)

Cradle-to-gate (A1–A3) emission factors in **kg CO2e per kg material**, compiled from peer-reviewed open-access literature for use in a concrete carbon emissions prediction tool.

**Changes from v1:**
- Aggregate defaults (coarse and fine) lowered to reflect UHPC-specific LCA sources (Sameer 2019, Randl 2014, Purnell & Black 2012). v1 defaults were on the high end and included an implicit long-haul transport allowance.
- Steel fiber defaults revised: virgin fiber default lowered to match Bekaert Dramix EPD and worldsteel LCI; recycled fiber default raised slightly to include drawing/cutting energy (per Colombo 2022 review).
- Weak citations replaced: Wang 2023 removed in favor of Sameer et al. 2019 (UHPC-specific, open-access). worldsteel methodology report replaced with worldsteel 2023 LCI dataset + Bekaert EPD.
- Added authoritative cement/SCM references (Habert 2020, Miller 2021, Scrivener 2018, Purnell & Black 2012).

---

## Emission Factors Table

| Code | Material | Default (kg CO2e/kg) | Low | High | Source |
|------|----------|---------------------:|----:|-----:|--------|
| C    | Cement (OPC, Portland CEM I)      | 0.830    | 0.740   | 0.950  | [1], [3], [4] |
| W    | Water (municipal, treated)         | 0.000196 | 0.0001  | 0.0008 | [1] |
| FA   | Fly Ash (PFA, coal byproduct)      | 0.009    | 0.004   | 0.050  | [1], [5], [6] |
| SF   | Silica Fume                        | 0.014    | 0.014   | 0.143  | [1], [5] |
| NS   | Nano-Silica                        | 1.500    | 0.500   | 3.000  | [8] |
| QP   | Quartz Powder                      | 0.0237   | 0.016   | 0.048  | [1], [2] |
| LP   | Limestone Powder                   | 0.017    | 0.007   | 0.032  | [6], [7] |
| A_c  | Aggregate — Coarse (gravel/crushed)| 0.008    | 0.005   | 0.054  | [1], [5] |
| A_f  | Aggregate — Fine (sand/quartz)     | 0.005    | 0.003   | 0.026  | [1], [2] |
| S    | Slag (GGBS / GGBFS)                | 0.052    | 0.019   | 0.083  | [5], [6], [10] |
| SP   | Superplasticizer                   | 0.944    | 0.720   | 2.200  | [1], [9] |
| Fi_s | Steel Fiber — Virgin (BF-BOF)      | 2.500    | 1.900   | 3.200  | [11], [12], [13] |
| Fi_r | Steel Fiber — Recycled (EAF)       | 0.900    | 0.500   | 1.300  | [11], [12], [13] |

---

## Notes on Material Variants

### Aggregate
Two types provided. If your mix design separates coarse and fine aggregate, use the individual values. If aggregate is entered as a single combined input, use a weighted average (typical normal concrete mix is roughly 65% coarse / 35% fine by mass).

- **Coarse aggregate (A_c):** Gravel or crushed stone, typically 5–20 mm.
- **Fine aggregate (A_f):** Natural or manufactured sand (for UHPC: fine quartz sand), typically < 5 mm.
- **Combined default (A):** ≈ 0.007 kg CO2e/kg (weighted avg at 65/35 split).
- **UHPC note:** UHPC mixes typically use only fine aggregate (quartz sand). The fine-aggregate factor (A_f) should be used as the UHPC default.

### Steel Fiber
Two types provided based on production route.

- **Virgin steel (Fi_s):** Produced via blast furnace / basic oxygen furnace (BF-BOF) from iron ore. Default 2.50 is aligned with Bekaert Dramix EPD and worldsteel LCI for drawn + cut fiber product.
- **Recycled steel (Fi_r):** Produced via electric arc furnace (EAF) from scrap. Default 0.90 includes drawing and cutting energy (per Colombo 2022 review). Represents roughly a 65% reduction versus virgin. Regional supply and scrap content vary — confirm with supplier EPD when possible.

---

## Important Caveats

- **Nano-silica** has wide variance in the literature (0.5–3.0 kg CO2/kg) because production methods differ dramatically (sol-gel vs. precipitated vs. pyrogenic). Mid-range value used as default.
- **Fly ash and slag** values are allocation-dependent. These are industrial byproducts (coal combustion and steel production, respectively), and different LCA studies use different allocation methods:
  - *Cut-off / waste allocation:* near-zero emissions (only processing counted).
  - *Economic allocation:* moderate emissions (a share of the parent process).
  - *Mass allocation:* higher emissions.
  The values here use economic or hybrid allocation. Document your choice in reporting.
- **Steel fiber** emission depends heavily on virgin vs. recycled content. Confirm your fiber supplier's EPD if possible.
- **Aggregate** values now reflect UHPC-specific quartz sand and local-supply crushed stone. Long-haul imported aggregate may be 3–5× higher; adjust upward if your project context involves significant transport distances (A4 boundary).
- **Superplasticizer** has a very high per-kg factor but is used in very small quantities (typically 0.2–2% of binder mass), so its absolute contribution to the mix is usually modest. The factor applies to solid content; liquid admixtures are typically 30–40% solids.
- **Regional variance:** Values can shift ±30% across regional LCA databases (EU, US, China, Japan). Values compiled here are representative global/peer-reviewed averages. **Not suitable for procurement, regulatory compliance, or EPD reporting.**
- **Methodological consistency:** Factors are compiled from multiple sources with differing system boundaries, allocation choices, and reference grids. No attempt has been made to harmonize across sources; values are taken as reported. A formal LCA study would use a single database (e.g., ecoinvent, ICE v4.1) end-to-end.
- **Scope:** All factors are cradle-to-gate (A1–A3). They exclude construction (A4–A5), use phase (B), end of life (C), and benefits beyond system boundary (D).

---

## References

**[1]** Sameer, H., Weber, V., Mostert, C., Bringezu, S., Fehling, E., & Wetzel, A. (2019). *Environmental Assessment of Ultra-High-Performance Concrete Using Carbon, Material, and Water Footprint.* Materials, 12(6), 851. Open access. DOI: 10.3390/ma12060851. — UHPC-specific LCA reporting ingredient-level factors for cement, silica fume, quartz powder, fine aggregate, superplasticizer, and steel fiber.

**[2]** Randl, N., Steiner, T., Ofner, S., Baumgartner, E., & Mészöly, T. (2014). *Development of UHPC mixtures from an ecological point of view.* Construction and Building Materials, 67, 373–378. DOI: 10.1016/j.conbuildmat.2013.12.102.

**[3]** Habert, G., Miller, S.A., John, V.M., Provis, J.L., Favier, A., Horvath, A., & Scrivener, K.L. (2020). *Environmental impacts and decarbonization strategies in the cement and concrete industries.* Nature Reviews Earth & Environment, 1, 559–573. DOI: 10.1038/s43017-020-0093-3.

**[4]** Miller, S.A., Habert, G., Myers, R.J., & Harvey, J.T. (2021). *Achieving net zero greenhouse gas emissions in the cement industry via value chain mitigation strategies.* One Earth, 4(10), 1398–1411. DOI: 10.1016/j.oneear.2021.09.011.

**[5]** Purnell, P., & Black, L. (2012). *Embodied carbon dioxide in concrete: Variation with common mix design parameters.* Cement and Concrete Research, 42(6), 874–877. DOI: 10.1016/j.cemconres.2012.02.005.

**[6]** Scrivener, K.L., John, V.M., & Gartner, E.M. (2018). *Eco-efficient cements: Potential economically viable solutions for a low-CO2 cement-based materials industry.* Cement and Concrete Research, 114, 2–26. DOI: 10.1016/j.cemconres.2018.03.015.

**[7]** Huang, W., Kazemi-Kamyab, H., Sun, W., & Scrivener, K. (2017). *Effect of cement substitution by limestone on the hydration and microstructural development of ultra-high performance concrete (UHPC).* Cement and Concrete Composites, 77, 86–101. DOI: 10.1016/j.cemconcomp.2017.01.007.

**[8]** Carvalho, J.P.G., Lima, A.P., Resende, L.F.M., Silva, C.M.R., & Borges, P.H.R. (2022). *A comparative study of mechanical properties and life cycle assessment of high-strength concrete containing silica fume and nanosilica as a partial cement replacement.* Structures, 46, 838–851. DOI: 10.1016/j.istruc.2022.10.080.

**[9]** DCCEEW / MECLA (2024). *How to Calculate Embodied Carbon of a Concrete Mix.* Australian Government Department of Climate Change, Energy, the Environment and Water. Superplasticizer factor (2,200 kg CO2e/tonne = 2.2 kg CO2e/kg) based on AusLCI database and supplementary EPD review.

**[10]** MPA Cement / Concrete Centre (2019). *Embodied CO2e of UK cement, additions and cementitious material.* Fact Sheet 18, The Concrete Centre. Available at: https://www.concretecentre.com. Industry fact sheet; included for UK/EU slag and cement context.

**[11]** Asare, G.O., Ofori-Kuragu, J.K., & Kyiire, B. (2024). *Life cycle assessment of steel fibre-reinforced concrete beams.* Cogent Engineering, 11(1). Open access. Steel fiber factors drawn from manufacturer EPDs (Bekaert, Liberty Specialty Steel).

**[12]** worldsteel Association (2023). *Life Cycle Inventory Study for Steel Products.* worldsteel, Brussels. Industry-average LCI dataset for BF-BOF and EAF steel routes.

**[13]** Bekaert (2021). *Dramix® Steel Fibre Environmental Product Declaration.* Published via the EPD International registry. Product-level cradle-to-gate factors for drawn + cut steel fiber; referenced here as an industry benchmark.

---

## Citation for this Dataset

If citing this compiled factor set in a portfolio project or notebook:

> *Emission factors compiled from peer-reviewed open-access LCA literature (2012–2024), with primary UHPC-specific values from Sameer et al. (2019) and Randl et al. (2014). Cement and SCM ranges informed by Habert et al. (2020), Miller et al. (2021), Purnell & Black (2012), and Scrivener et al. (2018). Steel fiber values cross-checked against worldsteel LCI (2023) and the Bekaert Dramix EPD (2021). Used for demonstration purposes in a concrete carbon emissions prediction tool. Values are approximate and not intended for production, procurement, or regulatory use.*
