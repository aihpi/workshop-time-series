# Helper modules

The course keeps almost all of its code in the notebooks, where it can be read alongside the explanation.
These few modules exist because the code in them is either noise in a teaching notebook or needed by
several of them at once.

## `notebooks.nb_config`

Every dataset path the notebooks use, derived from the repository root so that a notebook works wherever
the repository is cloned. Notebooks import this rather than writing paths of their own.

```{eval-rst}
.. automodule:: nb_config
   :members:
   :undoc-members:
```

## `notebooks.reference_scores`

Results carried from one notebook into another's comparison table, with the provenance needed to check
them. See [Maintaining the notebooks](maintenance.md#figures-carried-between-notebooks).

```{eval-rst}
.. automodule:: reference_scores
   :members:
   :undoc-members:
   :member-order: bysource
```

## `src.plotting`

Plotting helpers too long to sit inline in the notebook that uses them.

```{eval-rst}
.. automodule:: src.plotting
   :members:
   :undoc-members:
```

## `src.utils`

```{eval-rst}
.. automodule:: src.utils
   :members:
   :undoc-members:
```
