import cv2
import numpy as np
import pyautogui
import time
import threading

# Carregar os templates
template_comfey = cv2.imread('images/card.png', 0)
height_comfey, width_comfey = template_comfey.shape[:2]

template_sintese_aprender = cv2.imread('images/habilidade-sintese-aprender.png', 0)
height_sintese_aprender, width_sintese_aprender = template_sintese_aprender.shape[:2]

template_sintese_usar = cv2.imread('images/habilidade-sintese-usar.png', 0)
height_sintese_usar, width_sintese_usar = template_sintese_usar.shape[:2]

template_sintese_curar = cv2.imread('images/habilidade-sintese-curar.png', 0)
height_sintese_curar, width_sintese_curar = template_sintese_curar.shape[:2]

template_chicote_aprender = cv2.imread('images/habilidade-chicote-de-vinha-aprender.png', 0)
height_chicote_aprender, width_chicote_aprender = template_chicote_aprender.shape[:2]

template_chicote_usar = cv2.imread('images/habilidade-chicote-de-vinha-usar.png', 0)
height_chicote_usar, width_chicote_usar = template_chicote_usar.shape[:2]

template_cura_aprender = cv2.imread('images/habilidade-cura-das-flores-aprender.png', 0)
height_cura_aprender, width_cura_aprender = template_cura_aprender.shape[:2]

template_cura_usar = cv2.imread('images/habilidade-cura-das-flores-usar.png', 0)
height_cura_usar, width_cura_usar = template_cura_usar.shape[:2]

template_folha_magica_aprender = cv2.imread('images/habilidade-folha-magica-aprender.png', 0)
height_folha_magica_aprender, width_folha_magica_aprender = template_folha_magica_aprender.shape[:2]

template_folha_magica_usar = cv2.imread('images/habilidade-folha-magica-usar.png', 0)
height_folha_magica_usar, width_folha_magica_usar = template_folha_magica_usar.shape[:2]

template_unite_aprender = cv2.imread('images/habilidade-unite-aprender.png', 0)
height_unite_aprender, width_unite_aprender = template_unite_aprender.shape[:2]

template_unite_usar = cv2.imread('images/habilidade-unite-usar.png', 0)
height_unite_usar, width_unite_usar = template_unite_usar.shape[:2]

template_cura_plus_aprender = cv2.imread('images/habilidade-cura-das-flores-plus-aprender.png', 0)
height_cura_plus_aprender, width_cura_plus_aprender = template_cura_plus_aprender.shape[:2]

template_cura_plus_usar = cv2.imread('images/habilidade-cura-das-flores-plus-usar.png', 0)
height_cura_plus_usar, width_cura_plus_usar = template_cura_plus_usar.shape[:2]

template_folha_magica_plus_aprender = cv2.imread('images/habilidade-folha-magica-plus-aprender.png', 0)
height_folha_magica_plus_aprender, width_folha_magica_plus_aprender = template_folha_magica_plus_aprender.shape[:2]

template_folha_magica_plus_usar = cv2.imread('images/habilidade-folha-magica-plus-usar.png', 0)
height_folha_magica_plus_usar, width_folha_magica_plus_usar = template_folha_magica_plus_usar.shape[:2]

template_pause = cv2.imread('images/pause.png', 0)
height_pause, width_pause = template_pause.shape[:2]

template_toque_continuar1 = cv2.imread('images/toque-para-continuar1.png', 0)
height_toque_continuar1, width_toque_continuar1 = template_toque_continuar1.shape[:2]

template_toque_continuar2 = cv2.imread('images/toque-para-continuar2.png', 0)
height_toque_continuar2, width_toque_continuar2 = template_toque_continuar2.shape[:2]

template_fechar = cv2.imread('images/fechar.png', 0)
height_fechar, width_fechar = template_fechar.shape[:2]

template_proximo = cv2.imread('proximo.png')
height_proximo, width_proximo = template_proximo.shape[:2]

# Novos templates
template_cura_das_flores_curar = cv2.imread('images/habilidade-cura-das-flores-curar.png', 0)
height_cura_das_flores_curar, width_cura_das_flores_curar = template_cura_das_flores_curar.shape[:2]

template_cura_das_flores_ult_curar = cv2.imread('images/habilidade-cura-das-flores-ult-curar.png', 0)
height_cura_das_flores_ult_curar, width_cura_das_flores_ult_curar = template_cura_das_flores_ult_curar.shape[:2]

