import typer
import asyncio

from ocr import invoice_ocr_baseline, invoice_ocr_step_1, invoice_ocr_step_2, invoice_ocr_step_3, invoice_ocr_step_4, invoice_ocr_step_5
from evaluate import evaluate_step_2, evaluate_step_3, evaluate_step_4, evaluate_step_5


app = typer.Typer()

@app.command()
def run_baseline() -> None:
    asyncio.run(invoice_ocr_baseline())

@app.command()
def run_step_1() -> None:
    asyncio.run(invoice_ocr_step_1())

@app.command()
def run_step_2(eval: bool = False) -> None:
    invoices = asyncio.run(invoice_ocr_step_2())
    if eval:
        evaluate_step_2(invoices)

@app.command()
def run_step_3(eval: bool = False) -> None:
    invoices = asyncio.run(invoice_ocr_step_3())
    if eval:
        evaluate_step_3(invoices)

@app.command()
def run_step_4(eval: bool = False) -> None:
    invoices = asyncio.run(invoice_ocr_step_4())
    if eval:
        evaluate_step_4(invoices)

@app.command()
def run_step_5(eval: bool = False, n_retries: int = 5, debug: bool = False) -> None:
    invoices = asyncio.run(invoice_ocr_step_5(n_retries, debug))
    if eval:
        evaluate_step_5(invoices)

if __name__ == '__main__':
    app()
