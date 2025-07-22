import os
import time
from dotenv import load_dotenv # Embora não vá carregar essas chaves do .env, é bom manter para outras.
import azure.cognitiveservices.speech as speechsdk
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential

# --- CARREGAR VARIÁVEIS DE AMBIENTE DO ARQUIVO .env ---
# Garante que as variáveis do .env sejam carregadas no início do script.
load_dotenv() # Mantenha esta linha para carregar outras possíveis variáveis do .env

# --- CONFIGURAÇÕES DO SEU RECURSO AZURE SPEECH (DIRETAMENTE NO CÓDIGO) ---
# ATENÇÃO: É uma MÁ PRÁTICA de segurança inserir chaves diretamente no código.
# Use um arquivo .env para chaves reais em produção, lendo com os.getenv().
speech_key = "551d723268894fd8b817ba92b225e3cc"   # Corrigido: minúsculas e entre aspas.
speech_region = "brazilsouth"                     # Corrigido: minúsculas e entre aspas.
                                                  # OBS: Você tinha "brazilsout", o correto é "brazilsouth".

# --- CONFIGURAÇÕES DO SEU RECURSO AZURE AI LANGUAGE (DIRETAMENTE NO CÓDIGO) ---
language_key = "21J3G1ExEaMjC2Sny97sCh4bT5juqINPZUbGftfe7c61ANoff6ndJQQJ99BGACZoyfiXJ3w3AAAaACOGt2nM" # Corrigido: minúsculas e entre aspas.
language_endpoint = "https://language-acolhedor-caps-ia.cognitiveservices.azure.com/" # Corrigido: minúsculas e entre aspas.

# --- VERIFICAÇÕES DE CHAVES E ENDPOINTS ---
# Se alguma chave ou endpoint não for encontrada, o script será encerrado com uma mensagem de erro detalhada.

if not speech_key:
    print("Erro: Variável de ambiente SPEECH_KEY não encontrada ou vazia.")
    print("Por favor, verifique se a 'speech_key' está definida corretamente no código.")
    exit()

if not speech_region:
    print("Erro: Variável de ambiente SPEECH_REGION não encontrada ou vazia.")
    print("Por favor, verifique se a 'speech_region' está definida corretamente no código.")
    exit()

if not language_key:
    print("Erro: Variável de ambiente LANGUAGE_KEY não encontrada ou vazia.")
    print("Por favor, verifique se a 'language_key' está definida corretamente no código.")
    exit()

if not language_endpoint:
    print("Erro: Variável de ambiente LANGUAGE_ENDPOINT não encontrada ou vazia.")
    print("Por favor, verifique se a 'language_endpoint' é um URL completo e está definida corretamente no código.")
    exit()

# Inicializar o cliente para o Azure AI Language Service
try:
    text_analytics_client = TextAnalyticsClient(
        endpoint=language_endpoint,
        credential=AzureKeyCredential(language_key)
    )
except Exception as e:
    print(f"Erro ao inicializar o cliente do Azure AI Language: {e}")
    print("Verifique seu LANGUAGE_ENDPOINT e LANGUAGE_KEY (ou language_endpoint e language_key) no código.")
    exit()

# --- Caminho da pasta onde os áudios serão colocados pelos profissionais ---
AUDIO_FOLDER = "data"
# Tipos de arquivo de áudio suportados para transcrição local.
# O Azure Speech SDK para transcrição de arquivo local (recognize_once_async)
# funciona melhor com WAV. MP3 e OGG podem funcionar dependendo da configuração
# do sistema e codecs, mas são mais robustos para transcrição em lote (assíncrona).
SUPPORTED_AUDIO_EXTENSIONS = ('.wav', '.mp3', '.ogg')

