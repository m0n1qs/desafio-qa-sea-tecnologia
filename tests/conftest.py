
import base64
import html
import json
import os
import re
from pathlib import Path
from typing import Callable
from uuid import uuid4

import pytest
from dotenv import load_dotenv
from playwright.sync_api import Page

load_dotenv()


def _format_api_headers(headers):
    sensitive_headers = {"authorization", "cookie", "set-cookie"}
    return {
        key: "[REDACTED]" if key.lower() in sensitive_headers else value
        for key, value in headers.items()
    }


@pytest.fixture
def capture_screenshot(request, browser_type) -> Callable[..., Path]:
    scenario = re.search(r"CT\d+", request.node.name)
    if scenario is None:
        pytest.fail("Não foi possível identificar o ID do cenário para a evidência.")

    evidence_dir = (
        Path(__file__).resolve().parents[1]
        / "evidences"
        / "prints"
        / "automatizados"
    )
    evidence_dir.mkdir(parents=True, exist_ok=True)
    captures: list[tuple[str, bytes]] = []
    pdf_browser = browser_type.launch(headless=True)
    pdf_page = pdf_browser.new_page()

    def capture(
        page: Page,
        checkpoint: str,
        *,
        full_page: bool = False,
    ) -> Path:
        safe_checkpoint = re.sub(r"[^a-zA-Z0-9_-]+", "_", checkpoint).strip("_")
        if not safe_checkpoint:
            pytest.fail("Informe um nome válido para o ponto da captura.")

        screenshot = page.screenshot(full_page=full_page)
        captures.append((checkpoint, screenshot))
        sections = "\n".join(
            (
                f"<section><h2>{html.escape(label)}</h2>"
                f'<img src="data:image/png;base64,'
                f'{base64.b64encode(image).decode("ascii")}" '
                f'alt="{html.escape(label)}"></section>'
            )
            for label, image in captures
        )
        pdf_path = evidence_dir / f"{scenario.group()}.pdf"
        pdf_page.set_content(
            (
                "<!doctype html><html lang=\"pt-BR\"><head>"
                "<meta charset=\"utf-8\">"
                "<style>@page{size:A4 landscape;margin:10mm}"
                "body{font-family:Arial,sans-serif;margin:0}"
                "section{break-after:page;page-break-after:always}"
                "section:last-child{break-after:auto;page-break-after:auto}"
                "h2{font-size:14pt;margin:0 0 8mm}"
                "img{display:block;max-width:100%;max-height:160mm;"
                "width:auto;height:auto;margin:auto;object-fit:contain}"
                "</style></head><body>"
                f"{sections}"
                "</body></html>"
            )
        )
        pdf_page.pdf(
            path=str(pdf_path),
            format="A4",
            landscape=True,
            print_background=True,
        )
        return pdf_path

    try:
        yield capture
    finally:
        pdf_browser.close()


