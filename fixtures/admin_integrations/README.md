# Synthetic integration fixtures

Everything in this directory is invented. No provider resources are created by opening or copying these files. `project.json` supplies the ground truth and construction recipe; it is not a Google/Canva import payload or a native spreadsheet/presentation file.

Later, after scoped fixture-creation consent, use copies in one private test folder:
- A native Google Doc with Overview and Decisions tabs, the cost table, an unresolved due-date suggestion and one review comment.
- A native Sheet with Costs and hidden Controls tabs, entered formulas, effective totals/error and one chart. Preserve formulas, not just CSV values.
- A native Slides deck with three slides and speaker notes; recreate the labeled process using native shapes/lines. An SVG inserted as one image is a different fixture and does not test native element connectivity.
- A Canva presentation with matching wording and notes, and a separate native shape/arrow diagram. Do not assume Canva Sheet cells are available.
- An approved synthetic meeting artifact or uploaded test transcript. No real meeting/recording or invitation is necessary for offline preparation.

Read acceptance: owner Alex, reviewer Sam, status review, accepted due date 23 October (26 October is only proposed), total 660, approval pending, and no agreed meeting time. Diagram edges and transcript timestamps must be traceable. Missing artifacts, inaccessible resources or unsupported structures are explicit outcomes.

Creating/uploading provider copies, suggestions/comments or meetings requires separate scope authorization. Keep their real resource IDs and per-test results in private workspace storage, outside this repository.
