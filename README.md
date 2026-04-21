# LazyFrame

LazyFrame is a smart lazy DataFrame execution engine with a unified API over multiple backends.

## Highlights

- Chainable DataFrame API (`filter`, `select`, `groupby`, `agg`, `sort`)
- Logical plan construction with lazy execution (`.run()` is the trigger)
- Auto backend selection (`pandas`, `polars`, `duckdb` placeholder)
- Simple optimizer with filter pushdown
- Explainability via `.explain()`
- Actionable hints via `.optimize()`

## Quick start

```python
from lazyframe import lf

df = lf.load({
    "age": [20, 30, 40],
    "country": ["BD", "US", "IN"],
    "income": [1000, 2000, 3000],
})

result = (
    df.filter(df.age > 18)
      .groupby("country")
      .agg({"income": "mean"})
      .sort("income", descending=True)
)

print(result.explain())
print(result.run())
```

## Install for development

```bash
pip install -e ".[dev]"
pytest
```

## Backend strategy

- `strategy="auto"` chooses backend by dataset size heuristic
- `strategy="pandas"` forces pandas
- `strategy="polars"` forces polars fallback backend
- `strategy="duckdb"` forces duckdb placeholder backend
