import pandas as pd

from lazyframe import lf


def sample_data():
    return {
        "age": [20, 30, 40, 17],
        "country": ["BD", "US", "IN", "US"],
        "income": [1000, 2000, 3000, 100],
    }


def test_lazy_plan_builds_without_execution():
    df = lf.load(sample_data())
    plan_df = df.filter(df.age > 18).groupby("country").agg({"income": "mean"})

    assert plan_df._plan is not None
    assert plan_df._plan.operation == "agg"


def test_run_executes_pipeline_with_pandas():
    df = lf.load(sample_data())
    result = (
        df.filter(df.age > 18)
        .groupby("country")
        .agg({"income": "mean"})
        .sort("income", descending=True)
        .run(strategy="pandas")
    )

    assert isinstance(result, pd.DataFrame)
    assert list(result["country"]) == ["IN", "US", "BD"]
    assert list(result["income"]) == [3000.0, 2000.0, 1000.0]


def test_explain_contains_plan_and_backend_reasoning():
    df = lf.load(sample_data())
    plan_df = df.filter(df.age > 18).groupby("country").agg({"income": "mean"})

    explanation = plan_df.explain()

    assert "Execution Plan" in explanation
    assert "Filter" in explanation
    assert "GroupBy" in explanation
    assert "Aggregate" in explanation
    assert "Backend chosen" in explanation


def test_optimize_returns_suggestions():
    df = lf.load(sample_data())
    suggestions = df.filter(df.age > 18).optimize()

    assert isinstance(suggestions, list)
    assert len(suggestions) >= 1


def test_auto_selector_chooses_pandas_for_small_input():
    df = lf.load(sample_data())
    backend = df._executor.selector.select(df._source_data, df._plan, strategy="auto")
    assert backend.name == "pandas"
