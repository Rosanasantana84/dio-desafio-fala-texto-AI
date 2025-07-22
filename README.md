# Dio-desafio-fala-texto-AI
Projeto IA para Acolhimento CAPS com Azure Speech e Language Studio

# 🗣️ Acolhedor CAPS IA: Transcrição de Fala com Azure Speech Service

Este repositório contém o projeto desenvolvido como parte do desafio da DIO (Digital Innovation One) focado na aplicação de serviços de Inteligência Artificial da Azure para processamento de fala e linguagem natural. O objetivo principal é demonstrar a capacidade de transcrever áudios utilizando o Azure Speech Service e analisar o texto resultante com o Azure AI Language Service, com foco em potenciais aplicações para o contexto dos Centros de Atenção Psicossocial (CAPS).

## 🚀 Objetivos de Aprendizagem

Ao concluir este desafio, foram abordados os seguintes objetivos:

*Aplicar conceitos de IA e serviços de nuvem (Azure Speech e Language Services) em um ambiente prático.
*Documentar processos técnicos de forma clara e estruturada, como este README e o arquivo de testes.
*Utilizar o GitHub como ferramenta para compartilhamento de documentação técnica e código-fonte.
*Implementar boas práticas de segurança, como o uso de variáveis de ambiente para credenciais.

## ✨ Funcionalidades Atuais

* **Transcrição de Áudio Local:**  Capacidade de transcrever arquivos de áudio para texto utilizando o Azure Speech Service.
* **Suporte a Múltiplos Formatos de Áudio:** Identifica e converte automaticamente arquivos de áudio comuns (ex: .mp3, .ogg, .m4a, .flac) para o formato .wav antes da transcrição local, utilizando pydub e ffmpeg.
* **Análise de Sentimentos:**  Avalia o tom emocional do texto transcrito (positivo, negativo, neutro).
* **Extração de Entidades Nomeadas (NER):**  Identifica e categoriza informações chave no texto (ex: pessoas, locais, organizações).
* **Configuração Segura de Credenciais:**  Utiliza variáveis de ambiente (.env) para gerenciar chaves de API e endpoints de forma segura, mantendo-os fora do código-fonte.
* **Reconhecimento de Idioma:**  Configuração explícita do idioma de reconhecimento para pt-BR (Português do Brasil).

## 🛠️ Configuração do Ambiente e Execução

Para rodar este projeto em sua máquina local, siga os passos abaixo:

### Pré-requisitos

* ****Python 3.x** (preferencialmente com Anaconda ou Miniconda instalado).
* Uma conta Azure com um recurso de **Azure AI Speech Service** configurado.
* A **chave de assinatura** e a **região** do seu recurso Azure Speech Service.
* **Git** (para clonar o repositório).


### Instalação

**Instalação**
1. Clone o repositório:

git clone https://github.com/Rosanasantana84/dio-desafio-fala-texto-AI.git
cd dio-desafio-fala-texto-AI

2. Crie e ative um ambiente Conda (recomendado):

conda create -n acolhedor-ia python=3.x  # Use a versão do seu Python
conda activate acolhedor-ia

(Caso já tenha o ambiente base ativo, você pode pular a criação e usar conda activate base)

3. Instale as dependências Python:

pip install python-dotenv azure-cognitiveservices-speech azure-ai-textanalytics pydub

4. Instale o FFmpeg:

 - Para Windows (recomendado):

  1. Baixe a versão win64 (ex: ffmpeg-master-latest-win64-gpl-shared.zip ou similar) de https://www.gyan.dev/ffmpeg/builds/.

  2. Descompacte o arquivo ZIP em um local fácil de lembrar (ex: C:\ffmpeg).

  3. Adicione a pasta bin do FFmpeg ao seu PATH do sistema:
   Pesquise no Windows por "Editar as variáveis de ambiente do sistema".
   Clique em "Variáveis de Ambiente...".
   Na seção "Variáveis do sistema", encontre a variável Path e clique em "Editar...".
   Clique em "Novo" e adicione o caminho completo para a pasta bin do FFmpeg (ex: C:\ffmpeg\bin).
   Clique "OK" em todas as janelas para fechar.

  4. Reinicie seu terminal (VS Code, Anaconda Prompt) para que as mudanças no PATH entrem em vigor.

  5. Verifique a instalação abrindo um novo terminal e digitando ffmpeg -version.

