import tkinter as tk
from tkinter import messagebox
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from urllib.parse import quote

# Função para iniciar o Selenium com os dados inseridos
def iniciar_selenium():
    usuario_recebido = entrada_usuario.get()
    senha_recebida = entrada_senha.get()
    mensagem_dito = entrada_mensagem.get()

    if not usuario_recebido or not senha_recebida or not mensagem_dito:
        messagebox.showerror("Erro", "Por favor, preencha todos os campos.")
        return

    try:
        # Inicializar o driver do navegador
        driver = webdriver.Chrome()

        # Navegar até o site
        driver.get('https://pdv.dito.com.br/agenda')

        # Digitar o usuário e senha
        usuario = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//input[@id='user']")))
        usuario.send_keys(usuario_recebido)
        senha = driver.find_element(By.XPATH, "//input[@id='password']")
        senha.send_keys(senha_recebida)

        # Clicar em entrar
        botao_entrar = driver.find_element(By.XPATH, "//button[@id='dito-btn-login']")
        botao_entrar.click()
        sleep(10)

        while len(driver.find_elements(By.XPATH, "//header[@class='sc-kmQMED UPiIs campaign-header']")) >= 1:
            # Esperar até que a primeira campanha esteja disponível
            primeira_campanha = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//header[@class='sc-kmQMED UPiIs campaign-header']")))

            # Clicar na primeira campanha disponível
            primeira_campanha.click()

            # Esperar até que o primeiro cliente esteja disponível
            primeiro_cliente = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "(//div[@class='sc-bkbkJK iCahpR client-info'])[1]")))

            # Clicar no primeiro cliente disponível
            primeiro_cliente.click()

            # Copiar o nome do cliente
            elemento_nome_cliente = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//span[@class='sc-iqAclL dWlVKI']")))
            nome_cliente = elemento_nome_cliente.text
            lista_nome_cliente = nome_cliente.split()
            cliente = lista_nome_cliente[0]
            # Copiar o número do celular do cliente
            numero_cliente = driver.find_elements(By.XPATH, "//span[@class='sc-iqAclL dWlVKI']")[3].text
            numero_cliente_limpo = numero_cliente.replace("(", "").replace(")", "").replace(" ", "").replace("-", "").replace("+55", '')

            # Adicionar o código do país
            numero_cliente_internacional = "+55" + numero_cliente_limpo

            # Clicar para enviar para o cliente para validar o contato realizado
            botao_whatsapp = driver.find_element(By.XPATH, "//button[@class='ant-btn ant-btn-default sc-bBjRSN sc-JkixQ iTrhWF fgCFSm contact-wpp contact-wpp']")
            botao_whatsapp.click()

            # Esperar até que o botão de envio da campanha esteja disponível
            botao_enviar_campanha = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//button[@id='campaignCard-confirmButton']")))
            botao_enviar_campanha.click()
            sleep(1)
            driver.switch_to.window(driver.window_handles[1])
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
            sleep(1)
            driver.execute_script("window.open('');")
            driver.switch_to.window(driver.window_handles[1])
            mensagem_dito_encoded = quote(mensagem_dito)

            url_whatsapp = f'https://web.whatsapp.com/send?phone={numero_cliente_internacional}&text=Olá {cliente}, Tudo bem? {mensagem_dito_encoded}'
            driver.get(f'{url_whatsapp}')

            # Ir para a página do WhatsApp Web
            # Esperar até que a caixa de mensagem do WhatsApp esteja disponível
            while len(driver.find_elements(By.XPATH, "//div[@id='pane-side']")) < 1:
                sleep(1)
            try:
                botao_enviar_mensagem = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//button[@aria-label='Enviar']" or "//span[@data-icon='send']" or "//div[@class='_ak1t _ak1u']")))
                sleep(1)
                botao_confirmar_enviar_mensagem = driver.find_element(By.XPATH, "//button[@aria-label='Enviar']" or "//span[@data-icon='send']" or "//div[@class='_ak1t _ak1u']")
                botao_confirmar_enviar_mensagem.click()
                sleep(1)
                # Voltar ao site

                driver.close()
                driver.switch_to.window(driver.window_handles[0])
                confirmar_contato_realizado = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//button[@class='ant-btn ant-btn-default ant-btn-block sc-bBjRSN fyJzxp feedback-done feedback-done']")))
                confirmar_contato_realizado.click()
                sleep(2)
            except:
                botao_cliente_invalido = driver.find_element(By.XPATH, "//button[@class='x889kno x1a8lsjc xbbxn1n xxbr6pl x1n2onr6 x1rg5ohu xk50ysn x1f6kntn xyesn5m x1z11no5 xjy5m1g x1mnwbp6 x4pb5v6 x178xt8z xm81vs4 xso031l xy80clv x13fuv20 xu3j5b3 x1q0q8m5 x26u7qi x1v8p93f xogb00i x16stqrj x1ftr3km x1hl8ikr xfagghw x9dyr19 x9lcvmn xbtce8p x14v0smp xo8ufso xcjl5na x1k3x3db xuxw1ft xv52azi'][1]")
                driver.switch_to.window(driver.window_handles[1])
                driver.close()
                driver.switch_to.window(driver.window_handles[0])
                sleep(1)
                confirmar_contato_realizado = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//button[@class='ant-btn ant-btn-default ant-btn-block sc-bBjRSN fyJzxp feedback-done feedback-done']")))
                confirmar_contato_realizado.click()
                sleep(2)
            sleep(1)

        driver.quit()

    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro: {e}")

# Configurar a janela principal do Tkinter
janela = tk.Tk()
janela.title("Login DITO")

# Campo para o usuário
tk.Label(janela, text="Usuário DITO:").pack(pady=5)
entrada_usuario = tk.Entry(janela, width=30)
entrada_usuario.pack(pady=5)

# Campo para a senha
tk.Label(janela, text="Senha DITO:").pack(pady=5)
entrada_senha = tk.Entry(janela, show="*", width=30)
entrada_senha.pack(pady=5)

# Campo para a mensagem
tk.Label(janela, text="Mensagem a ser enviada:").pack(pady=5)
entrada_mensagem = tk.Entry(janela, width=30)
entrada_mensagem.pack(pady=5)

# Botão para iniciar o Selenium
botao_iniciar = tk.Button(janela, text="Iniciar", command=iniciar_selenium)
botao_iniciar.pack(pady=20)

# Iniciar o loop principal do Tkinter
janela.mainloop()
