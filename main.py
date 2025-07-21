import os
import time
import azure.cognitiveservices.speech as speechsdk
# A linha abaixo "from dotenv import load_dotenv" foi removida
# pois as chaves serão inseridas diretamente.

# --- ATENÇÃO: INSERINDO CHAVES DIRETAMENTE NO CÓDIGO ---
# É uma MÁ PRÁTICA de segurança. Use um arquivo .env para chaves reais em produção.
speech_key = "8d0cf4c7db784c78b4072b412d4e6633"  # Sua CHAVE 2 do Azure Speech Service
speech_region = "brazilsouth"                 # Sua REGIÃO do Azure Speech Service

# Caminho para o arquivo de áudio local que você quer transcrever
# Para testar com áudios longos, você precisará de um URI de blob storage.
# Este exemplo mostra como iniciar uma transcrição de um arquivo local,
# mas para > 10 minutos (ou 15MB), o ideal é usar um URI do Azure Blob Storage.
audio_file_path = "data/acolhedor-teste-caps.wav"

# ---- FUNÇÃO PARA TRANSCRIÇÃO DE ARQUIVO LOCAL (PARA TESTES RÁPIDOS < 10min) ----
def transcribe_file_local():
    """
    Transcreve um arquivo de áudio local usando o serviço Speech.
    Ideal para arquivos menores (até ~10 minutos ou 15MB).
    Para arquivos mais longos, o processamento em lote é recomendado.
    """
    if not os.path.exists(audio_file_path):
        print(f"Erro: Arquivo de áudio não encontrado em {audio_file_path}")
        print("Por favor, coloque um arquivo de áudio de teste (ex: seu_audio_de_teste.wav) na pasta 'data'.")
        return

    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=speech_region)
    # --- ALTERAÇÃO AQUI: DEFINA O IDIOMA DE RECONHECIMENTO ---
    speech_config.speech_recognition_language = "pt-BR" 
    # --- FIM DA ALTERAÇÃO ---

    # Opcional: Para reconhecimento contínuo de várias vozes, considere o diarization
    # speech_config.set_property(speechsdk.PropertyId.SpeechServiceConnection_DifferentiateSpeakers, "true")

    audio_config = speechsdk.AudioConfig(filename=audio_file_path)

    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    print(f"Transcrevendo áudio local: {audio_file_path}...")
    result = speech_recognizer.recognize_once_async().get()

    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        print("Transcrição concluída:")
        print(result.text)
        return result.text
    elif result.reason == speechsdk.ResultReason.NoMatch:
        print("Não foi possível reconhecer fala no arquivo.")
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print(f"Reconhecimento cancelado: {cancellation_details.reason}")
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print(f"Detalhes do erro: {cancellation_details.error_details}")
    return None

# ---- FUNÇÃO PARA TRANSCRIÇÃO EM LOTE (PARA ÁUDIOS LONGOS E MÚLTIPLOS FORMATOS) ----
# Para áudios de até 1:30h (90 minutos), o ideal é o processamento em lote.
# Você precisará fazer upload dos seus áudios para um Azure Blob Storage.

# NOTA IMPORTANTE: A implementação REAL de transcrição em lote requer o SDK 'azure-ai-language-speech' (v2)
# e a configuração de Azure Blob Storage. Este é um exemplo CONCEITUAL para demonstração.

# Exemplo de importações necessárias para o SDK v2 (descomente se for implementar de verdade):
# from azure.ai.language.speech import SpeechClient
# from azure.identity import DefaultAzureCredential # Para autenticação segura

