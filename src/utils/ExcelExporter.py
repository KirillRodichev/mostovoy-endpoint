import pandas as pd
import numpy as np

from src.constants.Constants import *


class ExcelExporter:
    data_frames = []
    common_data = []
    session_number = 0

    @staticmethod
    def store_session_data(data, avg, standard_deviation, numbers, time_sum):
        data.append([
            'Всего: ',
            numbers[IS_BREAKDOWN],
            numbers[IS_FAILURE],
            numbers[IS_BUSY],
            numbers[IS_GENERATING],
            time_sum,
        ])
        ExcelExporter.data_frames.append(pd.DataFrame(data, columns=HEADERS))

        session_common_data = [
            ExcelExporter.session_number,
            numbers[IS_BREAKDOWN],
            numbers[IS_FAILURE],
            numbers[IS_BUSY],
            numbers[IS_GENERATING],
            avg,
            standard_deviation
        ]

        ExcelExporter.common_data.append(session_common_data)

        ExcelExporter.session_number += 1

    @staticmethod
    def export_stored_data():
        writer = pd.ExcelWriter(
            r'D:\My Documents\uni\grade_4th\2nd\DB-security\ipo-project-1.0\output\stats\data.xlsx',
            engine='openpyxl'
        )

        pd.set_option('display.max_colwidth', 300)
        for i in range(len(ExcelExporter.data_frames)):
            name = 'Sheet' + str(i)
            ExcelExporter.data_frames[i].to_excel(writer, sheet_name=name, index=False)

        writer.save()

        c_writer = pd.ExcelWriter(
            r'D:\My Documents\uni\grade_4th\2nd\DB-security\ipo-project-1.0\output\stats\common_data.xlsx',
            engine='openpyxl'
        )

        transposed = np.array(ExcelExporter.common_data).transpose()
        ExcelExporter.common_data.append([
            'В среднем',
            np.average(transposed[1]),
            np.average(transposed[2]),
            np.average(transposed[3]),
            np.average(transposed[4]),
            int(np.average(transposed[5])),
            int(np.average(transposed[6])),
        ])
        transposed = np.array(ExcelExporter.common_data).transpose()
        data = {}
        for i in range(len(SESSION_HEADERS)):
            data[SESSION_HEADERS[i]] = transposed[i]

        df = pd.DataFrame(data, columns=SESSION_HEADERS)
        df.to_excel(c_writer, index=False)

        c_writer.save()
