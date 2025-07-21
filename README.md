# Dio-desafio-fala-texto-AI
Projeto IA para Acolhimento CAPS com Azure Speech e Language Studio

# 🗣️ Acolhedor CAPS IA: Transcrição de Fala com Azure Speech Service

Este repositório contém o projeto desenvolvido como parte do desafio da DIO (Digital Innovation One) focado na aplicação de serviços de Inteligência Artificial da Azure para processamento de fala e linguagem natural. O objetivo principal é demonstrar a capacidade de transcrever áudios utilizando o Azure Speech Studio, com foco em potenciais aplicações para o contexto dos Centros de Atenção Psicossocial (CAPS).

## 🚀 Objetivos de Aprendizagem

Ao concluir este desafio, foram abordados os seguintes objetivos:

* **Aplicar conceitos** de IA e serviços de nuvem (Azure Speech Service) em um ambiente prático.
* **Documentar processos técnicos** de forma clara e estruturada, como este README e o arquivo de testes.
* **Utilizar o GitHub** como ferramenta para compartilhamento de documentação técnica e código-fonte.

## ✨ Funcionalidades Atuais

* **Transcrição de Áudio Local:** Capacidade de transcrever arquivos de áudio `.wav` curtos para texto utilizando o Azure Speech Service.
* **Configuração Segura de Credenciais:** Demonstração do uso de variáveis de ambiente (`.env`) para gerenciar chaves de API.
* **Reconhecimento de Idioma:** Configuração explícita do idioma de reconhecimento para `pt-BR` (Português do Brasil).

## 🛠️ Configuração do Ambiente e Execução

Para rodar este projeto em sua máquina local, siga os passos abaixo:

### Pré-requisitos

* **Python 3.x** (preferencialmente com Anaconda ou Miniconda instalado).
* Uma conta Azure com um recurso de **Azure AI Speech Service** configurado.
* A **chave de assinatura** e a **região** do seu recurso Azure Speech Service.
* **Git** (para clonar o repositório).

### Instalação

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/seu-usuario/acolhedor-caps-ia.git](https://github.com/seu-usuario/acolhedor-caps-ia.git)
    cd acolhedor-caps-ia
    ```
    https://github.com/Rosanasantana84/dio-desafio-fala-texto-AI

2.  **Crie e ative um ambiente Conda (recomendado):**
    ```bash
    conda create -n acolhedor-ia python=3.x  # Use a versão do seu Python
    conda activate acolhedor-ia
    ```
    *(Caso já tenha o ambiente `base` ativo, você pode pular a criação e usar `conda activate base`)*

3.  **Instale as dependências:**
    ```bash
    pip install python-dotenv azure-cognitiveservices-speech
    ```

### Configuração das Variáveis de Ambiente

1.  Crie um arquivo chamado `.env` na raiz do seu projeto (`acolhedor-caps-ia/`).
2.  Dentro do arquivo `.env`, adicione suas credenciais do Azure Speech Service no seguinte formato:
    ```
    SPEECH_KEY=SUA_CHAVE_COMPLETA_AQUI
    SPEECH_REGION=sua_regiao # Ex: brazilsouth
    ```
    Substitua `SUA_CHAVE_COMPLETA_AQUI` pela sua chave real e `sua_regiao` pela região do seu recurso Azure (ex: `brazilsouth`).

### Preparar Áudio de Teste

1.  Crie uma pasta chamada `data` na raiz do seu projeto.
2.  Coloque um arquivo de áudio curto (`.wav` recomendado) dentro da pasta `data`. O script está configurado para `data/acolhedor-teste-caps.wav`. Se o nome do seu arquivo for diferente, ajuste a variável `audio_file_path` no `main.py`.

### Executando a Transcrição

1.  **Ative seu ambiente Python (se ainda não estiver ativo):**
    ```bash
    conda activate base # Ou o nome do seu ambiente, como acolhedor-ia
    ```
    Certifique-se de que `(base)` ou `(acolhedor-ia)` aparece no início do seu prompt.

2.  **Execute o script principal:**
    ```bash
    python main.py
    ```

## 📝 Testes e Observações

### Teste de Transcrição Local

**Áudio de Teste Utilizado:**
Um áudio curto em português (nome do arquivo: `acolhedor-teste-caps.wav`), onde uma pessoa comenta sobre categorias, incluindo a questão das medicações.

**Transcrição Gerada:**
### Observações e Insights

* **Precisão Geral:** A transcrição demonstrou uma **precisão muito alta** para o português do Brasil, capturando todas as palavras e a pontuação de forma correta e fluida.
* **Termos Específicos do CAPS:** Embora o áudio de teste não contivesse terminologias complexas específicas do CAPS, a clareza da transcrição geral é um forte indicativo do potencial do serviço para lidar com vocabulário mais específico, caso o modelo de linguagem seja ajustado.
* 
* **Dificuldades Iniciais:** Houve desafios na configuração inicial do ambiente Python, na correta utilização das variáveis de ambiente (`os.getenv`) e na especificação do idioma de reconhecimento. No entanto, após as correções (garantindo `speech_config.speech_recognition_language = "pt-BR"` e o uso correto do `python main.py` no ambiente ativado), o serviço funcionou conforme esperado.
* 
* **Qualidade do Serviço para o "Acolhedor CAPS":** O Azure Speech Service se mostra uma ferramenta **extremamente promissora** para o objetivo do projeto "Acolhedor CAPS". A capacidade de transcrever conversas de forma precisa pode otimizar o registro de atendimentos, permitindo que os profissionais foquem mais na interação e menos nas anotações manuais.

### Considerações para Áudios Longos e Pausas

Para lidar com áudios de maior duração (acima de 10 minutos) ou com muitas pausas e múltiplos locutores, a funcionalidade de **Transcrição em Lote (Batch Transcription)** do Azure Speech Service seria a abordagem mais adequada. Este método processa arquivos hospedados em Azure Blob Storage de forma assíncrona, oferecendo maior robustez e controle para cenários complexos. A estrutura para essa abordagem foi explorada no código (`submit_batch_transcription_job`), embora sua implementação completa para este desafio básico exija a configuração de um Azure Blob Storage e a utilização de um SDK mais específico para operações em lote (como `azure-ai-language-speech`).

## 📁 Estrutura do Projeto
acolhedor-caps-ia/
├── data/
│   └── acolhedor-teste-caps.wav  # Arquivo de áudio para transcrição
├── .env                          # Arquivo para variáveis de ambiente (SUA CHAVE E REGIÃO)
├── main.py                       # Script principal com a lógica de transcrição
├── docs/                         # Pasta para documentação adicional (ex: testes_transcricao.md)
│   └── testes_transcricao.md     # Documento detalhando os testes e resultados
└── README.md                     # Este arquivo

## 🤝 Contribuições

Sinta-se à vontade para explorar, testar e sugerir melhorias.

---
**Desenvolvido como parte do desafio da Digital Innovation One (DIO).**

## ⚠️ Observação de Uso

Este projeto foi desenvolvido como parte de um desafio pessoal na Digital Innovation One (DIO) com o objetivo de estudo e demonstração de conhecimentos em IA e serviços de nuvem. Embora o código esteja publicamente disponível para fins de aprendizado, peço a gentileza de **não copiá-lo integralmente e apresentá-lo como trabalho próprio**. Sinta-se à vontade para referenciá-lo, aprender com ele e usá-lo como inspiração para seus próprios projetos.

Todo o conteúdo e código aqui apresentados são de autoria de **Rosana de Souza Santana**.
