import copy
import os
import re
from uuid import uuid4

import pytest
import requests
from playwright.sync_api import expect


TIMEOUT = 15


@pytest.fixture
def writable_employee(request, api_url, capture_api_evidence):
    if os.getenv("ALLOW_TEST_WRITES") != "1":
        pytest.skip("Defina ALLOW_TEST_WRITES=1 para habilitar gravações de teste.")

    scenario_id = re.search(r"CT\d+", request.node.name)
    if scenario_id is None:
        pytest.fail("Não foi possível identificar o ID do cenário.")

    unique_id = uuid4().hex[:12].upper()
    cpf = f"{uuid4().int % 1_000_000_000:09d}"
    for weight in (10, 11):
        remainder = sum(
            int(digit) * (weight - index)
            for index, digit in enumerate(cpf)
        ) % 11
        cpf += str(0 if remainder < 2 else 11 - remainder)

    employee_name = f"QA Ficticio {scenario_id.group()}-{unique_id}"
    uses_epi = scenario_id.group() != "CT032"
    create_payload = {
        "state": {
            "employee": {
                "isActive": False,
                "name": employee_name,
                "gender": "masculino",
                "cpf": cpf,
                "birthDay": "1990-05-12",
                "rg": f"RG-QA-{unique_id}",
                "role": "Cargo 01",
                "usesEpi": uses_epi,
                "activity": "Ativid 01",
                "caNumber": f"CA-QA-{unique_id}",
            }
        }
    }

    create_response = requests.post(
        api_url,
        json=create_payload,
        timeout=TIMEOUT,
    )
    capture_api_evidence(
        create_response,
        context={"Payload fictício enviado para criação": create_payload},
    )
    employee_id = None
    if 200 <= create_response.status_code < 300:
        try:
            created_payload = create_response.json()
        except ValueError:
            created_payload = None
        if isinstance(created_payload, dict):
            employee_id = created_payload.get("id")

    if not employee_id and 200 <= create_response.status_code < 300:
        location = create_response.headers.get("Location", "").rstrip("/")
        if location:
            employee_id = location.rsplit("/", 1)[-1]

    if not employee_id:
        list_response = requests.get(api_url, timeout=TIMEOUT)
        capture_api_evidence(
            list_response,
            context={"Localização do cadastro fictício": employee_name},
        )
        if list_response.status_code == 200:
            employees = list_response.json()
            if isinstance(employees, list):
                matches = [
                    employee
                    for employee in employees
                    if employee.get("state", {})
                    .get("employee", {})
                    .get("name")
                    == employee_name
                ]
                if len(matches) == 1:
                    employee_id = matches[0].get("id")

    assert employee_id is not None, (
        f"Não foi possível localizar o trabalhador fictício após POST "
        f"HTTP {create_response.status_code}; o ID é necessário para "
        "verificação e limpeza."
    )

    employee_url = f"{api_url.rstrip('/')}/{employee_id}"

    verification_response = requests.get(employee_url, timeout=TIMEOUT)
    capture_api_evidence(
        verification_response,
        context={
            "ID retornado/localizado para o trabalhador fictício": employee_id,
            "Nome fictício esperado": employee_name,
        },
    )
    try:
        original_payload = verification_response.json()
    except ValueError:
        original_payload = None

    yield {
        "id": str(employee_id),
        "url": employee_url,
        "original": original_payload,
        "create_status": create_response.status_code,
        "verification_status": verification_response.status_code,
        "expected_name": employee_name,
    }


def _assert_created_employee(employee):
    assert employee["create_status"] == 201, (
        f"POST deveria retornar HTTP 201, mas retornou "
        f"HTTP {employee['create_status']}."
    )
    assert employee["verification_status"] == 200
    original_payload = employee["original"]
    assert isinstance(original_payload, dict), (
        "A consulta do trabalhador criado não retornou um objeto JSON."
    )
    assert original_payload.get("id") == employee["id"]
    original_employee = original_payload.get("state", {}).get("employee")
    assert isinstance(original_employee, dict)
    assert original_employee.get("name") == employee["expected_name"]
    return original_payload, original_employee