@pytest.fixture
def capture_api_evidence(request, browser_type):
    scenario = re.search(r"CT\d+", request.node.name)
    if scenario is None:
        pytest.fail("Não foi possível identificar o ID do cenário para a evidência.")

    evidence_dir = (
        Path(__file__).resolve().parents[1]
        / "evidences"
        / "api"
        / "automatizados"
    )
    evidence_dir.mkdir(parents=True, exist_ok=True)
    recorded_responses = []

    def record(response, context=None, interface_screenshot=None):
        try:
            response_body = json.dumps(
                response.json(),
                ensure_ascii=False,
                indent=2,
            )
        except (ValueError, json.JSONDecodeError):
            response_body = response.text or "(resposta sem corpo)"

        recorded_responses.append(
            {
                "request_method": response.request.method,
                "request_url": response.request.url,
                "request_headers": _format_api_headers(
                    response.request.headers
                ),
                "status_code": response.status_code,
                "reason": response.reason,
                "response_headers": _format_api_headers(response.headers),
                "response_body": response_body,
                "context": context or {},
                "interface_screenshot": interface_screenshot,
            }
        )

    yield record

    report = getattr(request.node, "rep_call", None)
    execution_result = report.outcome.upper() if report else "UNKNOWN"
    failure_details = ""
    if report and report.failed:
        failure_details = str(report.longrepr)

    sections = []
    for index, result in enumerate(recorded_responses, start=1):
        request_headers = json.dumps(
            result["request_headers"],
            ensure_ascii=False,
            indent=2,
        )
        response_headers = json.dumps(
            result["response_headers"],
            ensure_ascii=False,
            indent=2,
        )
        context = json.dumps(
            result["context"],
            ensure_ascii=False,
            indent=2,
        )
        sections.append(
            "<section>"
            f"<h2>Requisição {index}</h2>"
            "<h3>Requisição</h3>"
            f"<p><strong>Método:</strong> "
            f"{html.escape(result['request_method'])}</p>"
            f"<p><strong>URL:</strong> "
            f"{html.escape(result['request_url'])}</p>"
            f"<pre>{html.escape(request_headers)}</pre>"
            "<h3>Resposta</h3>"
            f"<p><strong>Status:</strong> "
            f"{result['status_code']} {html.escape(result['reason'])}</p>"
            f"<pre>{html.escape(response_headers)}</pre>"
            f"<pre>{html.escape(result['response_body'])}</pre>"
            f"<h3>Dados comparados</h3><pre>{html.escape(context)}</pre>"
            "</section>"
        )
        if result["interface_screenshot"] is not None:
            screenshot_base64 = base64.b64encode(
                result["interface_screenshot"]
            ).decode("ascii")
            sections.append(
                "<section><h2>Interface da listagem</h2>"
                f'<img src="data:image/png;base64,{screenshot_base64}" '
                'alt="Interface da listagem">'
                "</section>"
            )

    sections.append(
        "<section><h2>Resultado da execução</h2>"
        f"<p><strong>{html.escape(execution_result)}</strong></p>"
        f"<pre>{html.escape(failure_details or 'Sem falhas.')}</pre>"
        "</section>"
    )
    pdf_browser = browser_type.launch(headless=True)
    try:
        pdf_page = pdf_browser.new_page()
        pdf_page.set_content(
            (
                "<!doctype html><html lang=\"pt-BR\"><head>"
                "<meta charset=\"utf-8\">"
                "<style>@page{size:A4;margin:16mm}"
                "body{font-family:Arial,sans-serif;color:#222}"
                "section{break-after:page;page-break-after:always}"
                "section:last-child{break-after:auto;page-break-after:auto}"
                "h1{font-size:20pt}h2{font-size:16pt}"
                "h3{font-size:12pt;margin-bottom:4px}"
                "pre{white-space:pre-wrap;overflow-wrap:anywhere;"
                "font:9pt Consolas,monospace;background:#f3f4f6;"
                "padding:10px;border:1px solid #ddd}"
                "img{display:block;max-width:100%;max-height:250mm;"
                "width:auto;height:auto;object-fit:contain;margin:auto}"
                "p{overflow-wrap:anywhere}</style></head><body>"
                f"<h1>Evidência de API — {scenario.group()}</h1>"
                f"<p>Teste: {html.escape(request.node.name)}</p>"
                f"<p>Resultado: {html.escape(execution_result)}</p>"
                f"{''.join(sections)}</body></html>"
            )
        )
        pdf_page.pdf(
            path=str(evidence_dir / f"{scenario.group()}.pdf"),
            format="A4",
            print_background=True,
        )
    finally:
        pdf_browser.close()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    setattr(item, f"rep_{report.when}", report)


@pytest.fixture(scope="session")
def base_url():
    """
    Retorna a URL principal da aplicação.
    """
    return os.getenv(
        "BASE_URL",
        "https://analista-teste.seatecnologia.com.br"
    ).rstrip("/")


@pytest.fixture
def api_url():
    """
    Retorna a URL do endpoint de trabalhadores.
    """
    return os.getenv(
        "API_URL",
        "https://analista-teste.seatecnologia.com.br/employees"
    )


@pytest.fixture
def cadastro_form(page, base_url):
    page.goto(base_url, wait_until="domcontentloaded")
    page.get_by_role("button", name=re.compile("Adicionar", re.I)).click()
    return page


@pytest.fixture
def worker_test_data(request):
    scenario_id = re.search(r"CT\d+", request.node.name)
    if scenario_id is None:
        pytest.fail("Não foi possível identificar o ID do cenário.")

    suffix = scenario_id.group()
    unique_id = uuid4().hex[:8].upper()
    cpf_digits = f"{uuid4().int % 1_000_000_000:09d}"
    if len(set(cpf_digits)) == 1:
        cpf_digits = f"{int(cpf_digits) + 1:09d}"
    for weight in (10, 11):
        remainder = sum(
            int(digit) * (weight - index)
            for index, digit in enumerate(cpf_digits)
        ) % 11
        cpf_digits += str(0 if remainder < 2 else 11 - remainder)

    data = {
        "name": f"{os.getenv('TEST_WORKER_PREFIX', 'QA Teste')} {suffix}-{unique_id}",
        "cpf": cpf_digits,
        "birth_day": os.getenv("TEST_WORKER_BIRTHDAY", ""),
        "rg": f"{os.getenv('TEST_WORKER_RG_PREFIX', 'RG-QA-')}{suffix}-{unique_id}",
        "ca_number": f"{os.getenv('TEST_WORKER_CA_PREFIX', 'CA-QA-')}{suffix}-{unique_id}",
    }
    if not data["birth_day"]:
        data["birth_day"] = "1990-01-01"
    return data


@pytest.fixture
def existing_test_worker_name():
    return os.getenv("TEST_WORKER_NAME") or f"QA Teste {uuid4().hex[:8].upper()}"


@pytest.fixture
def browser_context_args(browser_context_args):
    """
    Configura o contexto do navegador utilizado pelo Playwright.
    """
    return {
        **browser_context_args,
        "ignore_https_errors": False,
        "viewport": {
            "width": 1366,
            "height": 900
        },
        "locale": "pt-BR",
    }
