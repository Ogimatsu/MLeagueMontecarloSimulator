from copy import deepcopy
from decimal import Decimal, ROUND_CEILING
from unittest.mock import patch

from common import const
from simulate.main import main
from test.test_data.simulate.test_data_main import (
    FINAL_ORDER_SEASON1,
    FINAL_ORDER_SEASON2,
    FINAL_POINTS_SEASON1,
    FINAL_POINTS_SEASON2,
    REGULAR_ORDER_SEASON1,
    REGULAR_ORDER_SEASON2,
    REGULAR_POINTS_SEASON1,
    REGULAR_POINTS_SEASON2,
    REGULAR_SCHEDULE,
    SEMIFINAL_ORDER_SEASON1,
    SEMIFINAL_ORDER_SEASON2,
    SEMIFINAL_POINTS_SEASON1,
    SEMIFINAL_POINTS_SEASON2,
    SEMIFINAL_PLACEHOLDER_SCHEDULE,
    TEAM_NAMES,
)

def make_phase_result(
    team_order,
    phase,
    points_by_team,
    previous_result=None,
):
    """固定したフェーズ順位・ポイントを持つ simulate_phase の戻り値を作る。"""
    previous_data = dict(previous_result or [])
    result = []

    for rank, team_name in enumerate(team_order, start=1):
        team_data = previous_data.get(
            team_name,
            {
                "weight": 1.0,
                "point": 0.0,
                "overall_rank": None,
                "regular_end_points": None,
                "regular_end_rank": None,
                "semifinal_start_points": None,
                "semifinal_end_points": None,
                "semifinal_end_rank": None,
                "final_start_points": None,
                "final_end_points": None,
                "final_end_rank": None,
            },
        ).copy()
        previous_phase = {
            const.SEMIFINAL_PHASE: const.REGULAR_PHASE,
            const.FINAL_PHASE: const.SEMIFINAL_PHASE,
        }.get(phase)
        if previous_phase is not None:
            # 前フェーズ終了時ポイントを持ち越し、小数第一位まで切り上げる。
            carry_over = (
                Decimal(str(team_data[f"{previous_phase}_end_points"]))
                * Decimal(str(const.CARRY_OVER_RATE))
            )
            team_data[f"{phase}_start_points"] = float(
                carry_over.quantize(Decimal("0.1"), rounding=ROUND_CEILING)
            )
        team_data["point"] = 0.0
        team_data[f"{phase}_end_points"] = points_by_team[team_name]
        team_data[f"{phase}_end_rank"] = rank
        result.append((team_name, team_data))

    return result

# レギュラーの結果
REGULAR_RESULT_SEASON1 = make_phase_result(
    REGULAR_ORDER_SEASON1,
    const.REGULAR_PHASE,
    REGULAR_POINTS_SEASON1
)
REGULAR_RESULT_SEASON2 = make_phase_result(
    REGULAR_ORDER_SEASON2,
    const.REGULAR_PHASE,
    REGULAR_POINTS_SEASON2
)

# セミの結果
SEMIFINAL_RESULT_SEASON1 = make_phase_result(
    SEMIFINAL_ORDER_SEASON1,
    const.SEMIFINAL_PHASE,
    SEMIFINAL_POINTS_SEASON1,
    previous_result=REGULAR_RESULT_SEASON1,
)
SEMIFINAL_RESULT_SEASON2 = make_phase_result(
    SEMIFINAL_ORDER_SEASON2,
    const.SEMIFINAL_PHASE,
    SEMIFINAL_POINTS_SEASON2,
    previous_result=REGULAR_RESULT_SEASON2,
)

# ファイナルの結果
FINAL_RESULT_SEASON1 = make_phase_result(
    FINAL_ORDER_SEASON1,
    const.FINAL_PHASE,
    FINAL_POINTS_SEASON1,
    previous_result=SEMIFINAL_RESULT_SEASON1,
)
FINAL_RESULT_SEASON2 = make_phase_result(
    FINAL_ORDER_SEASON2,
    const.FINAL_PHASE,
    FINAL_POINTS_SEASON2,
    previous_result=SEMIFINAL_RESULT_SEASON2,
)

