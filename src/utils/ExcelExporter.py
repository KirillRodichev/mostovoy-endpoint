import pandas as pd

from src.constants.Constants import *


class ExcelExporter:

    @staticmethod
    def export_session_data(data, avg, standard_deviation, numbers):
        data.append(
            [
                'Всего: ',
                numbers[IS_BREAKDOWN],
                numbers[IS_FAILURE],
                numbers[IS_BUSY],
                numbers[IS_GENERATING],
                ''
            ]
        )
        data.append(
            [
                'МО: ',
                avg,
            ]
        )
        data.append(
            [
                'СКО: ',
                standard_deviation
            ]
        )
        df = pd.DataFrame(
            data,
            columns=HEADERS
        )

        df.to_excel(r'D:\My Documents\uni\grade_4th\2nd\DB-security\ipo-project-1.0\output\stats\data.xlsx', index=False, header=True)
