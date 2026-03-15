import breakfast_sheet
import time

if __name__ == '__main__':
    monthyear = time.strftime('%B_%Y')
    date = time.strftime('%Y%m%d')
    breakfast_sheet.generate_daily_sheet(monthyear, date)

# for i in range(1, 15):
#     day = f'2026030{i}' if i < 10 else f'202603{i}'
#     breakfast_sheet.generate_daily_sheet('March_2026', day)