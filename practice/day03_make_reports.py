from pathlib import Path
from openpyxl import Workbook

Path("reports").mkdir(exist_ok=True)

def make_report(filename, title, blank_rows, start_col, rows):
    wb = Workbook()
    ws = wb.active
    ws.title = "보고서"
    ws.cell(row=1, column=1, value=title)
    ws.cell(row=2, column=1, value="작성일: 2026.10.31  /  [대외비]")

    r = 3 + blank_rows                       # 파일마다 표 시작 위치가 다름
    c = start_col
    ws.cell(row=r, column=c, value="부서")
    ws.cell(row=r, column=c + 1, value="한도")
    ws.cell(row=r, column=c + 2, value="익스포저")

    for desk, limit, exp in rows:
        r += 1
        ws.cell(row=r, column=c, value=desk)
        ws.cell(row=r, column=c + 1, value=limit)
        ws.cell(row=r, column=c + 2, value=exp)

    r += 2                                   # 합계 위에 빈 줄 하나
    ws.cell(row=r, column=c, value="합계")
    ws.merge_cells(start_row=r, start_column=c, end_row=r, end_column=c + 1)  # 병합 셀
    ws.cell(row=r, column=c + 2, value=sum(x[2] for x in rows))

    wb.save(f"reports/{filename}")
    print("created:", filename)

make_report("2026_08_market_risk.xlsx", "2026년 8월 시장리스크 현황", 1, 1,
            [("Equity", 100, 65), ("Bond", 200, 170), ("FX", 80, 60)])
make_report("2026_09_market_risk.xlsx", "2026년 9월 시장리스크 현황", 3, 2,
            [("Equity", 100, 80), ("Bond", 200, 185), ("FX", 80, 78), ("Credit", 150, 70)])
make_report("2026_10_market_risk.xlsx", "2026년 10월 시장리스크 현황", 5, 3,
            [("Equity", 100, 72), ("Bond", 200, 195), ("FX", 80, 85),
             ("Credit", 150, 90), ("Derivatives", 120, 110)])