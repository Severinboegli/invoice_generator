from weasyprint import HTML, CSS
from datetime import datetime

OUTPUT_FILENAME = f"./docs/output-{datetime.now().strftime('%d-%b-%Y')}"
TEMPLATE_HTML_PATH = "./template.html"

TEMPLATE_CSS = [
    CSS("./template.css"),
    CSS("https://cdn.jsdelivr.net/npm/bootstrap@4.6.2/dist/css/bootstrap.min.css" ),
    CSS("https://maxcdn.bootstrapcdn.com/font-awesome/4.3.0/css/font-awesome.min.css" )
]

def get_context_data(context_json:dict)->dict:
# Standard-Stundensatz
    hourly_rate = 20.0

    # Liste der Resultate umwandeln
    simplified_results = []
    for r in context_json.get("results", []):
        p = r["properties"]
        simplified_results.append({
            "title": p["Titel"]["title"][0]["plain_text"] if p["Titel"]["title"] else "",
            "object": ", ".join([t["name"] for t in p["Tags"]["multi_select"]]),
            "date": p["Datum"]["date"]["start"] if p["Datum"]["date"] else "",
            "hours": p["Stunden (in h)"]["number"] or 0,
            "rate": hourly_rate,
        })

    # Alle Zeilen + Gesamtsumme zurückgeben
    context_json["results"] = simplified_results
    context_json["total_sum"] = sum(i["hours"] * i["rate"] for i in simplified_results)
    return context_json