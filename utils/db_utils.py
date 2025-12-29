from sqlalchemy import inspect

# 데이터 베이스 행렬을 딕셔너리 형식으로 변환하는 기능
def row_to_dict(row) -> dict:
    return {key: getattr(row, key) for key in inspect(row.attrs.keys())}
