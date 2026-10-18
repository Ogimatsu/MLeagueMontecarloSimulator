# 想定するカラム名とその順序
EXPECTED_COLUMNS = [
    "season",
    "team",
    "overall_rank",
    "regular_end_rank",
    "regular_end_points",
    "semifinal_start_points",
    "semifinal_end_rank",
    "semifinal_end_points",
    "final_start_points",
    "final_end_rank",
    "final_end_points",
]


# シミュレーション結果
SIMULATE_RESULT = [
    {
        "season": 1,
        "teams": {
            # ファイナル進出
            "Ａチーム": {
                "overall_rank": 4,
                "regular_end_rank": 1,
                "regular_end_points": 883.8,
                "semifinal_start_points": 441.9,
                "semifinal_end_rank": 2,
                "semifinal_end_points": 377.2,
                "final_start_points": 188.6,
                "final_end_rank": 4,
                "final_end_points": 107.9,
            },
            # セミファイナル敗退
            "Ｂチーム": {
                "overall_rank": 6,
                "regular_end_rank": 5,
                "regular_end_points": 100.0,
                "semifinal_start_points": 50.0,
                "semifinal_end_rank": 6,
                "semifinal_end_points": -80.5,
                "final_start_points": None,
                "final_end_rank": None,
                "final_end_points": None,
            },
            # レギュラーシーズン敗退
            "Ｃチーム": {
                "overall_rank": 10,
                "regular_end_rank": 10,
                "regular_end_points": -500.3,
                "semifinal_start_points": None,
                "semifinal_end_rank": None,
                "semifinal_end_points": None,
                "final_start_points": None,
                "final_end_rank": None,
                "final_end_points": None,
            },
        },
    },
    {
        "season": 2,
        "teams": {
            # 同じチームの別シーズンの成績。0.0と空欄を区別する
            "Ａチーム": {
                "overall_rank": 4,
                "regular_end_rank": 6,
                "regular_end_points": 0.0,
                "semifinal_start_points": 0.0,
                "semifinal_end_rank": 3,
                "semifinal_end_points": -20.1,
                "final_start_points": -10.0,
                "final_end_rank": 4,
                "final_end_points": -100.5,
            },
        },
    },
]