def _update_and_verify_role_activity(
    employee,
    method,
    capture_api_evidence,
):
    original_payload, _ = _assert_created_employee(employee)

    for number in range(1, 6):
        changes = {
            "role": f"Cargo {number:02}",
            "activity": f"Ativid {number:02}",
        }
        if method == "PUT":
            payload = copy.deepcopy(original_payload)
            payload["state"]["employee"].update(changes)
        else:
            payload = {"state": {"employee": changes}}

        update_response = requests.request(
            method,
            employee["url"],
            json=payload,
            timeout=TIMEOUT,
        )
        capture_api_evidence(
            update_response,
            context={
                "Valor testado": number,
                "Payload enviado": payload,
            },
        )
        assert 200 <= update_response.status_code < 300, (
            f"{method} falhou para Cargo/Ativid {number:02}: "
            f"HTTP {update_response.status_code}."
        )

        verification_response = requests.get(employee["url"], timeout=TIMEOUT)
        capture_api_evidence(
            verification_response,
            context={
                "Cargo esperado": changes["role"],
                "Atividade esperada": changes["activity"],
            },
        )
        assert verification_response.status_code == 200
        current_employee = verification_response.json()["state"]["employee"]
        assert current_employee.get("role") == changes["role"], (
            f"{method} não persistiu o cargo {changes['role']}."
        )
        assert current_employee.get("activity") == changes["activity"], (
            f"{method} não persistiu a atividade {changes['activity']}."
        )


def _capture_full_listing(page):
    page.evaluate(
        """() => {
            for (const element of document.querySelectorAll("*")) {
                const style = getComputedStyle(element);
                if (
                    element.scrollHeight > element.clientHeight + 50
                    && element.clientHeight > 0
                    && style.overflowY !== "visible"
                ) {
                    element.style.setProperty("height", "auto", "important");
                    element.style.setProperty("max-height", "none", "important");
                    element.style.setProperty("overflow", "visible", "important");
                }
            }
        }"""
    )
    return page.screenshot(full_page=True)


@pytest.fixture
def employees_response(api_url, capture_api_evidence):
    response = requests.get(api_url, timeout=TIMEOUT)
    capture_api_evidence(response)
    return response


@pytest.mark.api
@pytest.mark.automatizado
def test_CT018_consultar_trabalhador_com_GET(employees_response):
    assert employees_response.status_code == 200
    assert "json" in employees_response.headers.get("Content-Type", "").lower()

    payload = employees_response.json()
    assert isinstance(payload, list)
    assert all(isinstance(employee, dict) for employee in payload)
    assert all("id" in employee and "state" in employee for employee in payload)


@pytest.mark.api
@pytest.mark.automatizado
def test_CT019_consultar_cabecalhos_utilizando_HEAD(api_url, capture_api_evidence):
    response = requests.head(api_url, timeout=TIMEOUT)
    capture_api_evidence(response)

    assert response.status_code < 500
    assert response.content == b""


@pytest.mark.api
@pytest.mark.automatizado
def test_CT020_consultar_metodos_com_OPTIONS(
    api_url,
    capture_api_evidence,
):
    response = requests.options(
        api_url,
        headers={
            "Origin": "https://qa.invalid",
            "Access-Control-Request-Method": "GET",
        },
        timeout=TIMEOUT,
    )
    capture_api_evidence(response)

    assert response.status_code < 500
    methods = response.headers.get("Access-Control-Allow-Methods", "").upper()
    origin = response.headers.get("Access-Control-Allow-Origin", "").strip()
    cors_headers = {
        name: value
        for name, value in response.headers.items()
        if name.lower().startswith("access-control-")
    }

    assert methods, "A resposta não anunciou métodos HTTP."
    assert origin, "A resposta não anunciou Access-Control-Allow-Origin."
    assert cors_headers


