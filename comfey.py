import cv2
import numpy as np
import pyautogui
import time
import threading

# Carregar os templates
templates = {
    'comfey': 'images/card.png',
    'sintese_aprender': 'images/habilidade-sintese-aprender.png',
    'sintese_usar': 'images/habilidade-sintese-usar.png',
    'sintese_curar': 'images/habilidade-sintese-curar.png',
    'chicote_aprender': 'images/habilidade-chicote-de-vinha-aprender.png',
    'chicote_usar': 'images/habilidade-chicote-de-vinha-usar.png',
    'cura_aprender': 'images/habilidade-cura-das-flores-aprender.png',
    'cura_usar': 'images/habilidade-cura-das-flores-usar.png',
    'folha_magica_aprender': 'images/habilidade-folha-magica-aprender.png',
    'folha_magica_usar': 'images/habilidade-folha-magica-usar.png',
    'unite_aprender': 'images/habilidade-unite-aprender.png',
    'unite_usar': 'images/habilidade-unite-usar.png',
    'cura_plus_aprender': 'images/habilidade-cura-das-flores-plus-aprender.png',
    'cura_plus_usar': 'images/habilidade-cura-das-flores-plus-usar.png',
    'folha_magica_plus_aprender': 'images/habilidade-folha-magica-plus-aprender.png',
    'folha_magica_plus_usar': 'images/habilidade-folha-magica-plus-usar.png',
    'pause': 'images/pause.png',
    'toque_continuar1': 'images/toque-para-continuar1.png',
    'toque_continuar2': 'images/toque-para-continuar2.png',
    'fechar': 'images/fechar.png',
    'proximo': 'images/proximo.png',
    'cura_das_flores_curar': 'images/habilidade-cura-das-flores-curar.png',
    'cura_das_flores_ult_curar': 'images/habilidade-cura-das-flores-ult-curar.png',
    'cura_das_flores_curar_plus': 'images/habilidade-cura-das-flores-curar-plus.png',
    'cura_das_flores_ult_curar_plus': 'images/habilidade-cura-das-flores-ult-curar-plus.png',
    'aceitar': 'images/aceitar.png',
    'comecar': 'images/comecar.png',
    'pronto': 'images/pronto.png',
    'item': 'images/item.png',
    'lobby': 'images/lobby.png',
    'inicio': 'images/inicio.png'
}

# Carregar os templates e calcular suas dimensões
templates_data = {}
for name, path in templates.items():
    img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)  # Carregar como imagem em escala de cinza
    if img is not None:
        height, width = img.shape
        templates_data[name] = (img, height, width)
    else:
        print(f"Erro ao carregar a imagem para {name}")

# Definir um limite de correspondência
threshold = 0.8

# Definir intervalo entre cliques (em segundos)
click_interval = 0.1

# Flag para indicar se o script está em pausa
is_paused = False

# Flag para controlar o período de 10 segundos após pause.png
pause_mode_active = False
pause_mode_start_time = 0

