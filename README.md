# PoMMES
This repository contains the source code for the paper [PoMMES: Prevention of Micro-architectural Leakages in Masked Embedded Software](https://eprint.iacr.org/2024/574/).

# Documentation
All information regarding installation, requirements and user guide are found in the [Wiki](https://github.com/ChairImpSec/PoMMES/wiki)

# Changes / Contributions
This fork contains the following fixes and additions contributed as part of the ongoing PoMMES effort:
- Fixed crash on unregistered internal function calls (e.g. `getRandomness`) that aborted parsing.
- Propagated condition sensitivity into generated conditional branches so secret-dependent control flow is flagged.
- Restored macOS/Linux build portability (OpenMP flag, standard includes, Boost paths, date handling).
- Added control-flow-graph and basic-block sensitivity plot generation (matplotlib).
- Fixed case-study input path for the `square_share` example.

# Contact and Support
Please contact [Jannik Zeitschner](mailto:jannik.zeitschner@rub.de) if you have any questions, comments, or if you found a bug that should be fixed.

# Publication
[J. Zeitschner](https://github.com/JannikZeitschner), [A.Moradi](https://github.com/amircrypto001) (2024): [PoMMES: Prevention of Micro-architectural Leakages in Masked Embedded Software](https://eprint.iacr.org/2024/574/)
