# Preserved Comparator-Configuration Attempt

This directory retains the first extended RTL run attempt and is intentionally not deleted. The Icarus RTL simulation itself reached `RTL_SSC_RESULT status=PASS` after the complete 128 affine campaign, prefix tie-break, exact collision rejection, and recovery test.

The runner exited non-zero because the independent Python comparator parsed a recovery trace that was labelled `case=affine trial=5` after the 128-trial campaign. The comparator correctly rejected that non-contiguous duplicate trial rather than silently ignoring it.

The bounded testbench was then corrected to label that extra diagnostic trace `case=recovery`, preserving the comparator's restriction to the intended `case=affine` trials `0..127`. The successful successor evidence is retained separately at [`../rtl-ssc/extended-128/`](../rtl-ssc/extended-128/); its two independent runs are byte-identical and its independent comparator passes.

This record is a harness-labelling correction, not a change to the RTL ordering module or a claim that the initially failed comparator was a passing validation result.
