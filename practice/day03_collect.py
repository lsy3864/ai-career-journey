from pathlib import Path
import pandas as pd

def find_value(path, label):
    grid = pd.read_excel(path, header=None)

    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            cell = grid.iat[r, c]
            if isinstance(cell, str) and cell.strip() == label:
                right_side = grid.iloc[r, c + 1:].dropna()
                return right_side.iloc[0]

    raise ValueError(f" '{label}'을(를) {path.name}에서 찾지 못했습니다.")


def read_table(path, header_label):
    grid = pd.read_excel(path, header=None)

    for r in range(grid.shape[0]):
        row_values = grid.iloc[r].astype(str).str.strip().tolist()
        if header_label in row_values:
            table = pd.read_excel(path, header=r)
            table = table.dropna(axis = 1, how = "all")
            table = table.dropna(subset = [header_label])
            table = table[table[header_label] != "합계"]
            return table

    raise ValueError(f" '{header_label}'을(를) {path.name}에서 찾지 못했습니다.")

# ---- 1. 각 보고서의 합계 값 취합 ----
summary = []
for f in sorted(Path("reports").glob("*.xlsx")):
    total = find_value(f, "합계")
    summary.append({"file": f.name, "total_exposure": total})

summary_df = pd.DataFrame(summary)
print("Step1: 월별 합계 ----------")
print(summary_df)

# ---- 2. 각 보고서의 부서별 표를 하나로 합치기 ----
tables = []
for f in sorted(Path("reports").glob("*.xlsx")):
    t = read_table(f, "부서")
    t["file"] = f.name
    tables.append(t)

detail_df = pd.concat(tables, ignore_index=True)
detail_df["usage"] = detail_df["익스포저"] / detail_df["한도"]
print("\nStep2: 부서별 상세 ----------")
print(detail_df)

# ---- 3. 엑셀 파일 하나에 시트 두 개로 저장 ----
with pd.ExcelWriter("practice/monthly_summary.xlsx") as writer:
    summary_df.to_excel(writer, sheet_name="월별합계", index=False)
    detail_df.to_excel(writer, sheet_name="부서별상세", index=False)

print("\nSaved: practice/monthly_summary.xlsx")