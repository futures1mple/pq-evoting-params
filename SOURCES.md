# Source documents

Parameters were read from the documents below. Where the PDF was retained, its
SHA-256 is given so that page references in `params.py` can be checked against
the same version. For two publisher PDFs (Hough et al.; Farzaliyev et al. 2025)
only the DOI is recorded; the versions used were the published versions of record
as downloaded in October 2026.

| Scheme | Document used for parameters | SHA-256 |
|---|---|---|
| EVOLVE | Cryptology ePrint Archive 2017/1235 (PDF) | bc4585c0392e0289470a5c081a73671ae9acc3ea1bf44c5344dbd4bbb3dd9bbf |
| EVOLVED | ePrint 2022/1686 (PDF) | 4b1ea7a172974479739e39816357ff0aa40cc464947c119bf9b483d090ea5997 |
| Epoque | ePrint 2021/304 (PDF) | 8a638b43c72e544d3097709b87a0768016e5087c378617efa6c3b47eb4655b4a |
| Boyen, Haines, Müller 2020 | ePrint 2020/115 (PDF) | d3416ad458370da1add70a36cae315df36a77e8c080cf831fc62f722b77adb60 |
| Aranha et al. 2021 | ePrint 2021/338 (PDF) | 0bd07a0f20cba0868d0125d610083e8c33445a3374b40e4f6b52a05411448c51 |
| Farzaliyev, Willemson, Kaasik 2021 | ePrint 2021/1499 (PDF) | 6a60fe09266c1a53ac440f52fb555235ffbc5f0c97b440100943ed0c53954415 |
| Herranz, Martínez, Sánchez 2021 | ePrint 2021/488 (PDF) | b5d6c7ba63fa75279d08f698f3c2e94fca3030a646100b1097817fedc3f2f38a |
| Aranha et al. 2023 | ePrint 2022/422, full version of the CCS 2023 paper (PDF, 28 pp.) | fa7b086e4c10e3c13b6de0bf71f7586ebdf3ed6ddf4c85be776544df10a57cb8 |
| Hough, Sandsbråten, Silde 2025 | IACR Communications in Cryptology 1(4), DOI 10.62056/a69qudhdj (publisher PDF) | not retained |
| Bootle, Lyubashevsky, Merino-Gallardo 2025 | ePrint 2025/658 (PDF) | 237b8dc9d058b6b0816923fb143f3fb7df408ba0d1d71d9141bdc3ed21d6045d |
| de Perthuis, Peters 2024 | ePrint 2024/2087 (PDF) | b9d82fddbade0b18d53ccce431813e57ecddcdbfe8458f92128cc779017de9d8 |
| Abdolmaleki et al. 2026 | ePrint 2026/1540 (PDF) | f0cd71c04cdc4c4175cf11fb712ee94e7cc2e618d00b01c0f96a41e177db71e3 |
| Farzaliyev, Pärn, Saarse, Willemson 2025 | Journal of Cryptology 38(1), art. 6, DOI 10.1007/s00145-024-09530-5 (open-access PDF) | not retained |
| PQKryvos | PoPETs 2026(4), DOI 10.56553/popets-2026-0164 (publisher PDF); ePrint 2026/1004 has the same parameters | ePrint PDF: d123e70be9a150c005a3e8330c229f66efe762aa80d24214f2d80049b1494b63 |

Excluded candidates (no concrete parameter set with a stated level): Costa–Martínez–Morillo ePrint
2017/900 (b1e9903fcd3178a986abdb58e9b4f2cc02d914801410eafbed4ff3a8df44738c) and 2019/357 (619d8b4593adb225ce0608a0da0ec4d4c4adca4a38cd9877f2fcd4efbf5a6a5e), Strand
2018/027 (2a483bf91bd578948abd78bd32dd140d35c84a067e051a8e70b248778acf672f), Gjøsteen–Strand 2017/166 (f6e9d2a18590a742903003c59af14b65b10c43bf94940720c996c536ff7020ca),
Goldhahn–Gjøsteen 2024/1513 (2adbe0b170800fe95d4bed8e61b5f3a31fad8949a829b09937518b1eed63e741), Abapour et al. 2025/1725 (e55825e57d2f30ffd3c6c627efa4243a0a8ecab9bf3367560d4fcc06d1e983a6).

Software: lattice-estimator commit 53da5982597709ba0fdf94ea37a84d822310fd84
(19 Aug 2026); cross-check at commit 352ddaf4a288a0543f5d9eb588d2f89c7acec463;
passagemath 10.8.12; Python 3.13.16; see `requirements.txt`.
