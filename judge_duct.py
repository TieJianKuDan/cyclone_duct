# Judge whether is atmospheric duct in somewhere
import libs.tools as tools

if __name__ == "__main__":
    file_path = "data/sondes/nestor_2019.hsa"
    records = tools.read_hsa(file_path)
    selected = tools.select_record(records)
    print(selected)
