import os
import sys
import time
import logging

import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)

# Functión para detectar cualquier tipo de alert y cerrarlos
def close_all_alerts(driver, timeout=5, max_wait_between_alerts=3, max_alerts=10):
    alert_count = 0

    while alert_count < max_alerts:
        try:
            WebDriverWait(driver, max_wait_between_alerts).until(EC.alert_is_present())
            alert = driver.switch_to.alert
            logging.info(f"Alerta #{alert_count + 1} detectada: {alert.text}")
            time.sleep(1)
            alert.accept()
            alert_count += 1
            logging.info(f"Alerta #{alert_count} cerrada.")
        except TimeoutException:
            logging.info(
                f"No se detectaron más alertas después de {alert_count} cierre(s)."
            )
            break

    if alert_count >= max_alerts:
        logging.warning(
            f"Se alcanzó el máximo de {max_alerts} alertas. Podría haber un bucle de alertas."
        )


# Función para configurar el navegador headless con todos los flags recomendados
def create_headless_driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--no-first-run")
    options.add_argument("--no-default-browser-check")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=options)
    return driver


# Instala automáticamente la versión correcta de ChromeDriver
chromedriver_autoinstaller.install()

# Leer la URL desde una variable de entorno
URL = os.getenv("TARGET_URL")

if not URL:
    raise ValueError("La variable de entorno 'TARGET_URL' no está definida.")

# Función principal que accede a la URL y verifica el contenido
def main():
    while True:
        try:
            driver = create_headless_driver()
            driver.get(URL)

            close_all_alerts(driver)

            logging.info(f"Accedido a {URL} exitosamente.")

            page_source = driver.page_source

            if "Function" in page_source:
                logging.info(
                    "Se encontró 'Function' en la página. Esperando 10 segundos antes de cerrar..."
                )
                time.sleep(10)
            else:
                logging.info("'Function' no encontrado. Cerrando inmediatamente.")

            driver.quit()

        except Exception as e:
            logging.error(f"Ocurrió un error: {e}")

        logging.info("Esperando 5 minutos antes de la próxima conexión...")
        time.sleep(300)  # 300 segundos = 5 minutos


if __name__ == "__main__":
    main()
