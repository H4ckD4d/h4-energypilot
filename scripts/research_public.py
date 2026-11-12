"""Opt-in public research only. No customer or private inputs."""
import os,sys
TOPICS={
 'pt-BR':'Normas técnicas públicas e boas práticas para H4 EnergyPilot',
 'en':'Public technical standards and best practices for H4 EnergyPilot',
 'es':'Normas técnicas públicas y buenas prácticas sobre H4 EnergyPilot',
}
def main():
    lang=sys.argv[1] if len(sys.argv)>1 else 'pt-BR'
    if lang not in TOPICS:
        raise SystemExit('Use pt-BR, en or es')
    if not os.getenv('GEMINI_API_KEY'):
        raise SystemExit('Set GEMINI_API_KEY and review external data handling first')
    try:
        from google import genai
        from google.genai import types
    except ImportError as exc:
        raise SystemExit('Install optional google-genai') from exc
    client=genai.Client(api_key=os.environ['GEMINI_API_KEY'])
    response=client.models.generate_content(
       model=os.getenv('GEMINI_MODEL','gemini-2.5-flash'),
       contents=TOPICS[lang]+'; provide dated sources, uncertainties, and links.',
       config=types.GenerateContentConfig(tools=[types.Tool(google_search=types.GoogleSearch())]))
    print(response.text)
if __name__=='__main__':main()
