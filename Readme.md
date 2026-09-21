# Proyecto Chatbot CIICAp — LLM + RAG 🤖
Asistente virtual para la página institucional del CIICAp, diseñado para facilitar la búsqueda de información a estudiantes y visitantes mediante inteligencia artificial.

## Stack de Tecnologías 
- Postgresql 
- Docker
- Fast API LTS 
- REST
- Python 3.11
### ¿Por qué Python 3.11?
Compatibilidad total con todas las librerías: transformers, torch, fastapi, redis, psycopg2, bitsandbytes y accelerate tienen soporte completamente estable en 3.11.
Rendimiento es hasta un 25% más rápido que 3.10 en operaciones generales, y tiene mejor soporte de PyTorch en Windows.
Google Colab actualmente corre Python 3.11 como versión por defecto, lo que significa que si desarrollas en 3.11 local, el código correrá igual en Colab sin problemas.


- 
### Transformers
- https://huggingface.co/PlanTL-GOB-ES/roberta-base-bne
- https://huggingface.co/dccuchile/bert-base-spanish-wwm-cased
  

## Librerias
- BeautifulSoup

## Herramientas
- Web Scraping
  - https://www.youtube.com/watch?v=bK3EwIMHm94
  - https://www.youtube.com/watch?v=yKi9-BfbfzQ
- RAG
  - https://www.youtube.com/watch?v=uAsd9pOIcLg
  - https://www.youtube.com/watch?v=W2YwMuxzyJY
  - https://www.youtube.com/watch?v=tjcMv_CPIxA
  - Qué es?
    - https://www.youtube.com/watch?v=esQ4LMVdbaA&t=210s
    - https://www.youtube.com/watch?v=5Y3a61o0jFQ




## Porqué se ha elegido Gemma 3 4B
este modelo de LLM se escogio debido a que a pesar de tener bastantes datos con los que fue entrenado relativamente no es tan pesado como otros que se pueden llegar a encontrar, a parte al hacer las pruebas tecnicas y empiricas este no presento gran demanda en el software, tambien porque sus respuestas comparadas con otros modelos fueron más acertivas y coherentes.  


```
chatbot-institucional/
│
├── docs/                         # Documentación técnica y notas del proyecto
│   ├── architecture.md           # Diagramas y flujo de datos del RAG + Redis
│   ├── research_notes/           # Tus apuntes escolares, modelos evaluados y benchmarks
│   └── fine_tuning_plan.md       # Estrategia futura para reentrenamiento de pesos
│
├── data/                         # Recursos locales de datos
│   ├── sql/
│   │   └── init_pgvector.sql     # Script DDL para tablas y extensiones de PostgreSQL
│   └── prompts/                  # Plantillas de prompts del sistema
│
├── src/                          # Código fuente del paquete principal
│   └── chatbot_core/             # Nombre del paquete importable
│       ├── __init__.py           # Expone la interfaz pública (ChatbotPipeline)
│       ├── config.py             # Gestión de variables de entorno y parámetros
│       ├── engine.py             # Orquestador principal (Patrón Facade)
│       │
│       ├── cache/                # Módulo de Redis (Caché Semántica / KV)
│       │   ├── __init__.py
│       │   └── redis_manager.py
│       │
│       ├── retrieval/            # Módulo RAG y Persistencia Vectorial
│       │   ├── __init__.py
│       │   ├── embeddings.py     # Generación de embeddings (HuggingFace / PyTorch)
│       │   └── vector_store.py   # Consultas similarity search en PostgreSQL (pgvector)
│       │
│       ├── web_search/           # Módulo de Contingencia Búsqueda Web
│       │   ├── __init__.py
│       │   └── tavily_client.py  # Conector Tavily/Serper con filtro de dominio
│       │
│       ├── llm/                  # Módulo de Inferencia y Generación
│       │   ├── __init__.py
│       │   ├── generator.py      # Pipeline de HuggingFace / Transformers
│       │   └── prompt_builder.py # Ensamblado de Contexto + Pregunta
│       │
│       └── telemetry/            # Módulo de Mapeo para Fine-Tuning
│           ├── __init__.py
│           └── logger.py         # Registro de dataset de entrenamiento (Prompt, Contexto, Resp)
│
├── tests/                        # Pruebas unitarias e integración (Pytest)
│   ├── test_cache.py
│   ├── test_retrieval.py
│   └── test_engine.py
│
├── .env.example                  # Plantilla de credenciales (PostgreSQL, Redis, API Keys)
├── .gitignore                    # Exclusión de __pycache__, .env, pesos pesados, etc.
├── pyproject.toml                # Definición formal del paquete Python y dependencias
├── README.md                     # Manual de instalación y uso rápido para el desarrollador Django
└── run_demo.py                   # Script ejecutable en CLI para pruebas independientes
```