**Configuração das Variáveis de Ambiente**
1. Crie um arquivo chamado .env na raiz do seu projeto (dio-desafio-fala-texto-AI/).
2. Dentro do arquivo .env, adicione suas credenciais do Azure Speech Service e Azure AI Language Service no seguinte formato (substitua pelos seus valores reais, sem aspas):

SPEECH_KEY=SUA_CHAVE_COMPLETA_DO_SPEECH_SERVICE
SPEECH_REGION=sua_regiao_do_speech_service # Ex: brazilsouth

LANGUAGE_KEY=SUA_CHAVE_COMPLETA_DO_LANGUAGE_SERVICE
LANGUAGE_ENDPOINT=https://seu_endpoint_completo_do_language_service.cognitiveservices.azure.com/

3. Adicione .env ao seu .gitignore: Para garantir que suas chaves não sejam enviadas para o GitHub, adicione a seguinte linha ao seu arquivo .gitignore (crie-o se não existir):
.env

**Preparar Áudio de Teste**
Crie uma pasta chamada data na raiz do seu projeto.
Crie uma pasta chamada temp_wavs dentro da pasta data (ex: data/temp_wavs). O script também tentará criá-la se não existir.
Coloque um arquivo de áudio (ex: .wav, .mp3, .ogg, .m4a, .flac) na pasta data. O script irá procurar o primeiro arquivo suportado e processá-lo.

**Executando o Projeto**
Ative seu ambiente Python (se ainda não estiver ativo):
conda activate base # Ou o nome do seu ambiente, como acolhedor-ia
Certifique-se de que (base) ou (acolhedor-ia) aparece no início do seu prompt.

**Execute o script principal:**

python main.py

O script irá transcrever o áudio e, em seguida, realizar a análise de sentimentos e extração de entidades, exibindo os resultados no terminal.

## 📝 Testes e Observações

### Teste de Transcrição Local

**Áudio de Teste Utilizado:**
Um áudio curto em português (ex: 02.wav), onde uma pessoa comenta sobre a importância de algo que estava procurando.

**Transcrição Gerada:**

É, na real, o mais importante. Quando eu tava procurando isso, é algo que fizesse uma.

**Resultados da Análise de Linguagem**
Após a transcrição, o Azure AI Language Service processou o texto com os seguintes resultados:

**Análise de Sentimentos**
--- Análise de Sentimentos ---
Texto: 'É, na real, o mais importante. Quando eu tava procurando isso, é algo que fizesse uma.'
Sentimento geral: neutral (Confiança: Positivo=0.27, Neutro=0.59, Negativo=0.14)
  Sentença: 'É, na real, o mais importante. ' -> Sentimento: neutral (Confiança: Positivo=0.47, Neutro=0.50, Negativo=0.02)
  Sentença: 'Quando eu tava procurando isso, é algo que fizesse uma.' -> Sentimento: neutral (Confiança: Positivo=0.06, Neutro=0.69, Negativo=0.25)

Observação: O sentimento foi classificado como "neutral", o que é esperado para um texto que expressa uma constatação ou busca, sem carga emocional forte.

**Extração de Entidades (NER)**
--- Extração de Entidades (NER) ---
Texto: 'É, na real, o mais importante. Quando eu tava procurando isso, é algo que fizesse uma.'
  Entidade: 'real' | Categoria: Organization | Subcategoria: Sports | Confiança: 0.88

Observação: A entidade "real" foi identificada como uma Organização/Esporte, o que pode ser uma interpretação comum para o termo "real" (como em "Real Madrid"). Para termos específicos do contexto CAPS, um modelo de linguagem customizado seria mais preciso.

**Resumo Abstrativo**
Observação: A funcionalidade de Resumo Abstrativo foi incluída no código de forma conceitual. Para uma implementação completa, seria necessário utilizar a API assíncrona do Azure AI Language Service para operações de longa duração, que é mais complexa e vai além do escopo da entrega básica deste desafio.

