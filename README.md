# LVBench relabelled answer keys

Corrected multiple-choice answer keys for [LVBench](https://github.com/zai-org/LVBench),
a long-video understanding benchmark. Every question in the corpus was independently
re-annotated; this repository publishes the resulting keys alongside the originals so the
two can be compared directly.

This repository contains **annotations only**. No video is redistributed here. See
[Getting the videos](#getting-the-videos).

## What is here

| file | rows | contents |
| --- | ---: | --- |
| `lvbench_relabelled.parquet` | 1,530 | the corrected questions and answer keys |
| `lvbench_relabelled_original.parquet` | 1,530 | the same questions with the published LVBench keys, row-aligned |
| `excluded.csv` | 19 | question ids not present in either file |

The two parquets are row-aligned on `uid`, so a before/after comparison is a column
comparison. Against the published keys:

| change | items | share |
| --- | ---: | ---: |
| correct answer repaired | 313 | 20.5% |
| question stem reworded | 137 | 9.0% |
| distractors changed | 356 | 23.3% |
| any of the three | 466 | 30.5% |

A **repair** means the text of the correct option changed. Compare option *text*, not the
`answer` letter: the annotators both reordered and rewrote option lists, so the letter moves
without the answer changing and the answer changes without the letter moving. The letter
differs on only 232 rows, which both understates and mismeasures the correction. Case,
punctuation and whitespace are normalised before comparison, so a typography fix is not a
repair, and reordering alone is not a repair.

Of the 313 repairs, 94 promote text that was already one of the published options and 219
use text the annotators rewrote.

`verify_counts.py` reproduces every number above from the two parquets:

```
python verify_counts.py lvbench_relabelled.parquet lvbench_relabelled_original.parquet
```

19 of LVBench's 1,549 questions were removed by the annotators as unrepairable and appear
in neither parquet. Their ids are listed in `excluded.csv`.

## Schema

`lvbench_relabelled.parquet`:

| column | description |
| --- | --- |
| `uid` | LVBench question id, the join key to the original dataset |
| `key` | YouTube video id |
| `type` | video genre (`selfmedia`, `cartoon`, `live`, `tv`, `sport`, `documentary`) |
| `video_info` | duration, fps and resolution of the source video |
| `question` | question stem followed by four options, in LVBench's packed `(A) …` format |
| `answer` | correct option letter, `A` to `D` |
| `question_type` | capability tags, e.g. `['reasoning']`, `['entity recognition']` |
| `time_reference` | evidence window in the source video |
| `source` | release identifier of the annotation pass |
| `repair_decision` | `repair` if the correct option's text changed, `keep` otherwise |
| `n_options` | option count; 4 on every row |

`lvbench_relabelled_original.parquet` has the first eight of these columns, with
`question` and `answer` exactly as published by LVBench.

Every question has exactly four options. `repair_decision` is derived from the two parquets
by the rule above and agrees with them on every row, so it is a sound filter for the repaired
items. It replaces the annotators' own classification, which disagreed with the data on 116
rows.

## Getting the videos

Videos and the original annotations come from
[`lmms-lab/LVBench`](https://huggingface.co/datasets/lmms-lab/LVBench), with the videos
under `video_chunks/`. The upstream project is
[zai-org/LVBench](https://github.com/zai-org/LVBench).

Join on `uid` to align these keys with the videos.

## Licence

Released under [CC BY-NC-SA 4.0](LICENSE), matching LVBench, whose ShareAlike term
requires derivatives to carry the same licence.

LVBench additionally states: *"LVBench is only used for academic research. Commercial use
in any form is prohibited."* That restriction applies to this derivative too.

Neither LVBench nor this repository holds copyright in the source videos, which remain
the property of their respective owners.

## Citation

These keys were produced for, and are described in:

```bibtex
@inproceedings{dyanatkar2026multiplechoice,
  title     = {What Does Multiple Choice Actually Measure? Disentangling Video
               Understanding from Option-Exploitation},
  author    = {Dyanatkar, Sepand and Piercy, Elliott and Chan, Justin},
  booktitle = {NeurIPS 2026 Workshop: Can We Trust AI Evaluation? Robustness,
               Causality, and Risk in Modern AI Assessment},
  year      = {2026},
  url       = {https://openreview.net/forum?id=qshO3h92ds}
}
```

OpenReview: <https://openreview.net/forum?id=qshO3h92ds>
NeurIPS: <https://neurips.cc/virtual/2026/loc/sydney/178197>
