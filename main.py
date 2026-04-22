import typer
import asyncio

from ocr import InvoiceOCRBaseline, InvoiceOCRStep1, InvoiceOCRStep2, InvoiceOCRStep3, InvoiceOCRStep4, InvoiceOCRStep5
from evaluate import evaluate_step_2, evaluate_step_3, evaluate_step_4, evaluate_step_5


app = typer.Typer()

@app.command()
def run_baseline() -> None:
    asyncio.run(InvoiceOCRBaseline().run_invoice_ocr())

@app.command()
def run_step_1() -> None:
    asyncio.run(InvoiceOCRStep1().run_invoice_ocr())

@app.command()
def run_step_2(eval: bool = False) -> None:
    invoices = asyncio.run(InvoiceOCRStep2().run_invoice_ocr())
    if eval:
        evaluate_step_2(invoices)

@app.command()
def run_step_3(eval: bool = False) -> None:
    invoices = asyncio.run(InvoiceOCRStep3().run_invoice_ocr())
    if eval:
        evaluate_step_3(invoices)

@app.command()
def run_step_4(eval: bool = False) -> None:
    invoices = asyncio.run(InvoiceOCRStep4().run_invoice_ocr())
    if eval:
        evaluate_step_4(invoices)

@app.command()
def run_step_5(eval: bool = False, n_retries: int = 5, debug: bool = False) -> None:
    invoices = asyncio.run(InvoiceOCRStep5(n_retries, debug).run_invoice_ocr())
    if eval:
        evaluate_step_5(invoices)

if __name__ == '__main__':
    app()
