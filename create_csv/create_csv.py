import csv
from time import perf_counter

def create_csv(simulate_result: list, output_path: str):
    """シミュレーション結果をCSVファイルに出力する"""
    start_time = perf_counter()

    columns = (
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
    )

    with open(
        output_path,
        mode="w",
        encoding="utf-8-sig",
        newline="",
    ) as file:
        writer = csv.DictWriter(file, fieldnames=columns)
        writer.writeheader()

        for season_result in simulate_result:
            for team_name, team_data in season_result["teams"].items():
                row = {
                    "season": season_result["season"],
                    "team": team_name,
                    **team_data
                }
                writer.writerow(row)

        print(f"CSV出力処理時間: {perf_counter() - start_time:.3f}秒")
