## Frontend Language as Control Constraint

Frontend copy intentionally avoids action-oriented language.

Implications:
- "Submit for Evaluation" means no execution occurs at submission.
- "Evaluation in Progress" implies analysis only.
- "Decision Complete" implies terminal state.

The control layer must respect these semantic constraints.
Any execution beyond evaluation requires an explicit future phase.

This prevents future confusion or scope creep.
