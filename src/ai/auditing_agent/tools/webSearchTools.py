import os
import dotenv
from googleapiclient.discovery import build
from langchain_core.tools import tool
import requests
from bs4 import BeautifulSoup

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
        res = service.cse().list(q=query, cx=CX_ANUNCIOS_IMOVEIS).execute()
        
        results = []
        for item in res.get("items", []):
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
                    extra_info = f"Título da página: {page_title}\nMeta description: {meta_desc_content}\n"
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
        # Fazer a requisição HTTP para a URL
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Referer': 'https://www.google.com/'  # Simula que a requisição veio do Google
        }
        response = requests.get(url, headers=headers, timeout=10)
        
        # Verificar se a requisição foi bem-sucedida
        if response.status_code != 200:
            return f"Erro ao acessar a URL {url}: Status Code {response.status_code}. Provavelmente o site bloqueou a requisição."

        # Usar BeautifulSoup para analisar o HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Tentar extrair o texto principal da página
        main_content = soup.find('main') or soup.find('article') or soup.find('body')
        
        if not main_content:
            return f"Conteúdo principal não encontrado na página {url}."

        # Retornar o texto limpo
        text = main_content.get_text(separator=' ', strip=True)
        
        # Limitar o tamanho do texto para evitar sobrecarga no LLM
        return text[:2000] + "..." if len(text) > 2000 else text

    except requests.exceptions.RequestException as e:
        return f"Ocorreu um erro na requisição: {e}"
    except Exception as e:
        return f"Ocorreu um erro inesperado: {e}"