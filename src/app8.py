import argparse
import os
import zipfile
from html import escape
from pathlib import Path

from dotenv import load_dotenv

from csv_file import CSVFile


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"


def get_dataset_path(dataset_path_text: str) -> Path:
    dataset_path = Path(dataset_path_text)

    if dataset_path.suffix.lower() != ".csv":
        raise ValueError("Dataset file must have a .csv extension.")

    if dataset_path.is_file():
        return dataset_path

    fallback_path = DATA_DIR / dataset_path
    if fallback_path.is_file():
        return fallback_path

    raise FileNotFoundError(
        f"Dataset file '{dataset_path_text}' does not exist."
    )


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Analyze the AI student impact dataset and optionally generate "
            "an Excel report."
        )
    )
    parser.add_argument(
        "dataset",
        help=(
            "Path to the local CSV dataset file, "
            "for example ai_student_inpact.csv."
        ),
    )
    parser.add_argument(
        "-o",
        "--output",
        help="Path to the .xlsx report file to create.",
    )
    return parser.parse_args()


def get_setting(name: str, default: str) -> str:
    return os.getenv(name, default).strip()


def validate_column(column_name: str, column_names: list[str]) -> None:
    if column_name not in column_names:
        raise ValueError(
            f"Column '{column_name}' does not exist in the dataset."
        )


def numeric_values(data: CSVFile, column_name: str) -> list[float]:
    column_index = data.get_column_index(column_name)
    values: list[float] = []

    for row in data.get_rows()[1:]:
        value = row[column_index].strip()
        if value:
            values.append(float(value))

    return values


def average(values: list[float]) -> float:
    return sum(values) / len(values)


def median(values: list[float]) -> float:
    sorted_values = sorted(values)
    middle = len(sorted_values) // 2

    if len(sorted_values) % 2 == 1:
        return sorted_values[middle]

    return (sorted_values[middle - 1] + sorted_values[middle]) / 2


def count_matching_rows(
    data: CSVFile,
    column_name: str,
    expected_value: str,
) -> int:
    column_index = data.get_column_index(column_name)
    return sum(
        1
        for row in data.get_rows()[1:]
        if row[column_index] == expected_value
    )


def column_letter(column_number: int) -> str:
    letters = ""
    while column_number:
        column_number, remainder = divmod(column_number - 1, 26)
        letters = chr(65 + remainder) + letters
    return letters


def cell_xml(
    row_number: int,
    column_number: int,
    value: object,
    style: int = 0,
) -> str:
    reference = f"{column_letter(column_number)}{row_number}"
    style_attr = f' s="{style}"' if style else ""
    text = escape(str(value))
    return (
        f'<c r="{reference}" t="inlineStr"{style_attr}>'
        f"<is><t>{text}</t></is></c>"
    )


def row_xml(row_number: int, values: list[object], style: int = 0) -> str:
    cells = [
        cell_xml(row_number, column_number, value, style)
        for column_number, value in enumerate(values, start=1)
    ]
    return f'<row r="{row_number}">{"".join(cells)}</row>'


