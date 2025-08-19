import os
import dotenv
from googleapiclient.discovery import build
from langchain_core.tools import tool
import requests
from bs4 import BeautifulSoup
import random
import time

dotenv.load_dotenv()

# Substitua pelas suas credenciais
API_KEY = os.getenv("API_CUSTOM_SEARCH")
CX_ANUNCIOS_IMOVEIS = os.getenv("CX_CUSTOM_SEARCH_ANUNCIOS_IMOVEIS")

@tool
def web_search_properties(query: str) -> str:
    """Faz uma busca na web usando a API do Google Custom Search pra buscar imóveis para alugar ou vender.
    Retorna também informações extras das páginas encontradas."""
    try:
        service = build("customsearch", "v1", developerKey=API_KEY)
        # Solicita até 20 resultados (máximo permitido por request)
        res = service.cse().list(q=query, cx=CX_ANUNCIOS_IMOVEIS, num=10).execute()
        items = res.get("items", [])
        # Se houver mais de 10 resultados, tenta buscar mais (até 20)
        if res.get("queries", {}).get("nextPage"):
            next_start = res["queries"]["nextPage"][0]["startIndex"]
            res2 = service.cse().list(q=query, cx=CX_ANUNCIOS_IMOVEIS, num=10, start=next_start).execute()
            items += res2.get("items", [])

        results = []
        for item in items:
            title = item.get("title", "Sem título")
            link = item.get("link", "Sem link")
            snippet = item.get("snippet", "Sem trecho")
            
            # Buscar informações extras da página
            extra_info = ""
            try:
                headers = {
                    'User-Agent': 'Mozilla/5.0',
                    'Accept-Language': 'pt-BR,pt;q=0.9'
                }
                page = requests.get(link, headers=headers, timeout=5)
                if page.status_code == 200:
                    soup = BeautifulSoup(page.text, 'html.parser')
                    page_title = soup.title.string.strip() if soup.title and soup.title.string else "Sem título da página"
                    meta_desc = soup.find('meta', attrs={'name': 'description'})
                    meta_desc_content = meta_desc['content'].strip() if meta_desc and meta_desc.get('content') else "Sem meta description"
                    meta_keywords = soup.find('meta', attrs={'name': 'keywords'})
                    meta_keywords_content = meta_keywords['content'].strip() if meta_keywords and meta_keywords.get('content') else "Sem meta keywords"
                    main_content = soup.find('main') or soup.find('article') or soup.find('body')
                    main_text = main_content.get_text(separator=' ', strip=True) if main_content else ""
                    main_text_preview = main_text[:1000] + "..." if len(main_text) > 1000 else main_text
                    num_images = len(soup.find_all('img'))
                    extra_info = (
                        f"Título da página: {page_title}\n"
                        f"Meta description: {meta_desc_content}\n"
                        f"Meta keywords: {meta_keywords_content}\n"
                        f"Texto principal (preview): {main_text_preview}\n"
                        f"Quantidade de imagens: {num_images}\n"
                    )
            except Exception as e:
                extra_info = f"Não foi possível extrair informações extras: {e}\n"
            
            results.append(
                f"Título: {title}\nURL: {link}\nTrecho: {snippet}\n{extra_info}"
            )
            
        if not results:
            return "Nenhum resultado encontrado."
            
        return "\n---\n".join(results)
    
    except Exception as e:
        return f"Ocorreu um erro durante a busca: {e}"
    
@tool
def browse_page_content(url: str) -> str:
    """Extrai o conteúdo principal de uma página da web a partir de sua URL.
    Útil para ler o conteúdo de anúncios de imóveis.
    A entrada deve ser o URL da página a ser lida."""
    try:
        # Lista de User-Agents populares para rotação
        user_agents = {
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0',
            'Mozilla/5.0 (Linux; Android 13; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36',
        }
        headers = {
            'User-Agent': random.choice(user_agents),
            'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Referer': 'https://www.google.com/',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'DNT': '1',
        }
        # Cookies simulados
        cookies = {
            'CONSENT': 'YES+',
            'NID': '204=xyz',
        }
        # Espera aleatória para evitar bloqueios
        time.sleep(random.uniform(1.5, 3.5))

        response = requests.get(url, headers=headers, cookies=cookies, timeout=12)

        if response.status_code != 200:
            return f"Erro ao acessar a URL {url}: Status Code {response.status_code}. Provavelmente o site bloqueou a requisição."

        soup = BeautifulSoup(response.text, 'html.parser')

        # Tenta extrair título, meta description, keywords
        page_title = soup.title.string.strip() if soup.title and soup.title.string else "Sem título da página"
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        meta_desc_content = meta_desc['content'].strip() if meta_desc and meta_desc.get('content') else "Sem meta description"
        meta_keywords = soup.find('meta', attrs={'name': 'keywords'})
        meta_keywords_content = meta_keywords['content'].strip() if meta_keywords and meta_keywords.get('content') else "Sem meta keywords"

        # Tenta extrair conteúdo principal de várias tags
        main_content = (
            soup.find('main') or
            soup.find('article') or
            soup.find('section') or
            soup.find('body')
        )
        if not main_content:
            return f"Conteúdo principal não encontrado na página {url}."

        text = main_content.get_text(separator=' ', strip=True)
        main_text_preview = text[:2000] + "..." if len(text) > 2000 else text
        num_images = len(main_content.find_all('img')) if main_content else 0

        # Formatação para visualização
        result = (
            f"Título da página: {page_title}\n"
            f"Meta description: {meta_desc_content}\n"
            f"Meta keywords: {meta_keywords_content}\n"
            f"Quantidade de imagens: {num_images}\n"
            f"Texto principal (preview):\n{main_text_preview}\n"
        )
        return result

    except requests.exceptions.RequestException as e:
        return f"Ocorreu um erro na requisição: {e}"
    except Exception as e:
        return f"Ocorreu um erro inesperado: {e}"