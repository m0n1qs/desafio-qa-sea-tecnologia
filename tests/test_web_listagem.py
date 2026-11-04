import re

import pytest
import requests
from playwright.sync_api import expect


@pytest.mark.web
@pytest.mark.automatizado
def test_CT017_identificar_trabalhadores_ativos_e_inativos(
    page,
    base_url,
    capture_screenshot,
):
    page.goto(base_url, wait_until="domcontentloaded")
    active_filter = page.get_by_role(
        "button",
        name=re.compile("Ver apenas ativos", re.I),
    )

    active_filter.click()
    capture_screenshot(page, "filtro-de-ativos-aplicado")
    expect(active_filter).to_have_class(re.compile("isActive"))

    page.get_by_role("button", name=re.compile("Limpar filtros", re.I)).click()
    capture_screenshot(page, "filtros-limpos")
    expect(active_filter).not_to_have_class(re.compile("isActive"))
