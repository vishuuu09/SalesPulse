import logging
import typer
from rich import print
from salespulse.config import settings
from salespulse.generator import generate
from salespulse.pipeline import run

app=typer.Typer(help="SalesPulse data analytics pipeline")

@app.command()
def generate_data(orders:int=typer.Option(5000,min=100),seed:int=42):
    generate(settings.raw_dir,orders,seed)
    print(f"[green]Generated source data in {settings.raw_dir}[/green]")

@app.command()
def run_pipeline():
    logging.basicConfig(level=logging.INFO,format="%(asctime)s | %(levelname)s | %(message)s")
    result=run()
    for key,value in result.items(): print(f"{key}: {value}")

if __name__=="__main__": app()