# ---- FUNÇÃO PARA TRANSCRIÇÃO DE ARQUIVO LOCAL (PARA ÁUDIOS CURTOS) ----
def transcribe_file_local():
    """
    Procura por arquivos de áudio suportados na pasta 'data' e transcreve o primeiro encontrado.
    Ideal para arquivos menores (até ~10 minutos ou 15MB).
    Para arquivos mais longos, o processamento em lote é recomendado.
    """
    audio_file_found = None
    # Itera sobre os arquivos na pasta de áudio para encontrar o primeiro suportado
    for filename in os.listdir(AUDIO_FOLDER):
        if filename.lower().endswith(SUPPORTED_AUDIO_EXTENSIONS):
            audio_file_found = os.path.join(AUDIO_FOLDER, filename)
            break # Encontrou um, para por aqui.

    if not audio_file_found:
        print(f"Erro: Nenhum arquivo de áudio suportado ({', '.join(SUPPORTED_AUDIO_EXTENSIONS)}) encontrado na pasta '{AUDIO_FOLDER}'.")
        print("Por favor, coloque um arquivo de áudio na pasta 'data'.")
        return None

    print(f"Transcrevendo áudio local: {audio_file_found}...")

    # Configuração do serviço de fala
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=speech_region)
    speech_config.speech_recognition_language = "pt-BR" # Define o idioma para português do Brasil

    # Configuração do áudio de entrada
    audio_config = speechsdk.AudioConfig(filename=audio_file_found)

    # Criar um reconhecedor de fala
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    # Realizar o reconhecimento de fala uma vez
    result = speech_recognizer.recognize_once_async().get()

    # Processar o resultado do reconhecimento
    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        print("Transcrição concluída:")
        print(result.text)
        return result.text # Retorna o texto transcrito
    elif result.reason == speechsdk.ResultReason.NoMatch:
        print("Não foi possível reconhecer fala no arquivo de áudio. Verifique se o áudio contém fala clara.")
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print(f"Reconhecimento cancelado: {cancellation_details.reason}")
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print(f"Detalhes do erro: {cancellation_details.error_details}")
            if cancellation_details.error_details.find("InvalidSubscriptionKey") != -1:
                print("ERRO DE CHAVE: Sua SPEECH_KEY pode estar incorreta ou expirada. Verifique-a no .env ou no Portal do Azure.")
    return None # Retorna None em caso de falha na transcrição

# --- FUNÇÕES DE ANÁLISE DE LINGUAGEM NATURAL (NLP) ---

def analyze_sentiment(text: str):
    """
    Analisa o sentimento de um texto (positivo, negativo, neutro ou misto).
    """
    print("\n--- Análise de Sentimentos ---")
    try:
        response = text_analytics_client.analyze_sentiment(documents=[text])[0]
        print(f"Texto: '{text}'")
        print(f"Sentimento geral: {response.sentiment} (Confiança: Positivo={response.confidence_scores.positive:.2f}, Neutro={response.confidence_scores.neutral:.2f}, Negativo={response.confidence_scores.negative:.2f})")
        for sentence in response.sentences:
            print(f"  Sentença: '{sentence.text}' -> Sentimento: {sentence.sentiment} (Confiança: Positivo={sentence.confidence_scores.positive:.2f}, Neutro={sentence.confidence_scores.neutral:.2f}, Negativo={sentence.confidence_scores.negative:.2f})")
        return response.sentiment
    except Exception as e:
        print(f"Erro na análise de sentimentos: {e}")
        return None

def extract_entities(text: str):
    """
    Extrai entidades nomeadas (pessoas, locais, organizações, etc.) de um texto.
    """
    print("\n--- Extração de Entidades (NER) ---")
    try:
        response = text_analytics_client.recognize_entities(documents=[text])[0]
        print(f"Texto: '{text}'")
        if response.entities:
            for entity in response.entities:
                print(f"  Entidade: '{entity.text}' | Categoria: {entity.category} | Subcategoria: {entity.subcategory if entity.subcategory else 'N/A'} | Confiança: {entity.confidence_score:.2f}")
        else:
            print("  Nenhuma entidade encontrada.")
        return response.entities
    except Exception as e:
        print(f"Erro na extração de entidades: {e}")
        return None

def abstractive_summarization(text: str):
    """
    Gera um resumo abstrativo de um texto. Esta é uma funcionalidade mais avançada.
    """
    print("\n--- Resumo Abstrativo (Avançado) ---")
    print("O Resumo Abstrativo é uma funcionalidade que pode exigir uma API/cliente")
    print("diferente ou configurações específicas de operação de longa duração (LRO) no SDK.")
    print("Para fins de demonstração neste desafio, o foco pode ser em Análise de Sentimentos e Extração de Entidades.")
    print("Se for implementar, use o begin_abstractive_summarization do SDK Text Analytics.")
    return None