def find_and_click(template_name, click_forever=False, force_click=False):
    global pause_mode_active, pause_mode_start_time

    if template_name not in templates_data:
        print(f"Template {template_name} não encontrado!")
        return

    template_img, height, width = templates_data[template_name]

    while True:
        if is_paused and not force_click:
            time.sleep(0.1)  # Aguarda 0.1 segundos enquanto está pausado
            continue

        if pause_mode_active and template_name not in ['sintese_aprender', 'sintese_usar']:
            time.sleep(0.1)  # Aguarda 0.1 segundos antes de tentar novamente
            continue

        screen_width, screen_height = pyautogui.size()  # Obtém a resolução da tela
        screenshot = pyautogui.screenshot(region=(0, 0, screen_width, screen_height))
        image = np.array(screenshot)
        image_gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        result = cv2.matchTemplate(image_gray, template_img, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

        print(f"Max val for {template_name}: {max_val}")  # Printar o valor máximo de correspondência para diagnóstico

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
            print(f"Imagem não encontrada: {template_name}")
        time.sleep(0.1)  # Aguarda 0.1 segundos antes de tentar novamente

def monitor_pause():
    global is_paused, pause_mode_active, pause_mode_start_time
    while True:
        if is_paused:
            time.sleep(0.1)  # Aguarda 0.1 segundos antes de verificar novamente
            continue

        screen_width, screen_height = pyautogui.size()
        screenshot = pyautogui.screenshot(region=(0, 0, screen_width, screen_height))
        image = np.array(screenshot)
        image_gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        template_img, _, _ = templates_data['pause']
        result = cv2.matchTemplate(image_gray, template_img, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

        if max_val >= threshold:
            print("Pause encontrado! Pausando...")
            is_paused = True
            pause_mode_active = True
            pause_mode_start_time = time.time()
            time.sleep(4)  # Pausa por 2 segundos
            is_paused = False
        time.sleep(0.1)  # Aguarda 0.1 segundos antes de verificar novamente

def start_thread(name, func, click_forever=False):
    while True:
        if not is_paused:
            func(name, click_forever)

# Definir funções de threads
def start_comfey_thread(): start_thread('comfey', find_and_click, click_forever=True)
def start_toque_continuar1_thread(): start_thread('toque_continuar1', find_and_click, click_forever=True)
def start_toque_continuar2_thread(): start_thread('toque_continuar2', find_and_click, click_forever=True)
def start_fechar_thread(): start_thread('fechar', find_and_click, click_forever=True)
def start_sintese_aprender_thread(): start_thread('sintese_aprender', find_and_click)
def start_sintese_usar_thread(): start_thread('sintese_usar', find_and_click, click_forever=True)
def start_sintese_curar_thread(): start_thread('sintese_curar', find_and_click, click_forever=True)
def start_chicote_aprender_thread(): start_thread('chicote_aprender', find_and_click)
def start_chicote_usar_thread(): start_thread('chicote_usar', find_and_click, click_forever=True)
def start_cura_aprender_thread(): start_thread('cura_aprender', find_and_click)
def start_cura_usar_thread(): start_thread('cura_usar', find_and_click, click_forever=True)
def start_folha_magica_aprender_thread(): start_thread('folha_magica_aprender', find_and_click)
def start_folha_magica_usar_thread(): start_thread('folha_magica_usar', find_and_click, click_forever=True)
def start_unite_aprender_thread(): start_thread('unite_aprender', find_and_click)
def start_unite_usar_thread(): start_thread('unite_usar', find_and_click, click_forever=True)
def start_cura_plus_aprender_thread(): start_thread('cura_plus_aprender', find_and_click)
def start_cura_plus_usar_thread(): start_thread('cura_plus_usar', find_and_click, click_forever=True)
def start_folha_magica_plus_aprender_thread(): start_thread('folha_magica_plus_aprender', find_and_click)
def start_folha_magica_plus_usar_thread(): start_thread('folha_magica_plus_usar', find_and_click, click_forever=True)
def start_cura_das_flores_curar_thread(): start_thread('cura_das_flores_curar', find_and_click)
def start_cura_das_flores_ult_curar_thread(): start_thread('cura_das_flores_ult_curar', find_and_click)
def start_cura_das_flores_curar_plus_thread(): start_thread('cura_das_flores_curar_plus', find_and_click)
def start_cura_das_flores_ult_curar_plus_thread(): start_thread('cura_das_flores_ult_curar_plus', find_and_click)
def start_aceitar_thread(): start_thread('aceitar', find_and_click)
def start_comecar_thread(): start_thread('comecar', find_and_click)
def start_pronto_thread(): start_thread('pronto', find_and_click)
def start_item_thread(): start_thread('item', find_and_click)
def start_lobby_thread(): start_thread('lobby', find_and_click)
def start_inicio_thread(): start_thread('inicio', find_and_click)
def start_proximo_thread(): start_thread('proximo', find_and_click)

# Iniciar as threads para cada habilidade
threading.Thread(target=start_comfey_thread, daemon=True).start()
threading.Thread(target=start_toque_continuar1_thread, daemon=True).start()
threading.Thread(target=start_toque_continuar2_thread, daemon=True).start()
threading.Thread(target=start_fechar_thread, daemon=True).start()
threading.Thread(target=start_sintese_aprender_thread, daemon=True).start()
threading.Thread(target=start_sintese_usar_thread, daemon=True).start()
threading.Thread(target=start_sintese_curar_thread, daemon=True).start()
threading.Thread(target=start_chicote_aprender_thread, daemon=True).start()
threading.Thread(target=start_chicote_usar_thread, daemon=True).start()
threading.Thread(target=start_cura_aprender_thread, daemon=True).start()
threading.Thread(target=start_cura_usar_thread, daemon=True).start()
threading.Thread(target=start_folha_magica_aprender_thread, daemon=True).start()
threading.Thread(target=start_folha_magica_usar_thread, daemon=True).start()
threading.Thread(target=start_unite_aprender_thread, daemon=True).start()
threading.Thread(target=start_unite_usar_thread, daemon=True).start()
threading.Thread(target=start_cura_plus_aprender_thread, daemon=True).start()
threading.Thread(target=start_cura_plus_usar_thread, daemon=True).start()
threading.Thread(target=start_folha_magica_plus_aprender_thread, daemon=True).start()
threading.Thread(target=start_folha_magica_plus_usar_thread, daemon=True).start()
threading.Thread(target=start_cura_das_flores_curar_thread, daemon=True).start()
threading.Thread(target=start_cura_das_flores_ult_curar_thread, daemon=True).start()
threading.Thread(target=start_cura_das_flores_curar_plus_thread, daemon=True).start()
threading.Thread(target=start_cura_das_flores_ult_curar_plus_thread, daemon=True).start()
threading.Thread(target=start_aceitar_thread, daemon=True).start()
threading.Thread(target=start_comecar_thread, daemon=True).start()
threading.Thread(target=start_pronto_thread, daemon=True).start()
threading.Thread(target=start_item_thread, daemon=True).start()
threading.Thread(target=start_lobby_thread, daemon=True).start()
threading.Thread(target=start_inicio_thread, daemon=True).start()
threading.Thread(target=start_proximo_thread, daemon=True).start()

# Iniciar o monitor de pausa
threading.Thread(target=monitor_pause, daemon=True).start()

# Manter o script em execução
while True:
    if pause_mode_active:
        if time.time() - pause_mode_start_time > 10:
            pause_mode_active = False
    time.sleep(0.1)
