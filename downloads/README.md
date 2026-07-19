# downloads/ (runtime output)

PhaseScout writes CIF batches and indexes here (for example `01_my_alloy/`).

This directory is **gitignored** except this README and `.gitkeep`.  
Your local phase libraries stay on disk but are not published to GitHub.

Suggested layout after a CLI run:

```text
downloads/
  01_Ti6Al4V/
    phase_index.csv
    query_summary.txt
    run_manifest.json
    mp-xxxx_Formula_sgN_Symbol_ehull…[_stable].cif
```

CIF naming (scheme B, mp-id first):

```text
mp-134_Al_sg225_Fm-3m_ehull0_stable.cif
mp-1183144_Al_sg194_P6_3_mmc_ehull0p010.cif
```

Existing older files may still be `mp-xxxx_Formula.cif`; they are not auto-renamed.
