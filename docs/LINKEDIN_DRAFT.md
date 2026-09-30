# LinkedIn draft (public-safe) - skill-range first-screen restyle 2026-09-30

Field pain first. Homayoun posts himself.
Paste verified 2026-09-30 on katas/K01-loop-contract/fixtures/fail: missing headings, exit 2.

---

Paste block (copy from the next line to the URL):

A skills list is easy to copy. Graded proof is not.

ai-eng-skill-range is 56 skills mapped to 24 katas with frozen graders that return 0 or 2.

The stranger run is the incomplete Loop Contract:

git clone https://github.com/homayoun-safarpour/ai-eng-skill-range
cd ai-eng-skill-range && pip install -e .
skillrange grade K01 --submission katas/K01-loop-contract/fixtures/fail

FAIL: missing headings:
  - ## 2. Verifier
  - ## 3. Stop layers
  - ## 4. State file
  - ## 5. Irreversible

Exit 2. The pass fixture on the same kata exits 0.

The limit: offline katas, not a 500-lesson curriculum and not an agent runtime.

Repo:
https://github.com/homayoun-safarpour/ai-eng-skill-range
