# --- START OF FILE get_location_url.py ---
import glob
from pathlib import Path
from bs4 import BeautifulSoup
import pandas as pd


class LocationURLProcessor:
    def __init__(self, input_dir, result_location_dir):
        self.input_dir = Path(input_dir)
        self.result_location_dir = Path(result_location_dir)
        self.result_location_dir.mkdir(parents=True, exist_ok=True)

    def processing_list(self, univ, year, item_list, df):
        print(univ)
        for item in item_list:
            x = item.find_all('a')
            exam_location = x[0].text[6:]
            try:
                location_link = x[0].get("href")
            except IndexError:
                location_link = "None"
            data = {'exam_location': exam_location, 'univ': univ, 'year': year, 'location_link': location_link}
            df = pd.concat([df, pd.DataFrame([data])], ignore_index=True)
        return df

    def processing_department(self, filename):
        filepath = self.input_dir / filename
        with open(filepath, 'r', encoding="utf-8") as file:
            html = file.read()
            soup = BeautifulSoup(html, 'html.parser')

        fields = ['exam_location', 'univ', 'year', 'location_link']
        df = pd.DataFrame(columns=fields)
        df1 = pd.DataFrame(columns=fields)
        df2 = pd.DataFrame(columns=fields)

        title_str = soup.head.find_all('title')[0].text
        year_pos = title_str.find('年')
        year = title_str[year_pos - 3:year_pos]

        univ_pos = title_str.find('-')
        univ = title_str[:univ_pos].rstrip()

        dark_list = soup.body.find_all(bgcolor="#DEDEDC")  # 褐色
        df1 = self.processing_list(univ, year, dark_list, df)

        white_list = soup.body.find_all(bgcolor="#FFFFFF")  # 白色
        df2 = self.processing_list(univ, year, white_list, df)

        max_len = max(len(df1), len(df2))
        for i in range(max_len):
            if i < len(df1):
                df = pd.concat([df, df1.iloc[[i]]], ignore_index=True)
            if i < len(df2):
                df = pd.concat([df, df2.iloc[[i]]], ignore_index=True)

        output_csv_path = self.result_location_dir / f'{univ}.csv'
        df.to_csv(output_csv_path, encoding='utf-8-sig', index=False)
        print(f"Processed and saved: {output_csv_path}")

    def run(self):
        department_dir = self.input_dir
        for file in glob.iglob(str(department_dir / '*交叉查榜*.html')):
            self.processing_department(Path(file).name)

        # Combine all university CSVs into whole.csv
        self.combine_csvs()

    def combine_csvs(self):
        fields = ['exam_location', 'univ', 'year', 'location_link']
        df_whole = pd.DataFrame(columns=fields)
        for file in glob.iglob(str(self.result_location_dir / '*大學*.csv')):
            df = pd.read_csv(file)
            df_whole = pd.concat([df_whole, df], ignore_index=True)

        whole_csv_path = self.result_location_dir / 'whole.csv'
        df_whole.to_csv(whole_csv_path, encoding='utf-8-sig', index=False)
        print(f"Combined all CSVs and saved: {whole_csv_path}")


if __name__ == "__main__":
    input_directory = 'data/department'  # Replace with your input directory
    result_directory = 'result/location'  # Replace with your result directory

    processor = LocationURLProcessor(input_directory, result_directory)
    processor.run()