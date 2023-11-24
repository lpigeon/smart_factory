# CSV 파일에서 데이터 읽어오기
        data = self.read_csv('./most_common_values.csv')
        data_text = "\n".join([f"{key}: {value}" for key, value in data.items()])