@pytest.mark.api
@pytest.mark.automatizado
def test_CT026_comparar_interface_com_API(
    page,
    base_url,
    api_url,
    capture_api_evidence,
):
    page.goto(base_url, wait_until="domcontentloaded")
    summary_pattern = re.compile(r"Ativos\s+(\d+)\s*/\s*(\d+)")
    page.wait_for_function(
        r"/Ativos\s+\d+\s*\/\s*\d+/.test(document.body.innerText)"
    )
    summary_text = page.locator("body").inner_text()
    summary_match = summary_pattern.search(summary_text)
    assert summary_match is not None, "O resumo de totais não apareceu na interface."
    ui_active_total, ui_worker_total = map(int, summary_match.groups())

    response = requests.get(api_url, timeout=TIMEOUT)
    try:
        payload = response.json()
    except ValueError:
        payload = None

    api_worker_total = len(payload) if isinstance(payload, list) else None
    api_active_total = (
        sum(
            employee.get("state", {})
            .get("employee", {})
            .get("isActive")
            is True
            for employee in payload
            if isinstance(employee, dict)
        )
        if isinstance(payload, list)
        else None
    )
    capture_api_evidence(
        response,
        context={
            "Resumo exibido na interface": summary_match.group(0),
            "Total de trabalhadores na interface": ui_worker_total,
            "Total de trabalhadores ativos na interface": ui_active_total,
            "Total de trabalhadores calculado pela API": api_worker_total,
            "Total de trabalhadores ativos calculado pela API": api_active_total,
        },
        interface_screenshot=_capture_full_listing(page),
    )

    assert response.status_code == 200
    assert isinstance(payload, list), "A resposta GET deve ser uma lista JSON."
    assert all(
        isinstance(employee, dict)
        and isinstance(employee.get("state", {}).get("employee"), dict)
        for employee in payload
    ), "Cada registro da API deve conter state.employee."
    assert ui_worker_total == api_worker_total, (
        f"Total de trabalhadores diverge: interface={ui_worker_total}, "
        f"API={api_worker_total}."
    )
    assert ui_active_total == api_active_total, (
        f"Total de ativos diverge: interface={ui_active_total}, "
        f"API={api_active_total}."
    )


@pytest.mark.api
@pytest.mark.automatizado
def test_CT028_comparar_total_inativos_inferido_com_API(
    page,
    base_url,
    api_url,
    capture_api_evidence,
):
    page.goto(base_url, wait_until="domcontentloaded")
    summary_pattern = re.compile(r"Ativos\s+(\d+)\s*/\s*(\d+)")
    page.wait_for_function(
        r"/Ativos\s+\d+\s*\/\s*\d+/.test(document.body.innerText)"
    )
    active_filter = page.get_by_role(
        "button",
        name=re.compile("Ver apenas ativos", re.I),
    )
    inactive_filter = page.get_by_role(
        "button",
        name=re.compile("Ver apenas inativos", re.I),
    )
    assert active_filter.count() == 1, (
        "O filtro 'Ver apenas ativos' esperado não foi encontrado."
    )
    assert inactive_filter.count() == 0, (
        "A interface agora possui filtro de inativos; revise o CT027 "
        "para validar a listagem filtrada diretamente."
    )

    summary_text = page.locator("body").inner_text()
    summary_match = summary_pattern.search(summary_text)
    assert summary_match is not None, "O resumo de totais não apareceu na interface."
    ui_active_total, ui_worker_total = map(int, summary_match.groups())
    ui_employee_total = page.evaluate(
        """() => {
            const summary = [...document.querySelectorAll("span")].find(
                element => /^Ativos\\s+\\d+\\s*\\/\\s*\\d+$/.test(
                    element.textContent.trim()
                )
            );
            const rows = summary?.parentElement?.querySelector(":scope > div");
            return rows
                ? [...rows.children].filter(
                    row => row.firstElementChild?.textContent.trim()
                ).length
                : null;
        }"""
    )
    assert ui_employee_total is not None, (
        "Não foi possível contar os trabalhadores exibidos na interface."
    )
    ui_inactive_total = ui_employee_total - ui_active_total

    response = requests.get(api_url, timeout=TIMEOUT)
    try:
        payload = response.json()
    except ValueError:
        payload = None

    api_worker_total = len(payload) if isinstance(payload, list) else None
    api_employee_total = (
        sum(
            isinstance(
                employee.get("state", {}).get("employee", {}).get("name"),
                str,
            )
            and bool(
                employee.get("state", {})
                .get("employee", {})
                .get("name", "")
                .strip()
            )
            for employee in payload
            if isinstance(employee, dict)
            and isinstance(employee.get("state", {}).get("employee"), dict)
        )
        if isinstance(payload, list)
        else None
    )
    api_inactive_total = (
        sum(
            employee.get("state", {})
            .get("employee", {})
            .get("isActive")
            is False
            for employee in payload
            if isinstance(employee, dict)
        )
        if isinstance(payload, list)
        else None
    )
    capture_api_evidence(
        response,
        context={
            "Resumo exibido na interface": summary_match.group(0),
            "Filtro exclusivo de inativos na interface": "Não existe",
            "Filtro disponível na interface": "Ver apenas ativos",
            "Total indicado no resumo da interface": ui_worker_total,
            "Total de trabalhadores com nome na interface": ui_employee_total,
            "Total de trabalhadores inativos calculado pela interface": (
                ui_inactive_total
            ),
            "Total de trabalhadores calculado pela API": api_worker_total,
            "Total de trabalhadores com nome calculado pela API": (
                api_employee_total
            ),
            "Total de trabalhadores inativos calculado pela API": (
                api_inactive_total
            ),
        },
        interface_screenshot=_capture_full_listing(page),
    )

    assert response.status_code == 200
    assert isinstance(payload, list), "A resposta GET deve ser uma lista JSON."
    assert all(
        isinstance(employee, dict)
        and isinstance(employee.get("state", {}).get("employee"), dict)
        for employee in payload
    ), "Cada registro da API deve conter state.employee."
    assert ui_employee_total == api_employee_total, (
        f"Total de trabalhadores com nome diverge: interface={ui_employee_total}, "
        f"API={api_employee_total}."
    )
    assert ui_inactive_total == api_inactive_total, (
        f"Total de inativos diverge: interface={ui_inactive_total}, "
        f"API={api_inactive_total}."
    )


