from playwright.sync_api import sync_playwright, expect

def run_verification():
    """
    Launches a browser, navigates to the dashboard, and takes a screenshot.
    """
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        try:
            # Navegar a la URL del dashboard
            page.goto("http://127.0.0.1:8057/", timeout=30000)

            # Esperar a que el título principal sea visible, lo que indica que la página se cargó
            expect(page.get_by_role("heading", name="Dashboard de Competitividad de Casanare")).to_be_visible(timeout=15000)

            # Esperar a que al menos uno de los gráficos de Plotly se cargue
            # Buscamos un div con la clase 'dash-graph', que es un contenedor de gráficos de Dash
            page.wait_for_selector("div.dash-graph", state="visible", timeout=15000)

            # Dar un tiempo extra para que los gráficos terminen de renderizarse dentro de los iframes
            page.wait_for_timeout(3000)

            # Tomar la captura de pantalla de la página completa
            screenshot_path = "jules-scratch/verification/dashboard_view.png"
            page.screenshot(path=screenshot_path, full_page=True)

            print(f"Screenshot saved to {screenshot_path}")

        except Exception as e:
            print(f"An error occurred during verification: {e}")

        finally:
            browser.close()

if __name__ == "__main__":
    run_verification()