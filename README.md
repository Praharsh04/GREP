# GRE Vocab Site (Wordsite)
https://grep-nu.vercel.app/

A self-contained GRE vocabulary learning application with over 900 words, including definitions, etymology, and memory hooks.

## Features
- **Flashcard Mode**: Interactive study sessions.
- **Search**: Quick access to any word in the database.
- **Grouped Learning**: Words organized by Greg Mat groups.
- **Synonym Clusters**: Grouped by meaning.
- **Mastery Tracking**: Mark words as mastered or add them to your hitlist (saved locally).

## Deployment
This site is ready for deployment on **Vercel**, **GitHub Pages**, or any static host.
The main entry point is `index.html`.

## Note on "Generate Experience"
The application includes a "Generate Experience" button that uses the Anthropic API to create new cards on the fly. 
To use this feature:
1. You will need an Anthropic API key.
2. Note that calling the API directly from the frontend may be blocked by CORS or expose your API key. It is recommended to use a serverless function as a proxy if you wish to enable this feature in production.
