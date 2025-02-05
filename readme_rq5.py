import json
import os
from pathlib import Path

def generate_rq_table(rq_number, output_dir="tables"):
    script_dir = Path(__file__).parent
    base_dir = script_dir / "calculations"
    rq_dir = base_dir / f"rq{rq_number}"
    
    clusters = ["envri", "escape", "lsri", "panosc", "rsd"]
    
    table_headers = ["Citation Files", "ESCAPE", "PANOSC", "LSRI", "ENVRI", "RSD"]
    row_mapping = {
        "bib": ".bib",
        "cff": ".cff",
        "readme": "README.md",
        "total": "Citation"
    }

    data = {}
    for cluster in clusters:
        json_file = rq_dir / f"rq{rq_number}_results_{cluster}.json"
        try:
            with open(json_file, 'r') as f:
                cluster_data = json.load(f)[cluster]
                data[cluster] = {k: cluster_data.get(k, 0) for k in row_mapping}
        except FileNotFoundError:
            print(f"Error: Missing file {json_file}")
            continue
        except KeyError:
            print(f"Error: Invalid structure in {json_file}")
            continue

    markdown = [
        f"<table><thead><tr><td colspan='{len(table_headers)}'><b>RESULTS FOR RQ{rq_number}: What are the citation practices among the communities?</b></td></tr></thead>",
        "<tbody>",
        "<tr>" + "".join(f"<td>{h}</td>" for h in table_headers) + "</tr>"
    ]
    
    for json_key, display_name in row_mapping.items():
        row = [display_name]
        for cluster in clusters:  
            if cluster in data and json_key in data[cluster]:
                value = data[cluster][json_key]
                formatted = f"{value:.2f}%" if isinstance(value, float) else f"{value}%"
                row.append(formatted)
            else:
                row.append("N/A")
        markdown.append("<tr>" + "".join(f"<td>{cell}</td>" for cell in row) + "</tr>")
    
    markdown.append("</tbody></table>")
    
    output_path = script_dir / output_dir
    output_path.mkdir(exist_ok=True)
    output_file = output_path / f"results_rq{rq_number}.md"
    
    with open(output_file, 'w') as f:
        f.write("\n".join(markdown))
    
    print(f"Markdown table saved to {output_file}")

if __name__ == "__main__":
    generate_rq_table(5)