template_cura_das_flores_curar_plus = cv2.imread('images/habilidade-cura-das-flores-curar-plus.png', 0)
height_cura_das_flores_curar_plus, width_cura_das_flores_curar_plus = template_cura_das_flores_curar_plus.shape[:2]

template_cura_das_flores_ult_curar_plus = cv2.imread('images/habilidade-cura-das-flores-ult-curar-plus.png', 0)
height_cura_das_flores_ult_curar_plus, width_cura_das_flores_ult_curar_plus = template_cura_das_flores_ult_curar_plus.shape[:2]

template_aceitar = cv2.imread('images/aceitar.png', 0)
height_aceitar, width_aceitar = template_aceitar.shape[:2]

template_comecar = cv2.imread('images/comecar.png', 0)
height_comecar, width_comecar = template_comecar.shape[:2]

template_pronto = cv2.imread('images/pronto.png', 0)
height_pronto, width_pronto = template_pronto.shape[:2]

template_item = cv2.imread('images/item.png', 0)
height_item, width_item = template_item.shape[:2]

template_lobby = cv2.imread('images/lobby.png', 0)
height_lobby, width_lobby = template_lobby.shape[:2]

# Definir um limite de correspondência
threshold = 0.8

# Definir intervalo entre cliques (em segundos)
click_interval = 0.1

# Flag para indicar se o script está em pausa
is_paused = False

