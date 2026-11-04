from datetime import date, timedelta
from email import message
import re

import pytest
import requests
from playwright.sync_api import expect


def preencher_dados_basicos(page, dados):
    page.locator('input[name="name"]').fill(dados["name"])
    page.locator('input[name="cpf"]').fill(dados["cpf"])
    page.locator('input[name="birthDay"]').fill(dados["birth_day"])
    page.locator('input[name="rg"]').fill(dados["rg"])
    page.locator('input[name="caNumber"]').fill(dados["ca_number"])


def salvar_cadastro(page, nome):
    page.get_by_role("button", name=re.compile("Salvar", re.I)).click()
    expect(page.locator("body")).to_contain_text(nome)


def consultar_cadastro(api_url, nome):
    response = requests.get(api_url, timeout=15)
    assert response.status_code == 200
    return next(
        (
            employee.get("state", {}).get("employee", {})
            for employee in response.json()
            if employee.get("state", {}).get("employee", {}).get("name") == nome
        ),
        None,
    )


@pytest.mark.automatizado
def test_CT001_exibir_campos_do_cadastro(cadastro_form, capture_screenshot):
    for field in ("name", "cpf", "birthDay", "rg", "caNumber"):
        expect(cadastro_form.locator(f'input[name="{field}"]')).to_be_visible()

    expect(cadastro_form.locator(".ant-select")).to_have_count(3)
    expect(cadastro_form.locator('input[type="file"]')).to_have_count(1)

    capture_screenshot(
        cadastro_form,
        "01-formulario-completo",
        full_page=True,
    )

    cadastro_form.evaluate(
        "window.scrollTo(0, document.documentElement.scrollHeight)"
    )
    cadastro_form.wait_for_function(
        "window.scrollY + window.innerHeight >= "
        "Math.max(document.documentElement.scrollHeight, document.body.scrollHeight)"
    )
    capture_screenshot(cadastro_form, "02-final-da-pagina")



@pytest.mark.automatizado
def test_CT002_validar_campos_obrigatorios(cadastro_form, capture_screenshot):
    required_fields = cadastro_form.locator("input[required]")
    assert required_fields.count() >= 5

    for index in range(required_fields.count()):
        assert not required_fields.nth(index).evaluate(
            "(element) => element.checkValidity()"
        )

    cadastro_form.get_by_role("button", name=re.compile("Salvar", re.I)).click()
    capture_screenshot(cadastro_form, "mensagem-campos-obrigatorios")

@pytest.mark.automatizado
def test_CT003_rejeitar_CPF_invalido(
    cadastro_form,
    capture_screenshot,
):
    capture_screenshot(cadastro_form, "inicio-do-cenario")

    cadastro_form.locator('input[name="name"]').fill("Teste automatizado")
    cpf = cadastro_form.locator('input[name="cpf"]')
    cpf.fill("cpf123")
    assert cpf.evaluate("(element) => element.validity.tooShort")

    cadastro_form.get_by_role("button", name=re.compile("Salvar", re.I)).click()
    expect(cpf).to_be_focused()
    capture_screenshot(cadastro_form, "cpf-inválido-rejeitado")


@pytest.mark.automatizado
def test_CT005_validar_data_de_nascimento_inválida(
    worker_test_data,
    cadastro_form,
    capture_screenshot,
):
    capture_screenshot(cadastro_form, "inicio-do-cenario")
    preencher_dados_basicos(cadastro_form, worker_test_data)
    birth_day = cadastro_form.locator('input[name="birthDay"]')
    birth_day.fill("0001-01-01")
    capture_screenshot(cadastro_form, "data-invalida-inserida")

    cadastro_form.get_by_role("button", name=re.compile("Salvar", re.I)).click()
    name_field = cadastro_form.locator('input[name="name"]')
    if not name_field.is_visible():
        message = (
            "Falha: o sistema permitiu cadastrar trabalhador com "
            "data de nascimento inválida (01/01/0001)."
        )
        cadastro_form.evaluate(
            """(message) => {
                const notice = document.createElement("div");
                notice.textContent = message;
                notice.style.cssText = [
                    "position:fixed",
                    "top:16px",
                    "left:50%",
                    "transform:translateX(-50%)",
                    "z-index:9999",
                    "padding:12px 20px",
                    "background:#f8d7da",
                    "color:#842029",
                    "border:1px solid #f5c2c7",
                    "border-radius:6px",
                    "font:16px sans-serif"
                ].join(";");
                document.body.appendChild(notice);
            }""",
            message,
        )
        capture_screenshot(cadastro_form, "data-invalida-aceita-pelo-sistema")
        pytest.fail(message)

    expect(name_field).to_be_visible()
    capture_screenshot(cadastro_form, "data-invalida-rejeitada")


