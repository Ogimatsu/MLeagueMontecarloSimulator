import csv

from create_csv.create_csv import create_csv
from test.test_data.create_csv.test_data_create_csv import (
    EXPECTED_COLUMNS,
    SIMULATE_RESULT,
)

def test_create_csv(tmp_path):
    """CSVファイルが正しく出力されるかを確認する"""
    output_path = tmp_path / "test_result.csv"

    # CSV出力データの期待値作成
    asserted_csv = []
    for season_result in SIMULATE_RESULT:
        for team_name, team_data in season_result["teams"].items():
            asserted_row = {
                "season": str(season_result["season"]),
                "team": team_name,
                **{
                    key: "" if value is None else str(value)
                    for key, value in team_data.items()
                },
            }
            asserted_csv.append(asserted_row)

    create_csv(SIMULATE_RESULT, output_path)

    with open(
        output_path,
        mode="r",
        encoding="utf-8-sig",
        newline=""
    ) as file:
        reader = csv.DictReader(file)
        columns = reader.fieldnames
        records = list(reader)
        # ヘッダーの出力項目名、出力順が想定通りか
        assert columns == EXPECTED_COLUMNS
        # 出力件数が想定通りか（ヘッダー除く）
        assert len(records) == 4
        # 出力内容が想定通りか
        assert records == asserted_csv
