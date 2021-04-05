import pandas as pd

from src.constants.Constants import *


class ExcelExporter:
    data_frames = []

    @staticmethod
    def store_session_data(data, avg, standard_deviation, numbers, time_sum):
        data.append([
            'Всего: ',
            numbers[IS_BREAKDOWN],
            numbers[IS_FAILURE],
            numbers[IS_BUSY],
            numbers[IS_GENERATING],
            time_sum
        ])
        data.append([
            'МО: ',
            avg,
        ])
        data.append([
            'СКО: ',
            standard_deviation
        ])
        ExcelExporter.data_frames.append(pd.DataFrame(data, columns=HEADERS))

    @staticmethod
    def export_stored_data():
        writer = pd.ExcelWriter(
            r'D:\My Documents\uni\grade_4th\2nd\DB-security\ipo-project-1.0\output\stats\data.xlsx',
            engine='openpyxl'
        )

        for i in range(len(ExcelExporter.data_frames)):
            name = 'Sheet' + str(i)
            ExcelExporter.data_frames[i].to_excel(writer, sheet_name=name, index=False)

        writer.save()