def create_excel_report(
    output_path: Path,
    summary_rows: list[list[object]],
    statistics_rows: list[list[object]],
    aggregation_rows: list[list[object]],
) -> None:
    rows: list[str] = []
    row_number = 1

    rows.append(row_xml(row_number, ["AI Student Impact Report"], style=1))
    row_number += 2

    for title, section_rows in [
        ("Summary", summary_rows),
        ("Statistics", statistics_rows),
        ("Aggregation", aggregation_rows),
    ]:
        rows.append(row_xml(row_number, [title], style=2))
        row_number += 1
        for index, values in enumerate(section_rows):
            style = 2 if index == 0 else 0
            rows.append(row_xml(row_number, values, style=style))
            row_number += 1
        row_number += 1

    spreadsheet_ns = (
        "http://schemas.openxmlformats.org/spreadsheetml/2006/main"
    )
    document_rels_ns = (
        "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
    )
    package_rels_ns = (
        "http://schemas.openxmlformats.org/package/2006/relationships"
    )
    content_types_ns = (
        "http://schemas.openxmlformats.org/package/2006/content-types"
    )
    sheet_content_type = (
        "application/vnd.openxmlformats-officedocument."
        "spreadsheetml.worksheet+xml"
    )
    workbook_content_type = (
        "application/vnd.openxmlformats-officedocument."
        "spreadsheetml.sheet.main+xml"
    )
    styles_content_type = (
        "application/vnd.openxmlformats-officedocument."
        "spreadsheetml.styles+xml"
    )
    rels_content_type = (
        "application/vnd.openxmlformats-package.relationships+xml"
    )

    sheet_xml = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        f'<worksheet xmlns="{spreadsheet_ns}">'
        "<cols>"
        '<col min="1" max="1" width="32" customWidth="1"/>'
        '<col min="2" max="4" width="24" customWidth="1"/>'
        "</cols>"
        f"<sheetData>{''.join(rows)}</sheetData>"
        "</worksheet>"
    )

    workbook_xml = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        f'<workbook xmlns="{spreadsheet_ns}" xmlns:r="{document_rels_ns}">'
        "<sheets>"
        '<sheet name="Report" sheetId="1" r:id="rId1"/>'
        "</sheets>"
        "</workbook>"
    )

    worksheet_rel = f"{document_rels_ns}/worksheet"
    styles_rel = f"{document_rels_ns}/styles"
    office_document_rel = f"{document_rels_ns}/officeDocument"

    workbook_rels_xml = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        f'<Relationships xmlns="{package_rels_ns}">'
        f'<Relationship Id="rId1" Type="{worksheet_rel}" '
        'Target="worksheets/sheet1.xml"/>'
        f'<Relationship Id="rId2" Type="{styles_rel}" '
        'Target="styles.xml"/>'
        "</Relationships>"
    )

    root_rels_xml = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        f'<Relationships xmlns="{package_rels_ns}">'
        f'<Relationship Id="rId1" Type="{office_document_rel}" '
        'Target="xl/workbook.xml"/>'
        "</Relationships>"
    )

    styles_xml = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        f'<styleSheet xmlns="{spreadsheet_ns}">'
        '<fonts count="3">'
        '<font><sz val="11"/><name val="Calibri"/></font>'
        '<font><b/><color rgb="FF1F4E78"/><sz val="14"/>'
        '<name val="Calibri"/></font>'
        '<font><b/><color rgb="FFFFFFFF"/><sz val="11"/>'
        '<name val="Calibri"/></font>'
        "</fonts>"
        '<fills count="3">'
        '<fill><patternFill patternType="none"/></fill>'
        '<fill><patternFill patternType="gray125"/></fill>'
        '<fill><patternFill patternType="solid">'
        '<fgColor rgb="FF4472C4"/><bgColor indexed="64"/>'
        "</patternFill></fill>"
        "</fills>"
        '<borders count="1"><border><left/><right/><top/>'
        "<bottom/><diagonal/></border></borders>"
        '<cellStyleXfs count="1">'
        '<xf numFmtId="0" fontId="0" fillId="0" borderId="0"/>'
        "</cellStyleXfs>"
        '<cellXfs count="3">'
        '<xf numFmtId="0" fontId="0" fillId="0" borderId="0" '
        'xfId="0"/>'
        '<xf numFmtId="0" fontId="1" fillId="0" borderId="0" '
        'xfId="0" applyFont="1"/>'
        '<xf numFmtId="0" fontId="2" fillId="2" borderId="0" '
        'xfId="0" applyFont="1" applyFill="1"/>'
        "</cellXfs>"
        "</styleSheet>"
    )

    content_types_xml = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        f'<Types xmlns="{content_types_ns}">'
        f'<Default Extension="rels" ContentType="{rels_content_type}"/>'
        '<Default Extension="xml" ContentType="application/xml"/>'
        '<Override PartName="/xl/workbook.xml" '
        f'ContentType="{workbook_content_type}"/>'
        '<Override PartName="/xl/worksheets/sheet1.xml" '
        f'ContentType="{sheet_content_type}"/>'
        '<Override PartName="/xl/styles.xml" '
        f'ContentType="{styles_content_type}"/>'
        "</Types>"
    )

    with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED) as report:
        report.writestr("[Content_Types].xml", content_types_xml)
        report.writestr("_rels/.rels", root_rels_xml)
        report.writestr("xl/workbook.xml", workbook_xml)
        report.writestr("xl/_rels/workbook.xml.rels", workbook_rels_xml)
        report.writestr("xl/worksheets/sheet1.xml", sheet_xml)
        report.writestr("xl/styles.xml", styles_xml)


def main() -> None:
    load_dotenv(PROJECT_ROOT / ".env")
    args = parse_arguments()

    stat_column = get_setting("STAT_COLUMN", "Post_Semester_GPA")
    aggregation_column = get_setting("AGGREGATION_COLUMN", "Major_Category")
    filter_column = get_setting("FILTER_COLUMN", "Paid_Subscription")
    filter_value = get_setting("FILTER_VALUE", "True")

    dataset_path = get_dataset_path(args.dataset)
    data = CSVFile(dataset_path)
    column_names = data.get_column_names()

    for column_name in [stat_column, aggregation_column, filter_column]:
        validate_column(column_name, column_names)

    values = numeric_values(data, stat_column)
    aggregation_counts = data.count_values(aggregation_column)
    total_rows = len(data.get_rows()) - 1
    filtered_rows = count_matching_rows(data, filter_column, filter_value)

    summary_rows = [
        ["Metric", "Value"],
        ["Dataset", dataset_path.name],
        ["Total rows", total_rows],
        [f"Rows where {filter_column} = {filter_value}", filtered_rows],
    ]
    statistics_rows = [
        ["Column", "Average", "Median"],
        [stat_column, f"{average(values):.3f}", f"{median(values):.3f}"],
    ]
    aggregation_rows = [["Value", "Count"]]
    aggregation_rows.extend(
        [value, count]
        for value, count in sorted(aggregation_counts.items())
    )

    if args.output:
        output_path = Path(args.output)
        if output_path.suffix.lower() != ".xlsx":
            output_path = output_path.with_suffix(".xlsx")
        create_excel_report(
            output_path,
            summary_rows,
            statistics_rows,
            aggregation_rows,
        )
        print(f"Excel report saved to: {output_path}")
    else:
        print("Summary")
        print(f"Dataset: {dataset_path.name}")
        print(f"Total rows: {total_rows}")
        print(f"Rows where {filter_column} = {filter_value}: {filtered_rows}")


if __name__ == "__main__":
    try:
        main()
    except (ValueError, FileNotFoundError) as error:
        print(f"Error: {error}")
        raise SystemExit(1)