@pytest.mark.api
@pytest.mark.automatizado
def test_CT030_atualizar_cargo_e_atividade_com_PUT(
    writable_employee,
    capture_api_evidence,
):
    _update_and_verify_role_activity(
        writable_employee,
        "PUT",
        capture_api_evidence,
    )


@pytest.mark.api
@pytest.mark.automatizado
def test_CT031_atualizar_cargo_e_atividade_com_PATCH(
    writable_employee,
    capture_api_evidence,
):
    _update_and_verify_role_activity(
        writable_employee,
        "PATCH",
        capture_api_evidence,
    )


@pytest.mark.api
@pytest.mark.automatizado
def test_CT032_alterar_uso_de_EPI_para_com_EPI(
    writable_employee,
    capture_api_evidence,
):
    _assert_created_employee(writable_employee)

    payload = {"state": {"employee": {"usesEpi": True}}}
    response = requests.patch(
        writable_employee["url"],
        json=payload,
        timeout=TIMEOUT,
    )
    capture_api_evidence(response, context={"Payload enviado": payload})
    assert 200 <= response.status_code < 300, (
        f"PATCH para habilitar EPI retornou HTTP {response.status_code}."
    )

    verification = requests.get(writable_employee["url"], timeout=TIMEOUT)
    capture_api_evidence(
        verification,
        context={"Valor esperado de usesEpi": True},
    )
    assert verification.status_code == 200
    current_employee = verification.json()["state"]["employee"]
    assert current_employee.get("usesEpi") is True


@pytest.mark.api
@pytest.mark.automatizado
def test_CT033_alterar_uso_de_EPI_para_sem_EPI(
    writable_employee,
    capture_api_evidence,
):
    _assert_created_employee(writable_employee)

    payload = {"state": {"employee": {"usesEpi": False}}}
    response = requests.patch(
        writable_employee["url"],
        json=payload,
        timeout=TIMEOUT,
    )
    capture_api_evidence(response, context={"Payload enviado": payload})
    assert 200 <= response.status_code < 300, (
        f"PATCH para desabilitar EPI retornou HTTP {response.status_code}."
    )

    verification = requests.get(writable_employee["url"], timeout=TIMEOUT)
    capture_api_evidence(
        verification,
        context={"Valor esperado de usesEpi": False},
    )
    assert verification.status_code == 200
    current_employee = verification.json()["state"]["employee"]
    assert current_employee.get("usesEpi") is False
