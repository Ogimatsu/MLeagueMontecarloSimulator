# Mリーグモンテカルロシミュレーションツール

本ツールは、Mリーグの現行レギュレーションをモデル化し、
仮想的なリーグ戦を多数回実行するためのツールです。
レギュラーシーズン順位と最終順位の関係を分析したり、
アドバンテージやチームの強さ等を調整したりしてシミュレーションすることで、
どのように結果が変わるかを検証するのに使用します。

---

## 使用技術

- Python 3.13.2

---

## 使い方

[セットアップ](#セットアップ手順ローカル開発環境)後、仮想環境を有効にしてプロジェクトのルートディレクトリで実行します。

```powershell
python -m simulate.main
```

指定シーズン数のシミュレーション結果が、`output`フォルダ内に`mleague_simulate_result_<日時>.csv`という名前で保存されます。
文字コードはUTF-8（BOM付き）で、未進出フェーズの値は空欄になります。

データ分析は、`analyze\analyze.ipynb`を実行して行うことができます。
`output`フォルダ内に複数のCSVファイルがある場合は、更新日時が最新のCSVファイルに対して分析を行います。

---

## ディレクトリ構成（抜粋）

```
MLeagueMontecarloSimulator/
├── analyze/                      # シミュレーション結果の分析
│   └── analyze.ipynb             # 集計・可視化用のNotebook
├── common/                       # 共通処理
│   └── const.py                  # 定数
├── create_csv/                   # CSV出力処理
│   ├── __init__.py
│   └── create_csv.py             # シミュレーション結果のCSV出力
├── docs/
│   └── specification.md          # 仕様書
├── output/                       # 作成したCSVファイルの出力場所
├── simulate/                     # シミュレーション本体
│   ├── __init__.py
│   ├── game.py                   # 1半荘の処理
│   ├── main.py                   # シーズンシミュレーション
│   ├── schedule.py               # 対戦スケジュールの作成
│   └── simulate_phase.py         # フェーズのシミュレーション
├── test/                         # テストコード
│   ├── create_csv/
│   │   ├── __init__.py
│   │   └── test_create_csv.py
│   ├── simulate/
│   │   ├── __init__.py
│   │   ├── test_game.py
│   │   ├── test_main.py
│   │   ├── test_schedule.py
│   │   └── test_simulate_phase.py
│   ├── test_data/                # テスト用データ
│   │   ├── create_csv/
│   │   │   └── test_data_create_csv.py
│   │   └── simulate/
│   │       └── test_data_main.py
│   └── __init__.py
├── .gitignore                    # Gitの管理対象外ファイル設定
├── .pre-commit-config.yaml       # コミット前の自動チェック設定
├── AGENTS.md                     # AIへの作業指示
└── README.md                     # プロジェクトの説明
```

---

## セットアップ手順（ローカル開発環境）

「使用技術」に記載したバージョンのPythonとGitを用意してください。以下はWindows PowerShellでの手順です。
シミュレーション本体はPython標準ライブラリのみを使用し、開発時にはpytestとpre-commitを追加します。

### リポジトリと仮想環境の準備

```powershell
git clone https://github.com/Ogimatsu/MLeagueMontecarloSimulator.git
cd MLeagueMontecarloSimulator
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

以降のコマンドは、仮想環境を有効にしてプロジェクトのルートディレクトリで実行します。
既にクローン済みの場合は、クローンを省略してください。

macOS/Linuxでは、仮想環境の有効化に次のコマンドを使用します。

```bash
source .venv/bin/activate
```

### 開発用ツールの導入

```powershell
python -m pip install pytest pre-commit
pre-commit install
```

pre-commitのpytestフックは`.venv/Scripts/python.exe`を使用するWindows向けの設定です。
macOS/Linuxでは、その実行パスを環境に合わせて変更する必要があります。

---

## 開発者向け情報

### 仕様と設定

- 計算ルール・用語・結果形式は[仕様書](docs/specification.md)を参照してください。
- シミュレーションの定数は`common/const.py`にあります。
- 実行シーズン数は`SEASON_COUNT`（現在は10,000）で指定します。

### テスト

全テストを実行します。

```powershell
python -m pytest test
```

対象のファイルを指定して実行することもできます。`-s`を付けると、テスト中の標準出力を表示します。

```powershell
python -m pytest -s test/simulate/test_main.py
```

### コミット前のチェック

[.pre-commit-config.yaml](.pre-commit-config.yaml)には、isort（Black互換設定）、Black、pytest、末尾空白・ファイル末尾改行・YAML構文・マージ競合のチェックを設定しています。
`pre-commit install`後はコミット時に自動実行されます。全ファイルを手動でチェックする場合は、次を実行します。

```powershell
pre-commit run --all-files
```

isort、Black、空白・改行のフックは対象ファイルを自動修正する場合があります。

---

## Git 運用方針

- main: 本番用、常にデプロイ可能な状態
- feature/〇〇: 機能ごとの開発ブランチ（例：feature/search-function）
- コミットメッセージはプレフィックス付きで明確に（例：fix:, feat:）
