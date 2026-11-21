from sqlalchemy import create_engine, text
from salespulse.config import settings

def engine():
    return create_engine(settings.database_url,pool_pre_ping=True,future=True)

def run_sql_file(db, path):
    sql=open(path,encoding="utf-8").read()
    with db.begin() as conn:
        for statement in sql.split(";"):
            if statement.strip(): conn.execute(text(statement))