@pytest.mark.automatizado
def test_CT006_validar_data_de_nascimento_futura(
    worker_test_data,
    cadastro_form,
    capture_screenshot,
):
    capture_screenshot(cadastro_form, "inicio-do-cenario")
    preencher_dados_basicos(cadastro_form, worker_test_data)
    birth_day = cadastro_form.locator('input[name="birthDay"]')
    future_date = (date.today() + timedelta(days=1)).isoformat()
    birth_day.fill(future_date)
    capture_screenshot(cadastro_form, "data-futura-inserida")

    cadastro_form.get_by_role("button", name=re.compile("Salvar", re.I)).click()
    name_field = cadastro_form.locator('input[name="name"]')
    if not name_field.is_visible():
        message = (
            "Falha: o sistema permitiu cadastrar trabalhador com "
            "data de nascimento futura."
        )
        cadastro_form.evaluate(
            """(message) => {
                const notice = document.createElement("div");
                notice.textContent = message;
                notice.style.cssText = [
                    "position:fixed",
                    "top:16px",
                    "left:50%",
                    "transform:translateX(-50%)",
                    "z-index:9999",
                    "padding:12px 20px",
                    "background:#f8d7da",
                    "color:#842029",
                    "border:1px solid #f5c2c7",
                    "border-radius:6px",
                    "font:16px sans-serif"
                ].join(";");
                document.body.appendChild(notice);
            }""",
            message,
        )
        capture_screenshot(cadastro_form, "data-futura-aceita-pelo-sistema")
        pytest.fail(message)

    expect(name_field).to_be_visible()
    capture_screenshot(cadastro_form, "data-futura-rejeitada")



@pytest.mark.automatizado
def test_CT007_cadastrar_trabalhador_ativo(
    worker_test_data,
    cadastro_form,
    api_url,
    capture_screenshot,
):
    capture_screenshot(cadastro_form, "trabalhador-ativo-cadastro")
    preencher_dados_basicos(cadastro_form, worker_test_data)
    status = cadastro_form.get_by_role("switch")
    if status.get_attribute("aria-checked") != "true":
        status.click()
    capture_screenshot(cadastro_form, "formulario-preenchido-antes-salvar")
    cadastro_form.get_by_role("button", name=re.compile("Salvar", re.I)).click()
    expect(
        cadastro_form.get_by_role(
            "button",
            name=re.compile("Adicionar Funcionário", re.I),
        )
    ).to_be_visible()
    saved_worker = consultar_cadastro(api_url, worker_test_data["name"])
    assert saved_worker is not None
    assert saved_worker.get("isActive") is True
    cadastro_form.reload(wait_until="domcontentloaded")
    active_filter = cadastro_form.get_by_role(
        "button",
        name=re.compile("Ver apenas ativos", re.I),
    )
    active_filter.click()
    expect(active_filter).to_have_class(re.compile("isActive"))
    expect(
        cadastro_form.get_by_text(worker_test_data["name"], exact=True)
    ).to_have_count(1)
    verification_message = (
        f"Verificação da API: trabalhador '{worker_test_data['name']}' "
        "encontrado com status Ativo (isActive=True)."
    )
    cadastro_form.evaluate(
        """(message) => {
            const notice = document.createElement("div");
            notice.textContent = message;
            notice.style.cssText = [
                "position:fixed",
                "top:16px",
                "left:50%",
                "transform:translateX(-50%)",
                "z-index:9999",
                "padding:12px 20px",
                "background:#d1e7dd",
                "color:#0f5132",
                "border:1px solid #badbcc",
                "border-radius:6px",
                "font:16px sans-serif"
            ].join(";");
            document.body.appendChild(notice);
        }""",
        verification_message,
    )
    expect(cadastro_form.get_by_text(verification_message, exact=True)).to_be_visible()
    capture_screenshot(cadastro_form, "verificacao-api-trabalhador-ativo")