def find_and_click(template, height, width, message, click_forever=False, force_click=False):
    while True:
        if is_paused and not force_click:
            time.sleep(0.1)  # Aguarda 1 segundo enquanto está pausado
            continue

        screen_width, screen_height = pyautogui.size()  # Obtém a resolução da tela
        screenshot = pyautogui.screenshot(region=(0, 0, screen_width, screen_height))
        image = np.array(screenshot)
        image_bgr = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        image_gray = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2GRAY)
        result = cv2.matchTemplate(image_gray, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        print(f"Max val for {message}: {max_val}")  # Printar o valor máximo de correspondência para diagnóstico

        if max_val >= threshold:
            center_x = max_loc[0] + width // 2
            center_y = max_loc[1] + height // 2
            print(f"Encontrado! Clicando na posição: ({center_x}, {center_y})")
            pyautogui.moveTo(center_x, center_y)
            pyautogui.click()
            time.sleep(0.1)  # Aguarda 0.1 segundos para garantir o clique

            if click_forever:
                time.sleep(click_interval)  # Aguarda meio segundo antes de procurar novamente
            else:
                return True  # Retorna verdadeiro quando encontra e clica
        else:
            print(f"Imagem não encontrada: {message}")
        time.sleep(0.1)  # Aguarda 1 segundo antes de tentar novamente

def monitor_pause():
    global is_paused
    while True:
        screen_width, screen_height = pyautogui.size()
        screenshot = pyautogui.screenshot(region=(0, 0, screen_width, screen_height))
        image = np.array(screenshot)
        image_bgr = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        image_gray = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2GRAY)
        result = cv2.matchTemplate(image_gray, template_pause, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        if max_val >= threshold:
            print("Pause encontrado! Pausando...")
            is_paused = True
            time.sleep(3)  # Pausa por 3 segundos
            is_paused = False
        time.sleep(0.1)  # Aguarda 1 segundo antes de verificar novamente

def start_comfey_thread():
    while True:
        find_and_click(template_comfey, height_comfey, width_comfey, "Comfey encontrado!", click_forever=True)

def start_toque_continuar1_thread():
    while True:
        find_and_click(template_toque_continuar1, height_toque_continuar1, width_toque_continuar1, "Toque para Continuar 1 clicado!", click_forever=True)

def start_toque_continuar2_thread():
    while True:
        find_and_click(template_toque_continuar2, height_toque_continuar2, width_toque_continuar2, "Toque para Continuar 2 clicado!", click_forever=True)

def start_fechar_thread():
    while True:
        find_and_click(template_fechar, height_fechar, width_fechar, "Fechar clicado!", click_forever=True)

def start_sintese_aprender_thread():
    while True:
        if not is_paused:
            find_and_click(template_sintese_aprender, height_sintese_aprender, width_sintese_aprender, "Habilidade Síntese aprendida!")

def start_sintese_usar_thread():
    while True:
        if not is_paused:
            find_and_click(template_sintese_usar, height_sintese_usar, width_sintese_usar, "Habilidade Síntese utilizada a cada meio segundo!", click_forever=True)

def start_sintese_curar_thread():
    while True:
        if not is_paused:
            find_and_click(template_sintese_curar, height_sintese_curar, width_sintese_curar, "Habilidade Síntese Curar usada!", click_forever=True)

def start_chicote_aprender_thread():
    while True:
        if not is_paused:
            find_and_click(template_chicote_aprender, height_chicote_aprender, width_chicote_aprender, "Habilidade Chicote de Vinha aprendida!")

def start_chicote_usar_thread():
    while True:
        if not is_paused:
            find_and_click(template_chicote_usar, height_chicote_usar, width_chicote_usar, "Habilidade Chicote de Vinha utilizada a cada meio segundo!", click_forever=True)

def start_cura_aprender_thread():
    while True:
        if not is_paused:
            find_and_click(template_cura_aprender, height_cura_aprender, width_cura_aprender, "Habilidade Cura das Flores aprendida!")

def start_cura_usar_thread():
    while True:
        if not is_paused:
            find_and_click(template_cura_usar, height_cura_usar, width_cura_usar, "Habilidade Cura das Flores utilizada a cada meio segundo!", click_forever=True)

def start_folha_magica_aprender_thread():
    while True:
        if not is_paused:
            find_and_click(template_folha_magica_aprender, height_folha_magica_aprender, width_folha_magica_aprender, "Habilidade Folha Mágica aprendida!")

def start_folha_magica_usar_thread():
    while True:
        if not is_paused:
            find_and_click(template_folha_magica_usar, height_folha_magica_usar, width_folha_magica_usar, "Habilidade Folha Mágica utilizada a cada meio segundo!", click_forever=True)

def start_unite_aprender_thread():
    while True:
        if not is_paused:
            find_and_click(template_unite_aprender, height_unite_aprender, width_unite_aprender, "Habilidade Unite aprendida!")

def start_unite_usar_thread():
    while True:
        if not is_paused:
            find_and_click(template_unite_usar, height_unite_usar, width_unite_usar, "Habilidade Unite utilizada a cada meio segundo!", click_forever=True)

def start_cura_plus_aprender_thread():
    while True:
        if not is_paused:
            find_and_click(template_cura_plus_aprender, height_cura_plus_aprender, width_cura_plus_aprender, "Habilidade Cura das Flores Plus aprendida!")

def start_cura_plus_usar_thread():
    while True:
        if not is_paused:
            find_and_click(template_cura_plus_usar, height_cura_plus_usar, width_cura_plus_usar, "Habilidade Cura das Flores Plus utilizada a cada meio segundo!", click_forever=True)

def start_folha_magica_plus_aprender_thread():
    while True:
        if not is_paused:
            find_and_click(template_folha_magica_plus_aprender, height_folha_magica_plus_aprender, width_folha_magica_plus_aprender, "Habilidade Folha Mágica Plus aprendida!")

def start_folha_magica_plus_usar_thread():
    while True:
        if not is_paused:
            find_and_click(template_folha_magica_plus_usar, height_folha_magica_plus_usar, width_folha_magica_plus_usar, "Habilidade Folha Mágica Plus utilizada a cada meio segundo!", click_forever=True)

# Funções novas
def start_cura_das_flores_curar_thread():
    while True:
        if not is_paused:
            find_and_click(template_cura_das_flores_curar, height_cura_das_flores_curar, width_cura_das_flores_curar, "Habilidade Cura das Flores Curar usada!")

def start_cura_das_flores_ult_curar_thread():
    while True:
        if not is_paused:
            find_and_click(template_cura_das_flores_ult_curar, height_cura_das_flores_ult_curar, width_cura_das_flores_ult_curar, "Habilidade Cura das Flores Ult Curar usada!")

def start_cura_das_flores_curar_plus_thread():
    while True:
        if not is_paused:
            find_and_click(template_cura_das_flores_curar_plus, height_cura_das_flores_curar_plus, width_cura_das_flores_curar_plus, "Habilidade Cura das Flores Curar Plus usada!")

def start_cura_das_flores_ult_curar_plus_thread():
    while True:
        if not is_paused:
            find_and_click(template_cura_das_flores_ult_curar_plus, height_cura_das_flores_ult_curar_plus, width_cura_das_flores_ult_curar_plus, "Habilidade Cura das Flores Ult Curar Plus usada!")

def start_aceitar_thread():
    while True:
        if not is_paused:
            find_and_click(template_aceitar, height_aceitar, width_aceitar, "Aceitar clicado!")

def start_comecar_thread():
    while True:
        if not is_paused:
            find_and_click(template_comecar, height_comecar, width_comecar, "Começar clicado!")

def start_pronto_thread():
    while True:
        if not is_paused:
            find_and_click(template_pronto, height_pronto, width_pronto, "Pronto clicado!")

def start_item_thread():
    while True:
        if not is_paused:
            find_and_click(template_item, height_item, width_item, "Item clicado!")

def start_lobby_thread():
    while True:
        if not is_paused:
            find_and_click(template_lobby, height_lobby, width_lobby, "Lobby clicado!")

def start_proximo_thread():
    while True:
        if not is_paused:
            find_and_click(template_proximo, height_proximo, width_proximo, "Próximo clicado!")            

# Iniciar threads
thread_comfey = threading.Thread(target=start_comfey_thread)
thread_toque_continuar1 = threading.Thread(target=start_toque_continuar1_thread)
thread_toque_continuar2 = threading.Thread(target=start_toque_continuar2_thread)
thread_fechar = threading.Thread(target=start_fechar_thread)
thread_sintese_aprender = threading.Thread(target=start_sintese_aprender_thread)
thread_sintese_usar = threading.Thread(target=start_sintese_usar_thread)
thread_sintese_curar = threading.Thread(target=start_sintese_curar_thread)
thread_chicote_aprender = threading.Thread(target=start_chicote_aprender_thread)
thread_chicote_usar = threading.Thread(target=start_chicote_usar_thread)
thread_cura_aprender = threading.Thread(target=start_cura_aprender_thread)
thread_cura_usar = threading.Thread(target=start_cura_usar_thread)
thread_folha_magica_aprender = threading.Thread(target=start_folha_magica_aprender_thread)
thread_folha_magica_usar = threading.Thread(target=start_folha_magica_usar_thread)
thread_unite_aprender = threading.Thread(target=start_unite_aprender_thread)
thread_unite_usar = threading.Thread(target=start_unite_usar_thread)
thread_cura_plus_aprender = threading.Thread(target=start_cura_plus_aprender_thread)
thread_cura_plus_usar = threading.Thread(target=start_cura_plus_usar_thread)
thread_folha_magica_plus_aprender = threading.Thread(target=start_folha_magica_plus_aprender_thread)
thread_folha_magica_plus_usar = threading.Thread(target=start_folha_magica_plus_usar_thread)
thread_cura_das_flores_curar = threading.Thread(target=start_cura_das_flores_curar_thread)
thread_cura_das_flores_ult_curar = threading.Thread(target=start_cura_das_flores_ult_curar_thread)
thread_cura_das_flores_curar_plus = threading.Thread(target=start_cura_das_flores_curar_plus_thread)
thread_cura_das_flores_ult_curar_plus = threading.Thread(target=start_cura_das_flores_ult_curar_plus_thread)
thread_aceitar = threading.Thread(target=start_aceitar_thread)
thread_comecar = threading.Thread(target=start_comecar_thread)
thread_pronto = threading.Thread(target=start_pronto_thread)
thread_item = threading.Thread(target=start_item_thread)
thread_lobby = threading.Thread(target=start_lobby_thread)
thread_proximo = threading.Thread(target=start_proximo_thread)

thread_comfey.start()
thread_toque_continuar1.start()
thread_toque_continuar2.start()
thread_fechar.start()
thread_sintese_aprender.start()
thread_sintese_usar.start()
thread_sintese_curar.start()
thread_chicote_aprender.start()
thread_chicote_usar.start()
thread_cura_aprender.start()
thread_cura_usar.start()
thread_folha_magica_aprender.start()
thread_folha_magica_usar.start()
thread_unite_aprender.start()
thread_unite_usar.start()
thread_cura_plus_aprender.start()
thread_cura_plus_usar.start()
thread_folha_magica_plus_aprender.start()
thread_folha_magica_plus_usar.start()
thread_cura_das_flores_curar.start()
thread_cura_das_flores_ult_curar.start()
thread_cura_das_flores_curar_plus.start()
thread_cura_das_flores_ult_curar_plus.start()
thread_aceitar.start()
thread_comecar.start()
thread_pronto.start()
thread_item.start()
thread_lobby.start()
thread_proximo.start()


# Iniciar o monitoramento de pause.png
pause_thread = threading.Thread(target=monitor_pause)
pause_thread.start()

# Manter o script em execução
input("Pressione Enter para terminar o script...")
