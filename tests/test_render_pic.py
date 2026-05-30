from typing import TYPE_CHECKING

import pytest
import nonebot

if TYPE_CHECKING:
    from nonebot_plugin_wakatime.schema import Stats as StatsType


def _empty_stats() -> "StatsType":
    nonebot.require("nonebot_plugin_wakatime")
    from nonebot_plugin_wakatime.schema import Stats

    return Stats(
        human_readable_total="0 secs",
        human_readable_total_including_other_language="0 secs",
        daily_average=0.0,
        daily_average_including_other_language=0.0,
        human_readable_daily_average="0 secs",
        human_readable_daily_average_including_other_language="0 secs",
        categories=None,
        projects=None,
        languages=None,
        editors=None,
        operating_systems=None,
        machines=None,
        user_id="48e5e537-efb7-4304-8562-132953542107",
        username="Komorebi",
        is_up_to_date=True,
    )


def _build_ai_coding_summary():
    nonebot.require("nonebot_plugin_wakatime")
    from nonebot_plugin_wakatime.utils import build_ai_coding_summary

    return build_ai_coding_summary


def _template_filters():
    nonebot.require("nonebot_plugin_wakatime")
    from nonebot_plugin_wakatime.filters import TEMPLATE_FILTERS

    return TEMPLATE_FILTERS


def test_build_ai_coding_summary_calculates_weekly_ai_coding_metrics(
    nonebug_init: None,
):
    build_ai_coding_summary = _build_ai_coding_summary()
    stats = _empty_stats()
    stats["ai_additions"] = 8430
    stats["ai_deletions"] = 717
    stats["human_additions"] = 395
    stats["human_deletions"] = 690
    stats["ai_input_tokens"] = 50131473
    stats["ai_output_tokens"] = 158151
    stats["ai_agent_breakdown"] = [
        {"name": "Claude", "lines": 9147, "cost": 152.708139},
        {"name": "Codex", "lines": 0, "cost": 0.025001},
    ]

    summary = build_ai_coding_summary(stats)

    assert summary is not None
    assert summary["ai_lines"] == 9147
    assert summary["human_lines"] == 1085
    assert summary["ai_percent"] == pytest.approx(89.39601250977326)
    assert summary["human_percent"] == pytest.approx(10.60398749022674)
    assert summary["dominant_label"] == "AI-driven"
    assert summary["dominant_percent"] == pytest.approx(89.39601250977326)
    assert summary["tokens_in"] == 50131473
    assert summary["tokens_out"] == 158151
    assert summary["total_tokens"] == 50289624
    assert summary["agents"] == [{"name": "Claude", "percent": 100.0, "lines": 9147}]


def test_build_ai_coding_summary_falls_back_to_agent_line_changes(nonebug_init: None):
    build_ai_coding_summary = _build_ai_coding_summary()
    stats = _empty_stats()
    stats["ai_additions"] = 1585
    stats["ai_deletions"] = 10
    stats["human_additions"] = 15
    stats["human_deletions"] = 7
    stats["ai_input_tokens"] = 23791542
    stats["ai_output_tokens"] = 69656
    stats["ai_agent_line_changes"] = {"Claude": 132, "Codex": 1463}

    summary = build_ai_coding_summary(stats)

    assert summary is not None
    assert summary["dominant_label"] == "AI-driven"
    assert summary["dominant_percent"] == pytest.approx(98.63945578231292)
    assert summary["agents"] == [
        {"name": "Codex", "percent": pytest.approx(91.72413793103448), "lines": 1463},
        {"name": "Claude", "percent": pytest.approx(8.275862068965518), "lines": 132},
    ]


def test_build_ai_coding_summary_uses_human_led_label_when_human_dominates(
    nonebug_init: None,
):
    build_ai_coding_summary = _build_ai_coding_summary()
    stats = _empty_stats()
    stats["ai_additions"] = 5
    stats["ai_deletions"] = 0
    stats["human_additions"] = 15
    stats["human_deletions"] = 0
    stats["ai_input_tokens"] = 1000
    stats["ai_output_tokens"] = 500

    summary = build_ai_coding_summary(stats)

    assert summary is not None
    assert summary["dominant_label"] == "Human-led"
    assert summary["dominant_percent"] == pytest.approx(75.0)


def test_build_ai_coding_summary_merges_extra_agents_into_other(nonebug_init: None):
    build_ai_coding_summary = _build_ai_coding_summary()
    stats = _empty_stats()
    stats["ai_additions"] = 60
    stats["ai_deletions"] = 0
    stats["human_additions"] = 40
    stats["human_deletions"] = 0
    stats["ai_agent_line_changes"] = {
        "Claude": 30,
        "Codex": 20,
        "Cursor": 10,
        "Other Agent": 5,
    }

    summary = build_ai_coding_summary(stats)

    assert summary is not None
    assert summary["agents"] == [
        {"name": "Claude", "percent": pytest.approx(46.15384615384615), "lines": 30},
        {"name": "Codex", "percent": pytest.approx(30.76923076923077), "lines": 20},
        {"name": "Other", "percent": pytest.approx(23.076923076923077), "lines": 15},
    ]


def test_build_ai_coding_summary_returns_none_without_ai_coding_data(
    nonebug_init: None,
):
    build_ai_coding_summary = _build_ai_coding_summary()
    empty_stats = _empty_stats()
    zero_stats = _empty_stats()
    zero_stats["ai_additions"] = 0
    zero_stats["ai_deletions"] = 0
    zero_stats["human_additions"] = 0
    zero_stats["human_deletions"] = 0
    zero_stats["ai_input_tokens"] = 0
    zero_stats["ai_output_tokens"] = 0
    zero_stats["ai_agent_line_changes"] = {}

    assert build_ai_coding_summary(empty_stats) is None
    assert build_ai_coding_summary(zero_stats) is None


def test_ai_coding_filters_format_template_values(nonebug_init: None):
    filters = _template_filters()

    assert filters["count"](9147) == "9,147"
    assert filters["compact_count"](50289624) == "50.3M"
    assert filters["percent"](89.39503518373729) == "89.4"
    assert filters["ring_dasharray"](89.39503518373729) == "67 100"