@pytest.mark.automatizado
def test_CT008_cadastrar_trabalhador_inativo(
    worker_test_data,
    cadastro_form,
    api_url,
    capture_screenshot,
):
    capture_screenshot(cadastro_form, "trabalhador-inativo-cadastro")
    preencher_dados_basicos(cadastro_form, worker_test_data)
    status = cadastro_form.get_by_role("switch")
    if status.get_attribute("aria-checked") != "false":
        status.click()
    capture_screenshot(cadastro_form, "formulario-inativo-preenchido-antes-salvar")
    cadastro_form.get_by_role("button", name=re.compile("Salvar", re.I)).click()
    expect(
        cadastro_form.get_by_role(
            "button",
            name=re.compile("Adicionar Funcionário", re.I),
        )
    ).to_be_visible()
    saved_worker = consultar_cadastro(api_url, worker_test_data["name"])
    assert saved_worker is not None
    assert saved_worker.get("isActive") is False
    cadastro_form.reload(wait_until="domcontentloaded")
    active_filter = cadastro_form.get_by_role(
        "button",
        name=re.compile("Ver apenas ativos", re.I),
    )
    active_filter.click()
    expect(active_filter).to_have_class(re.compile("isActive"))
    expect(
        cadastro_form.get_by_text(worker_test_data["name"], exact=True)
    ).to_have_count(0)
    capture_screenshot(cadastro_form, "inativo-ausente-do-filtro-ativos")
    cadastro_form.get_by_role("button", name=re.compile("Limpar filtros", re.I)).click()
    expect(active_filter).not_to_have_class(re.compile("isActive"))
    expect(
        cadastro_form.get_by_text(worker_test_data["name"], exact=True)
    ).to_have_count(1)
    verification_message = (
        f"Verificação da API: trabalhador '{worker_test_data['name']}' "
        "encontrado com status Inativo (isActive=False)."
    )
    cadastro_form.evaluate(
        """(message) => {
            const notice = document.createElement("div");
            notice.textContent = message;
            notice.style.cssText = [
                "position:fixed",
                "top:16px",
                "left:50%",
                "transform:translateX(-50%)",
                "z-index:9999",
                "padding:12px 20px",
                "background:#d1e7dd",
                "color:#0f5132",
                "border:1px solid #badbcc",
                "border-radius:6px",
                "font:16px sans-serif"
            ].join(";");
            document.body.appendChild(notice);
        }""",
        verification_message,
    )
    expect(cadastro_form.get_by_text(verification_message, exact=True)).to_be_visible()
    capture_screenshot(cadastro_form, "verificacao-api-trabalhador-inativo")