# ---- FUNÇÃO PARA TRANSCRIÇÃO EM LOTE (PARA ÁUDIOS LONGOS E MÚLTIPLOS FORMATOS) ----
# Esta função é conceitual. A implementação REAL de transcrição em lote requer o SDK 'azure-ai-language-speech' (v2)
# e a configuração de Azure Blob Storage.
def submit_batch_transcription_job(audio_blob_uri: str, audio_format: str = "wav"):
    """
    Submete um trabalho de transcrição em lote para áudios armazenados no Azure Blob Storage.
    Suporta diversos formatos (WAV, MP3, OGG, FLAC, etc.) e é ideal para áudios longos.
    """
    print(f"\nSubmetendo trabalho de transcrição em lote para: {audio_blob_uri}")
    print("Esta função é conceitual e requer instalações e configurações adicionais para ser funcional.")
    print("Para a entrega básica na DIO, você pode focar no teste de transcrição local com um áudio curto,")
    print("e documentar que para áudios longos, o método de transcrição em lote via Blob Storage seria utilizado.")
    # Exemplo CONCEITUAL de como seria a chamada (comentado)
    # from azure.ai.language.speech import SpeechClient
    # from azure.identity import DefaultAzureCredential
    # try:
    #     client = SpeechClient(endpoint=f"https://{speech_region}.api.cognitive.microsoft.com/",
    #                           credential=DefaultAzureCredential())
    #     poller = client.begin_create_batch_transcription(
    #         display_name=f"AcolhedorCAPS_Job_{time.strftime('%Y%m%d%H%M%S')}",
    #         locale="pt-BR",
    #         content_urls=[audio_blob_uri]
    #     )
    #     print("Aguardando conclusão do resumo abstrativo...")
    #     job_result = poller.result()
    #     print(f"Transcrição em lote concluída. Status: {job_result.status}")
    # except Exception as e:
    #     print(f"Erro ao tentar submeter o trabalho de transcrição em lote (conceitual): {e}")
    return None

# --- EXECUÇÃO PRINCIPAL DO SCRIPT ---

if __name__ == "__main__":
    print("Iniciando testes do Acolhedor CAPS IA...")

    # --- TESTE BÁSICO DE TRANSCRIÇÃO LOCAL ---
    print("\n--- INICIANDO TESTE DE TRANSCRIÇÃO LOCAL ---")
    transcribed_text = transcribe_file_local()

    # --- NOVOS TESTES DE ANÁLISE DE LINGUAGEM NATURAL ---
    # As funções de NLP são chamadas apenas se a transcrição local for bem-sucedida.
    if transcribed_text:
        print("\n--- INICIANDO TESTES DE AZURE AI LANGUAGE ---")

        analyze_sentiment(transcribed_text)
        extract_entities(transcribed_text)
        abstractive_summarization(transcribed_text) # Esta função é conceitual e não realiza resumo real por padrão.
    else:
        print("\nNão foi possível obter transcrição para análise de linguagem.")
        print("Certifique-se de que há um arquivo de áudio válido na pasta 'data' e suas chaves do Speech Service estão corretas.")

    # --- INFORMAÇÕES SOBRE TRANSCRIÇÕES LONGAS E FORMATOS ---
    # Esta seção é informativa sobre a abordagem para áudios maiores.
    print("\n--- SOBRE TRANSCRIÇÕES LONGAS E FORMATOS ---")
    print("Para áudios de até 1:30h (90 minutos) e diversos formatos (MP3, FLAC, OGG, etc.),")
    print("o Azure Speech Service requer que o áudio seja hospedado em um Azure Blob Storage e")
    print("que seja utilizada a funcionalidade de 'Transcrição em Lote'.")
    print("O código comentado 'submit_batch_transcription_job' mostra a estrutura para isso.")
    print("Para a entrega básica na DIO, você pode focar no teste de transcrição local com um áudio curto,")
    print("e documentar que para áudios longos, o método de transcrição em lote via Blob Storage seria utilizado.")