**Observações e Insights Gerais**
Precisão Geral da Transcrição: A transcrição demonstrou uma precisão muito alta para o português do Brasil, capturando todas as palavras e a pontuação de forma correta e fluida para áudios .wav.

**Suporte a Formatos de Áudio:** A implementação da conversão automática de áudio via pydub e ffmpeg resolveu o desafio de lidar com múltiplos formatos de entrada, tornando o sistema mais amigável para o usuário final. Inicialmente, arquivos .mp3 causaram erros (SPXERR_INVALID_HEADER), mas a conversão prévia para .wav garante a compatibilidade com a transcrição local do SDK.

**Termos Específicos do CAPS:** Embora os áudios de teste não contivessem terminologias complexas específicas do CAPS, a clareza da transcrição e a capacidade de extração de entidades demonstram o potencial dos serviços Azure AI. Para maior precisão em jargões técnicos, a personalização de modelos de linguagem seria o próximo passo.

**Dificuldades Iniciais e Resolução:** Houve desafios significativos na configuração inicial do ambiente Python, na correta utilização das variáveis de ambiente (os.getenv), na especificação do idioma de reconhecimento, e na depuração de erros de sintaxe e de execução relacionados a chaves e formatos de áudio. Todas essas questões foram superadas através de um processo iterativo de depuração e correção, garantindo a funcionalidade completa do sistema.

**Qualidade dos Serviços Azure AI para o "Acolhedor CAPS":** O Azure Speech Service e o Azure AI Language Service se mostram ferramentas extremamente promissoras para o objetivo do projeto "Acolhedor CAPS". A capacidade de transcrever conversas de forma precisa e extrair insights emocionais e de entidades pode otimizar o registro de atendimentos, permitindo que os profissionais foquem mais na interação e menos nas anotações manuais. Para áudios longos, a transcrição em lote via Blob Storage é a abordagem adequada.

**Considerações para Áudios Longos e Pausas**
Para lidar com áudios de maior duração (acima de 10 minutos) ou com muitas pausas e múltiplos locutores, a funcionalidade de Transcrição em Lote (Batch Transcription) do Azure Speech Service seria a abordagem mais adequada. Este método processa arquivos hospedados em Azure Blob Storage de forma assíncrona, oferecendo maior robustez e controle para cenários complexos. A estrutura para essa abordagem foi explorada no código (submit_batch_transcription_job), embora sua implementação completa para este desafio básico exija a configuração de um Azure Blob Storage e a utilização de um SDK mais específico para operações em lote (como azure-ai-language-speech).

## 📁 Estrutura do Projeto
dio-desafio-fala-texto-AI/
├── data/
│   ├── acolhedor-teste-caps.wav  # Exemplo de arquivo de áudio (ou outros formatos)
│   └── temp_wavs/                # Pasta para arquivos WAV temporários gerados
├── .env                          # Arquivo para variáveis de ambiente (NÃO ENVIADO PARA O GITHUB)
├── .gitignore                    # Ignora o arquivo .env
├── main.py                       # Script principal com a lógica de transcrição e análise
├── docs/                         # Pasta para documentação adicional (ex: testes_transcricao.md)
│   └── testes_transcricao.md     # Documento detalhando os testes e resultados (opcional)
└── README.md                     # Este arquivo (documentação principal do projeto)

🤝 **Contribuições**
Sinta-se à vontade para explorar, testar e sugerir melhorias.

Desenvolvido como parte do desafio da Digital Innovation One (DIO).

⚠️ **Observação de Uso**
Este projeto foi desenvolvido como parte de um desafio pessoal na Digital Innovation One (DIO) com o objetivo de estudo e demonstração de conhecimentos em IA e serviços de nuvem. Embora o código esteja publicamente disponível para fins de aprendizado, peço a gentileza de não copiá-lo integralmente e apresentá-lo como trabalho próprio. Sinta-se à vontade para referenciá-lo, aprender com ele e usá-lo como inspiração para seus próprios projetos.

Todo o conteúdo e código aqui apresentados são de autoria de **Rosana de Souza Santana.**