@pytest.mark.automatizado
def test_CT012_marcar_trabalhador_sem_EPI(
    worker_test_data,
    cadastro_form,
    api_url,
    capture_screenshot,
):
    cadastro_form.locator('input[name="name"]').fill(worker_test_data["name"])
    cadastro_form.locator('input[name="cpf"]').fill(worker_test_data["cpf"])
    cadastro_form.locator('input[name="birthDay"]').fill(
        worker_test_data["birth_day"]
    )
    cadastro_form.locator('input[name="rg"]').fill(worker_test_data["rg"])
    assert cadastro_form.locator("input[type=search]").count() == 3
    cadastro_form.locator('input[type="checkbox"]').check()
    capture_screenshot(cadastro_form, "opcao-sem-epi-selecionada")
    expect(cadastro_form.locator("input[type=search]")).to_have_count(1)

    cadastro_form.get_by_role("button", name=re.compile("Salvar", re.I)).click()
    expect(
        cadastro_form.get_by_role(
            "button",
            name=re.compile("Adicionar Funcionário", re.I),
        )
    ).to_be_visible()
    saved_worker = consultar_cadastro(api_url, worker_test_data["name"]    )
    assert saved_worker is not None
    uses_epi = saved_worker.get("usesEpi")
    verification_message = (
        f"Verificação da API: trabalhador '{worker_test_data['name']}' "
        f"encontrado; usesEpi={uses_epi}."
    )
    cadastro_form.evaluate(
        """({message, usesEpi}) => {
            const notice = document.createElement("div");
            notice.textContent = message;
            notice.style.cssText = [
                "position:fixed",
                "top:16px",
                "left:50%",
                "transform:translateX(-50%)",
                "z-index:9999",
                "padding:12px 20px",
                `background:${usesEpi === false ? "#d1e7dd" : "#f8d7da"}`,
                `color:${usesEpi === false ? "#0f5132" : "#842029"}`,
                `border:1px solid ${usesEpi === false ? "#badbcc" : "#f5c2c7"}`,
                "border-radius:6px",
                "font:16px sans-serif"
            ].join(";");
            document.body.appendChild(notice);
        }""",
        {"message": verification_message, "usesEpi": uses_epi},
    )
    expect(cadastro_form.get_by_text(verification_message, exact=True)).to_be_visible()
    capture_screenshot(cadastro_form, "verificacao-api-trabalhador-sem-epi")
    assert uses_epi is False, (
        "O cadastro foi encontrado, mas a API informa usesEpi=True "
        "mesmo com a opção 'O trabalhador não usa EPI' marcada."
    )


@pytest.mark.automatizado
def test_CT013_impedir_EPI_sem_CA(
    worker_test_data,
    cadastro_form,
    capture_screenshot,
):
    preencher_dados_basicos(cadastro_form, worker_test_data)
    ca_number = cadastro_form.locator('input[name="caNumber"]')
    ca_number.fill("")

    assert ca_number.get_attribute("required") is not None
    assert not ca_number.evaluate("(element) => element.checkValidity()")

    capture_screenshot(cadastro_form, "ca-obrigatorio-vazio-antes-salvar")
    cadastro_form.get_by_role("button", name=re.compile("Salvar", re.I)).click()

    expect(ca_number).to_be_focused()
    assert not ca_number.evaluate("(element) => element.checkValidity()")
    capture_screenshot(cadastro_form, "cadastro-bloqueado-sem-ca")


@pytest.mark.automatizado
def test_CT015_adicionar_atividade_sem_perder_dados(
    worker_test_data,
    cadastro_form,
    capture_screenshot,
):
    preencher_dados_basicos(cadastro_form, worker_test_data)
    first_ca = cadastro_form.locator('input[name="caNumber"]').first
    original_ca = first_ca.input_value()
    first_activity = cadastro_form.locator(
        ".ant-select-selection-item"
    ).nth(1).inner_text()
    capture_screenshot(cadastro_form, "atividade-original-preenchida")
    add_activity_button = cadastro_form.get_by_role(
        "button",
        name=re.compile("Adicionar outra atividade", re.I),
    )
    add_activity_button.scroll_into_view_if_needed()
    capture_screenshot(cadastro_form, "botao-adicionar-outra-atividade")
    add_activity_button.click()
    capture_screenshot(cadastro_form, "segunda-atividade-adicionada")
    expect(cadastro_form.locator('input[name="caNumber"]').nth(0)).to_have_value(
        original_ca
    )
    expect(cadastro_form.locator(".ant-select-selection-item").nth(1)).to_have_text(
        first_activity
    )
    capture_screenshot(cadastro_form, "primeira-atividade-preservada")
