from datetime import datetime
from selenium.common.exceptions import TimeoutException  # Importar TimeoutException
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from time import sleep
import os

from handle_listas import tranform_text_atribuicao

from google_sheets import main

USER_ACCOUNT = os.environ.get("USER_ACCOUNT")
PASS_ACCOUNT = os.environ.get("PASS_ACCOUNT")
UNID_ACCOUNT = os.environ.get("UNID_ACCOUNT")


def query(page, box_msg,
          numSei, etiqueta, msg, atribuicao, assunto, status, categoria, grava_reg_sei):

    def send_msg(msg):
        box_msg.content.value = msg
        page.update()

    send_msg("Iniciando a busca...")

    atribuicao = tranform_text_atribuicao(atribuicao)

    try:

        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        servico = Service(ChromeDriverManager().install(),
                          chrome_options=options)
        navegador = webdriver.Chrome(service=servico)
        navegador.implicitly_wait(10)

        url = "https://www.sei.mg.gov.br"
        navegador.get(url)

        # Insere a credencial de login
        navegador.find_element(By.ID, "txtUsuario").send_keys(USER_ACCOUNT)

        # Insere a Senha de login
        navegador.find_element(By.ID, "pwdSenha").send_keys(PASS_ACCOUNT)

        # Realiza o select cujo texto é "Selecione o Orgão"
        select_element = navegador.find_element(
            By.ID, "selOrgao"
        )
        # Crie um objeto Select com o elemento encontrado
        select = Select(select_element)

        # Selecione a opção pelo texto visível
        select.select_by_visible_text(UNID_ACCOUNT)

        # Clique no botão Acessar
        navegador.find_element(By.ID, "Acessar").click()

        ################# SEGUNDA PARTE #################

        send_msg("Login realizado com sucesso. Aguardando busca...")

        # Insira no campo perquisa de id=txtPesquisaRapida o valor que está na variavel numSei
        navegador.find_element(By.ID, "txtPesquisaRapida").send_keys(numSei)

        # Tecle Enter
        navegador.find_element(
            By.ID, "txtPesquisaRapida").send_keys(Keys.ENTER)

        navegador.switch_to.frame(1)

        # Clique no botão #divArvoreAcoes > a:nth-child(22)

        navegador.find_element(
            By.XPATH, '//*[@id="divArvoreAcoes"]/a[22]').click()

        navegador.find_element(
            By.XPATH, '//*[@id="btnAdicionar"]').click()

        # Esperar até que o dropdown esteja clicável e então clicar para expandir as opções
        dropdown = WebDriverWait(navegador, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".dd-select"))
        )
        dropdown.click()

        # Aguardar que as opções estejam visíveis
        opcoes = WebDriverWait(navegador, 10).until(
            EC.visibility_of_all_elements_located(
                (By.CSS_SELECTOR, ".dd-option-text"))
        )

        # Iterar sobre as opções e clicar naquela que corresponde ao texto alvo
        for opcao in opcoes:
            if opcao.text == etiqueta:
                opcao.click()
                break

        # Insere o conteudo de msg no campo de mensagens //*[@id="txaTexto"]
        navegador.find_element(By.XPATH, '//*[@id="txaTexto"]').send_keys(msg)

        # Clica atraves do XPATH no botão //*[@id="sbmSalvar"]
        navegador.find_element(By.XPATH, '//*[@id="sbmSalvar"]').click()

        send_msg("Despacho realizado com sucesso. Aguardando atribuição...")

        # Atualiza a pagina
        navegador.refresh()

        navegador.switch_to.frame(1)

        # Faz um click no botao XPATH //*[@id="divArvoreAcoes"]/a[8]
        navegador.find_element(
            By.XPATH, '//*[@id="divArvoreAcoes"]/a[8]').click()

        # Script JavaScript para selecionar a opção pelo texto
        script = f"""
        var atribuicao = "{atribuicao}";
        var selectElement = document.querySelector("#selAtribuicao");
        for (var i = 0; i < selectElement.options.length; i++) {{
            if (selectElement.options[i].text === atribuicao) {{
                selectElement.selectedIndex = i;
                selectElement.dispatchEvent(new Event('change'));
                break;
            }}
        }}
        """
        # Executar o script
        navegador.execute_script(script)

        # Clica no botao de XPATH //*[@id="sbmSalvar"]
        navegador.find_element(By.XPATH, '//*[@id="sbmSalvar"]').click()

        sleep(1)

        send_msg(
            "Atribuição realizada com sucesso. Aguardando registro em controle sei...")
        if grava_reg_sei == "Sim":
            main([numSei, "", "", assunto, status, categoria, "Cap Cleyton"])

            send_msg(
                "Registro em controle sei realizado com sucesso. Todas as etapas foram cocluidas!!")
        else:
            send_msg(
                "Registro em controle sei não foi gravado. Todas as etapas foram cocluidas!!")

        sleep(1)

    except Exception as e:
        box_msg.content.color = "red"

        send_msg(f"Erro: {e}")


if __name__ == "__main__":
    query()
