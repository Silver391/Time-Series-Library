import os
import pandas as pd
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor
import logging  # 新增日志模块

# 配置日志格式
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def process_single_file(file_path, date_str):
    d = pd.read_csv(file_path)
    d['date'] = f'{date_str} ' + d['0'].astype(str)
    return d.drop(columns=['0'])


def process_csv_files(input_dir, output_dir, st_date, ed_date):
    start_date = datetime.strptime(st_date, '%Y%m%d')
    end_date = datetime.strptime(ed_date, '%Y%m%d')
    current_date = start_date
    file_paths = []
    
    logging.info(f"开始处理日期范围：{st_date} 至 {ed_date}")
    
    total_days = (end_date - start_date).days + 1
    found_files = 0

    while current_date <= end_date:
        date_str = current_date.strftime('%Y%m%d')
        file_path = os.path.join(input_dir, f'{date_str}.csv')
        if os.path.exists(file_path):
            file_paths.append((file_path, date_str))
            found_files += 1
        current_date += timedelta(days=1)
        
    logging.info(f"找到{found_files}/{total_days}个有效数据文件")

    with ThreadPoolExecutor() as executor:
        all_data = []
        for i, result in enumerate(executor.map(lambda x: process_single_file(*x), file_paths)):
            all_data.append(result)
            logging.info(f"已处理 {i+1}/{len(file_paths)} 个文件 ({((i+1)/len(file_paths)*100):.1f}%)")

    if all_data:
        combined_data = pd.concat(all_data, ignore_index=True)
        output_path = os.path.join(output_dir, f'{st_date}_{ed_date}.csv')
        combined_data.to_csv(output_path, index=False)
        logging.info(f"合并完成，总记录数：{len(combined_data)}")
        logging.info(f"已保存至：{output_path} (文件大小：{os.path.getsize(output_path)/1024/1024:.2f}MB)")


if __name__ == '__main__':
    input_dir = '/home/lenovo/yinzhou/csv_data'
    output_dir = '/home/lenovo/yinzhou/dataset'
    st_date = '20250227'
    ed_date = '20250327'
    process_csv_files(input_dir, output_dir, st_date, ed_date)