# シーズン全体のチーム
EXPECTED_SEASON_TEAM_NAMES = set(TEAM_NAMES)


def test_main_multi_season():
    """複数シーズンの各フェーズ実行と、成績を含むリストの返却を確認する。"""
    phase_calls = []
    expected_seasons = [
        {
            "regular": REGULAR_RESULT_SEASON1,
            "semifinal": SEMIFINAL_RESULT_SEASON1,
            "final": FINAL_RESULT_SEASON1,
            "regular_order": REGULAR_ORDER_SEASON1,
            "semifinal_order": SEMIFINAL_ORDER_SEASON1,
        },
        {
            "regular": REGULAR_RESULT_SEASON2,
            "semifinal": SEMIFINAL_RESULT_SEASON2,
            "final": FINAL_RESULT_SEASON2,
            "regular_order": REGULAR_ORDER_SEASON2,
            "semifinal_order": SEMIFINAL_ORDER_SEASON2,
        },
    ]
    phase_results = iter(
        deepcopy(
            [
                phase_result
                for season in expected_seasons
                for phase_result in (
                    season["regular"],
                    season["semifinal"],
                    season["final"],
                )
            ]
        )
    )

    def fake_simulate_phase(teams, phase, schedule=None):
        # 後続処理で辞書が変更されても、呼び出し時点の値を確認できるようにする。
        phase_calls.append(deepcopy((teams, phase, schedule)))
        return next(phase_results)

    with (
        patch(
            "simulate.main.const.SEASON_COUNT",
            2,
        ),
        patch(
            "simulate.main.create_schedule",
            side_effect=deepcopy(
                [REGULAR_SCHEDULE, SEMIFINAL_PLACEHOLDER_SCHEDULE]
            )
        ) as mock_create_schedule,
        patch(
            "simulate.main.simulate_phase",
            side_effect=fake_simulate_phase,
        ) as mock_simulate_phase,
    ):
        test_result = main()
        # 2シーズン分の結果が、シーズン番号とチーム成績を持つこと
        assert isinstance(test_result, list)
        assert len(test_result) == len(expected_seasons) == 2
        assert mock_simulate_phase.call_count == len(phase_calls) == (
            len(expected_seasons) * 3
        )

        # 規定の引数でスケジュールを作成し、レギュラーを実行していること
        assert mock_create_schedule.call_count == 2
        regular_schedule_call, semifinal_schedule_call = mock_create_schedule.call_args_list
        assert regular_schedule_call.args[:2] == (
            const.REGULAR_GAMES_PER_TEAM, const.REGULAR_TEAM_COUNT
        )
        assert set(regular_schedule_call.args[2]) == EXPECTED_SEASON_TEAM_NAMES
        assert semifinal_schedule_call.args[:2] == (
            const.SEMIFINAL_GAMES_PER_TEAM, const.SEMIFINAL_TEAM_COUNT
        )
        assert semifinal_schedule_call.args[2] == [
            f"REGULAR_{rank}" for rank in range(1, const.SEMIFINAL_TEAM_COUNT + 1)
        ]

        for season_index, (season_result, expected) in enumerate(
            zip(test_result, expected_seasons, strict=True)
        ):
            assert set(season_result) == {"season", "teams"}
            assert season_result["season"] == season_index + 1
            team_results = season_result["teams"]
            assert isinstance(team_results, dict)
            assert set(team_results) == EXPECTED_SEASON_TEAM_NAMES

            call_start = season_index * 3
            regular_call, semifinal_call, final_call = (
                mock_simulate_phase.call_args_list[call_start:call_start + 3]
            )
            regular_phase_result = expected["regular"]
            semifinal_phase_result = expected["semifinal"]
            final_phase_result = expected["final"]
            regular_order = expected["regular_order"]
            semifinal_order = expected["semifinal_order"]
            expected_semifinalists = set(
                regular_order[:const.SEMIFINAL_TEAM_COUNT]
            )
            expected_finalists = set(
                semifinal_order[:const.FINAL_TEAM_COUNT]
            )
            expected_regular_eliminated = set(
                regular_order[const.SEMIFINAL_TEAM_COUNT:]
            )
            expected_semifinal_eliminated = set(
                semifinal_order[const.FINAL_TEAM_COUNT:]
            )

            assert set(regular_call.args[0]) == EXPECTED_SEASON_TEAM_NAMES
            assert regular_call.args[1] == const.REGULAR_PHASE
            assert regular_call.args[2] == REGULAR_SCHEDULE

            # レギュラー上位チームをセミファイナルへ渡していること
            semifinal_input, semifinal_phase, semifinal_schedule = phase_calls[
                call_start + 1
            ]
            assert set(semifinal_input) == expected_semifinalists
            assert semifinal_phase == const.SEMIFINAL_PHASE
            assert semifinal_call.args[1] == const.SEMIFINAL_PHASE

            # セミファイナルの仮チーム名が、シーズンごとの順位で置き換わること
            semifinal_mapping = {
                f"REGULAR_{rank}": team_name
                for rank, team_name in enumerate(regular_order, start=1)
            }
            expected_semifinal_schedule = [
                [semifinal_mapping[team] for team in card]
                for card in SEMIFINAL_PLACEHOLDER_SCHEDULE
            ]
            assert semifinal_schedule == expected_semifinal_schedule
            assert semifinal_call.args[2] == expected_semifinal_schedule

            # セミファイナル上位チームをファイナルへ渡していること
            final_input, final_phase, final_schedule = phase_calls[call_start + 2]
            assert set(final_input) == expected_finalists
            assert final_phase == const.FINAL_PHASE
            assert final_schedule is None
            assert final_call.args[1] == const.FINAL_PHASE
            assert len(final_call.args) == 2
            assert final_call.kwargs == {}

            # 次フェーズ開始時に前フェーズのポイントを引き継ぐこと
            expected_semifinal_by_team = dict(semifinal_phase_result)
            expected_final_by_team = dict(final_phase_result)
            for team_name, team_data in semifinal_input.items():
                assert team_data["regular_end_points"] == dict(
                    regular_phase_result
                )[team_name]["regular_end_points"]
                assert team_data["semifinal_start_points"] == (
                    expected_semifinal_by_team[team_name]["semifinal_start_points"]
                )
            for team_name, team_data in final_input.items():
                assert team_data["semifinal_end_points"] == (
                    expected_semifinal_by_team[team_name]["semifinal_end_points"]
                )
                assert team_data["final_start_points"] == (
                    expected_final_by_team[team_name]["final_start_points"]
                )

            # 敗退チームも含め、シーズン内の全チーム成績が返ること
            expected_results_by_rank = (
                (
                    expected_regular_eliminated,
                    dict(regular_phase_result),
                    "regular_end_rank",
                ),
                (
                    expected_semifinal_eliminated,
                    expected_semifinal_by_team,
                    "semifinal_end_rank",
                ),
                (
                    expected_finalists,
                    expected_final_by_team,
                    "final_end_rank",
                ),
            )
            for team_names, expected_result, rank_key in expected_results_by_rank:
                for team_name in team_names:
                    expected_team_data = {
                        key: value
                        for key, value in expected_result[team_name].items()
                        if key not in ("weight", "point")
                    }
                    expected_team_data["overall_rank"] = expected_team_data[rank_key]
                    assert team_results[team_name] == expected_team_data
                    assert "weight" not in team_results[team_name]
                    assert "point" not in team_results[team_name]
