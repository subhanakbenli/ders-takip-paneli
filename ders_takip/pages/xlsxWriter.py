from openpyxl import Workbook
from openpyxl.utils import get_column_letter
from openpyxl.styles import Font

def _set_column_width(sheet, column_letters, width):
    """Set the width for given column letters in the Excel sheet."""
    for col_letter in column_letters:
        sheet.column_dimensions[col_letter].width = width

def _write_header(sheet, row_index, headers):
    """Write the header row with bold font."""
    for col_index, header in enumerate(headers, start=1):
        cell = sheet.cell(row=row_index, column=col_index, value=header)
        cell.font = Font(bold=True)

def _write_row(sheet, row_index, row_data):
    """Write a single row of data."""
    for col_index, cell_data in enumerate(row_data, start=1):
        sheet.cell(row=row_index, column=col_index, value=cell_data)

def write_to_excel(teachers_data, file_name):
    """
    Write teacher data with courses and documents to an Excel file.

    Args:
        teachers_data (list): List of teacher data from the get_teachers_with_courses_and_documents function.
        file_name (str): The name of the file (without the .xlsx extension) to save.
    """
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Teachers Overview"

    # Set column widths
    column_width = 30

    # Write data
    row_index = 1
    for teacher in teachers_data:
        # Write teacher data
        sheet.cell(row=row_index, column=1, value="Teacher Name")
        sheet.cell(row=row_index, column=2, value=f"{teacher['name']} {teacher['surname']}")
        row_index += 1

        sheet.cell(row=row_index, column=1, value="Title")
        sheet.cell(row=row_index, column=2, value=teacher['title'])
        row_index += 1

        sheet.cell(row=row_index, column=1, value="Description")
        sheet.cell(row=row_index, column=2, value=teacher['description'])
        row_index += 1

        sheet.cell(row=row_index, column=1, value="Warning Message")
        sheet.cell(row=row_index, column=2, value=teacher['warning_message'])
        row_index += 2

        # Write courses
        for course in teacher['courses']:
            sheet.cell(row=row_index, column=1, value="Course Name")
            sheet.cell(row=row_index, column=2, value=course['name'])
            row_index += 1

            sheet.cell(row=row_index, column=1, value="Description")
            sheet.cell(row=row_index, column=2, value=course['description'])
            row_index += 1

            sheet.cell(row=row_index, column=1, value="Warning Message")
            sheet.cell(row=row_index, column=2, value=course['warning_message'])
            row_index += 1

            # Write documents
            for document in course['documents']:
                sheet.cell(row=row_index, column=1, value="Document Name")
                sheet.cell(row=row_index, column=2, value=document['belge_adi'])
                sheet.cell(row=row_index, column=3, value=document['warning_message'])
                row_index += 1

            row_index += 1
        row_index += 2

    # Adjust column widths
    for col_index in range(1, sheet.max_column + 1):
        col_letter = get_column_letter(col_index)
        sheet.column_dimensions[col_letter].width = column_width

    try:
        workbook.save(f'{file_name}.xlsx')
        print(f"{file_name}.xlsx has been created successfully.")
    except Exception as e:
        print("Please close the Excel file:", e)
