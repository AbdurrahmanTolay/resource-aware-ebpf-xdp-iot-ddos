# Analysis

`statistical_analysis.py` contains run-level helpers used for replication and consistency checks.

The helpers deliberately enforce the manuscript's analysis boundary:

- paired service comparisons use matched `pair_id` values;
- bootstrap intervals are calculated over independent run-level values;
- nested timing events are reduced to one median per independent run before inference.

The script is not a substitute for missing historical raw data. Only apply an inferential method when the experimental unit and source records support it.