def submit_batch_transcription_job(audio_blob_uri: str, audio_format: str = "wav"):
    """
    Submete um trabalho de transcrição em lote para áudios armazenados no Azure Blob Storage.
    Suporta diversos formatos (WAV, MP3, OGG, FLAC, etc.).
    Para mais informações sobre formatos: https://learn.microsoft.com/en-us/azure/ai-services/speech-service/batch-transcription#supported-audio-formats
    """
    print(f"Submetendo trabalho de transcrição em lote para: {audio_blob_uri}")
    print("Esta função é conceitual e requer instalações e configurações adicionais para ser funcional.")
    
    # Exemplo CONCEITUAL de como seria a chamada usando o SDK Azure AI Speech (v2):
    # try:
    #     # A autenticação pode ser via DefaultAzureCredential ou AzureKeyCredential
    #     # client = SpeechClient(endpoint=f"https://{speech_region}.api.cognitive.microsoft.com/", 
    #     #                      credential=DefaultAzureCredential()) # OU AzureKeyCredential(speech_key)
    #
    #     display_name = f"AcolhedorCAPS_Transcricao_{time.strftime('%Y%m%d%H%M%S')}"
    #     
    #     # Parâmetros do job
    #     job_parameters = {
    #         "display_name": display_name,
    #         "locale": "pt-BR", # Idioma do áudio
    #         "content_urls": [audio_blob_uri], # URI(s) do(s) áudio(s) no Blob Storage
    #         "properties": {
    #             "wordLevelTimestampsEnabled": False,
    #             "diarizationEnabled": False, # 'True' para identificar múltiplos falantes
    #             "profanityFilterMode": "Masked",
    #             "segmentSilenceTimeoutMs": "1000" # Ajuste para lidar com pausas
    #         }
    #     }
    #
    #     # Submetendo o trabalho de transcrição
    #     # poller = client.begin_create_batch_transcription(**job_parameters)
    #     # print(f"Trabalho '{display_name}' submetido. Monitorando status...")
    #     # job_result = poller.result() # Isso aguarda a conclusão do job
    #     # print(f"Transcrição em lote concluída para ID: {job_result.id}. Status: {job_result.status}")
    #     # print("Resultados disponíveis no Blob Storage de saída configurado ou via API.")
    #
    # except Exception as e:
    #     print(f"Erro ao tentar submeter o trabalho de transcrição em lote (conceitual): {e}")

    print("Para a entrega básica na DIO, você pode focar no teste de transcrição local com um áudio curto,")
    print("e documentar que para áudios longos, o método de transcrição em lote via Blob Storage seria utilizado.")

    # Aguarda o trabalho ser concluído
    while job.status not in [speechsdk.TranscriptionStatus.Succeeded, speechsdk.TranscriptionStatus.Failed]:
        time.sleep(10) # Aguarda 10 segundos antes de verificar novamente
        job = speechsdk.SpeechRecognizer.get_batch_transcription_job(client, job.id)
        print(f"Status do trabalho: {job.status}")

    if job.status == speechsdk.TranscriptionStatus.Succeeded:
        print("\nTranscrição em lote concluída com sucesso!")
        for file in job.get_files():
            print(f"  URI do arquivo de resultado: {file.uri}")
            # Você pode baixar o conteúdo do URI para obter a transcrição completa
            # Ex: (requer biblioteca 'requests' para baixar)
            # import requests
            # response = requests.get(file.uri)
            # if response.status_code == 200:
            #     print("Conteúdo da transcrição:")
            #     print(response.text)
            # else:
            #     print(f"Erro ao baixar resultado: {response.status_code}")
    else:
        print(f"\nErro na transcrição em lote. Status: {job.status}")
        print(f"Detalhes do erro: {job.properties.get('error', 'N/A')}")

# --- EXEMPLOS DE USO ---

if __name__ == "__main__":
    print("Iniciando testes de transcrição...")

    # Exemplo 1: Transcrição de um arquivo de áudio local (ideal para testes rápidos < 10min)
    # Certifique-se de ter um arquivo 'data/seu_audio_de_teste.wav'
    # transcribe_file_local()

    # Exemplo 2: Transcrição em lote de um áudio no Azure Blob Storage
    # ESTE É O MÉTODO RECOMENDADO PARA ÁUDIOS LONGOS (até 1:30h)
    # Você PRECISA de um URI de blob storage para este teste.
    # Como obter o URI:
    # 1. Crie uma conta de armazenamento no Azure.
    # 2. Crie um contêiner (ex: 'audios-caps').
    # 3. Faça upload do seu arquivo de áudio (ex: 'sessao_longa.mp3') para este contêiner.
    # 4. Gere uma SAS URI (Shared Access Signature URI) para o arquivo de áudio, com permissão de leitura.
    #    (No portal, vá para o blob, clique em 'Gerar SAS' e configure as permissões e validade.)
    # 5. Cole essa SAS URI abaixo.

    # Exemplo de URI (substitua pelo seu):
    # azure_blob_audio_uri = "https://suaconta.blob.core.windows.net/seucntainer/sessao_longa.mp3?sv=...suas_credenciais_sas..."

    # if azure_blob_audio_uri:
    #     submit_batch_transcription_job(azure_blob_audio_uri, audio_format="mp3")
    # else:
    #     print("Pular teste de transcrição em lote: URI do blob não fornecido.")
    #     print("Para testar áudios longos, você precisará configurar um Azure Blob Storage e gerar uma SAS URI.")

    print("\n--- TESTE BÁSICO DE TRANSCRIÇÃO LOCAL ---")
    print("Para transcrever um arquivo local (para a DIO, você pode usar um áudio curto aqui):")
    transcribe_file_local()
    print("\n--- SOBRE TRANSCRIÇÕES LONGAS E FORMATOS ---")
    print("Para áudios de até 1:30h (90 minutos) e diversos formatos (MP3, FLAC, OGG, etc.), o Azure Speech Service requer que o áudio seja hospedado em um Azure Blob Storage e que seja utilizada a funcionalidade de 'Transcrição em Lote'.")
    print("O código comentado 'submit_batch_transcription_job' mostra a estrutura para isso.")
    print("Para a entrega básica na DIO, você pode focar no teste de transcrição local com um áudio curto, e documentar que para áudios longos, o método de transcrição em lote via Blob Storage seria utilizado.")