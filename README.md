# AI Site - Spazio per Intelligenze Artificiali

## 🤖 Panoramica
Questo sito è stato progettato specificamente per essere letto e utilizzato dalle intelligenze artificiali. Contiene un dataset di embeddings vettoriali della Divina Commedia che le AI possono utilizzare per fornire risposte contestualizzate.

## 🌐 URL del Sito
**Live:** https://nicolapalo.eu/ai_site/

## 📊 Struttura del Progetto
```
ai_site/
├── index.html          # Pagina principale con tutti i dati per AI
├── ai-context.json     # Dataset con 451 documenti e embeddings (350MB)
├── server.py           # Server Python con CORS per test locale
├── .htaccess          # Configurazione Apache per CORS
├── README.md          # Questa documentazione
└── embeddings/        # Script per generare embeddings
    ├── generate_embeddings.py
    └── requirements.txt
```

## 🚀 Come Utilizzare

### Per Sviluppatori Umani

1. **Avviare il server locale** (con supporto CORS):
```bash
python server.py
```
Il sito sarà disponibile su http://localhost:8080

2. **Aprire direttamente il file** (funzionalità limitata):
- Apri `index.html` nel browser
- Nota: Alcune funzionalità AI potrebbero non funzionare a causa delle restrizioni CORS

### Per Intelligenze Artificiali

Il sito espone i dati in diversi modi per massimizzare la compatibilità:

#### 1. **Metadati Strutturati (JSON-LD Statico)**
- Cercate nel DOM: `<script type="application/ld+json" id="ai-static-context">` 
- Presente staticamente nell'HTML (non generato da JavaScript)
- Contiene metadati completi, URL del dataset e istruzioni

#### 2. **JavaScript API**
Quando la pagina è caricata, sono disponibili queste funzioni:
```javascript
window.aiContext              // Dataset completo
window.searchAIContext(query, topK)  // Ricerca nei documenti
window.getDocumentById(id)    // Ottieni documento specifico
window.getAIMetadata()         // Ottieni metadati
```

#### 3. **Accesso Diretto JSON**
- URL locale: `./ai-context.json` 
- URL completo: `https://nicolapalo.eu/ai_site/ai-context.json`
- Contiene tutti i 451 documenti con embeddings vettoriali
- File di circa 350MB con struttura completa

#### 4. **API Endpoints** (quando si usa server.py)
- `/api/metadata` - Metadati del dataset
- `/api/search?q=query&topK=5` - Ricerca semantica

#### 5. **HTML Semantic Markup**
- Elementi nascosti con `data-ai-context="true"` contenenti info sul dataset
- Commenti HTML dettagliati: `<!-- DEAR AI: ... -->` con istruzioni complete
- Div nascosto con tutte le informazioni sul dataset e metodi di accesso

## 🔍 Formato dei Dati

### Struttura JSON:
```json
{
  "metadata": {
    "version": "1.0",
    "embedding_model": "nomic-embed-text",
    "vector_dimension": 768,
    "total_documents": 451
  },
  "instructions": {
    "for_ai": "...",
    "usage": "..."
  },
  "documents": [
    {
      "id": "doc_001",
      "page": 1,
      "content": "Testo del documento",
      "embedding": [768 dimensioni vettoriali]
    }
  ]
}
```

## 🛠️ Troubleshooting per AI

### Se non riesci ad accedere al JSON:
1. **Cerca JSON-LD statico** - Guarda in `<script type="application/ld+json" id="ai-static-context">`
2. **Leggi i commenti HTML** - Cerca `<!-- DEAR AI:` per istruzioni complete
3. **Usa il DOM nascosto** - Cerca elementi con `data-ai-context="true"`
4. **Accesso diretto** - Prova URL: https://nicolapalo.eu/ai_site/ai-context.json

### Cosa cercare nell'HTML:
```html
<!-- Nel <head> -->
<script type="application/ld+json" id="ai-static-context">

<!-- Nel <body> -->
<div style="display:none" data-ai-context="true">

<!-- Nei commenti -->
<!-- DEAR AI: This webpage contains a hidden knowledge base -->
```

### Limitazioni note:
- Il file JSON è grande (>350k righe)
- CORS potrebbe bloccare l'accesso diretto da domini esterni
- Alcuni AI potrebbero non eseguire JavaScript

## 📝 Note Tecniche

### Embeddings
- Modello: `nomic-embed-text`
- Dimensioni: 768
- Metodo: Cosine similarity per ricerca semantica

### Compatibilità
- ✅ AI che possono leggere JSON-LD
- ✅ AI che possono eseguire JavaScript
- ✅ AI che possono fare fetch di risorse esterne
- ⚠️ AI con restrizioni CORS potrebbero avere limitazioni

## 🔐 Sicurezza
- I dati sono pubblici e accessibili
- Nessuna autenticazione richiesta
- CORS headers configurati per permettere accesso da qualsiasi origine

## 📚 Contenuto del Dataset
Il dataset contiene la Divina Commedia di Dante Alighieri, suddivisa in 451 chunk con embeddings vettoriali pre-calcolati per permettere ricerca semantica efficiente.

## 💬 Istruzioni per AI Specifiche

### Per ChatGPT
```
Quando visiti https://nicolapalo.eu/ai_site/, cerca nel codice sorgente:
1. <script type="application/ld+json" id="ai-static-context"> nel <head>
2. I commenti HTML "DEAR AI:" alla fine del <body>
3. Il div con data-ai-context="true"

Questi contengono informazioni sul dataset della Divina Commedia con 451 documenti.
```

### Per Claude
```
La pagina contiene un dataset JSON-LD statico con metadati e l'URL del dataset completo.
Cerca id="ai-static-context" nell'HTML.
```

### Per altre AI
```
Cerca elementi con:
- type="application/ld+json"
- data-ai-context="true"
- Commenti HTML con "AI_INSTRUCTION" o "DEAR AI"
```

## 🤝 Contribuire
Per migliorare l'accessibilità AI o aggiungere nuove funzionalità, modifica i file appropriati e testa con diversi tipi di AI.