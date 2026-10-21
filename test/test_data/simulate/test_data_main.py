# 出場チーム
TEAM_NAMES = (
    "Ａチーム",
    "Ｂチーム",
    "Ｃチーム",
    "Ｄチーム",
    "Ｅチーム",
    "Ｆチーム",
    "Ｇチーム",
    "Ｈチーム",
    "Ｉチーム",
    "Ｊチーム",
)

# レギュラー順位
REGULAR_ORDER_SEASON1 = TEAM_NAMES
REGULAR_ORDER_SEASON2 = (
    "Ｊチーム",
    "Ｉチーム",
    "Ｈチーム",
    "Ｇチーム",
    "Ｆチーム",
    "Ｅチーム",
    "Ｄチーム",
    "Ｃチーム",
    "Ｂチーム",
    "Ａチーム",
)

#セミファイナル順位
SEMIFINAL_ORDER_SEASON1 = (
    "Ｃチーム",
    "Ａチーム",
    "Ｆチーム",
    "Ｂチーム",
    "Ｄチーム",
    "Ｅチーム",
)
SEMIFINAL_ORDER_SEASON2 = (
    "Ｉチーム",
    "Ｇチーム",
    "Ｊチーム",
    "Ｈチーム",
    "Ｅチーム",
    "Ｆチーム",
)

# ファイナル順位
FINAL_ORDER_SEASON1 = (
    "Ｆチーム",
    "Ｃチーム",
    "Ａチーム",
    "Ｂチーム",
)
FINAL_ORDER_SEASON2 = (
    "Ｉチーム",
    "Ｇチーム",
    "Ｊチーム",
    "Ｈチーム",
)

# レギュラーのMリーグポイント
REGULAR_POINTS_SEASON1 = {
    team_name: float((len(TEAM_NAMES) - rank + 1) * 100)
    for rank, team_name in enumerate(REGULAR_ORDER_SEASON1, start=1)
}
REGULAR_POINTS_SEASON2 = {
    team_name: float((len(TEAM_NAMES) - rank + 1) * 80)
    for rank, team_name in enumerate(REGULAR_ORDER_SEASON2, start=1)
}

# セミファイナルのMリーグポイント
SEMIFINAL_POINTS_SEASON1 = {
    team_name: float((len(SEMIFINAL_ORDER_SEASON1) - rank + 1) * 50)
    for rank, team_name in enumerate(SEMIFINAL_ORDER_SEASON1, start=1)
}
SEMIFINAL_POINTS_SEASON2 = {
    team_name: float((len(SEMIFINAL_ORDER_SEASON2) - rank + 1) * 40)
    for rank, team_name in enumerate(SEMIFINAL_ORDER_SEASON2, start=1)
}

# ファイナルのMリーグポイント
FINAL_POINTS_SEASON1 = {
    team_name: float((len(FINAL_ORDER_SEASON1) - rank + 1) * 25)
    for rank, team_name in enumerate(FINAL_ORDER_SEASON1, start=1)
}
FINAL_POINTS_SEASON2 = {
    team_name: float((len(FINAL_ORDER_SEASON2) - rank + 1) * 20)
    for rank, team_name in enumerate(FINAL_ORDER_SEASON2, start=1)
}

# レギュラーの対戦スケジュール
REGULAR_SCHEDULE = [["Ａチーム", "Ｂチーム", "Ｃチーム", "Ｄチーム"]]
# セミの対戦スケジュールのデフォルト値
SEMIFINAL_PLACEHOLDER_SCHEDULE = [
    ["REGULAR_1", "REGULAR_2", "REGULAR_3", "REGULAR_4"],
    ["REGULAR_5", "REGULAR_6", "REGULAR_1", "REGULAR_2"],
]
