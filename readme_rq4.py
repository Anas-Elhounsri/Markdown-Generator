import json
from pathlib import Path

def generate_rq4_tables(rq_number=4, output_dir="tables"):

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    base_dir = Path("calculations")
    rq_dir = base_dir / f"rq{rq_number}"
    clusters = ["envri", "escape", "lsri", "panosc", "rsd"]
    
    data = {}
    for cluster in clusters:
        json_file = rq_dir / f"rq{rq_number}_results_{cluster}.json"
        try:
            with open(json_file, 'r') as f:
                data[cluster] = json.load(f)[cluster]
        except FileNotFoundError:
            print(f"Error: Missing file {json_file}")
            continue

    table1 = [
        "### RESULTS FOR RQ4-1: How do communities describe their software (short vs long)}",
        "",
        "| Long vs Short Description     | ENVRI | ESCAPE | LSRI | PANOSC | RSD |",
        "|-------------|--------|--------|-------|-----|-----|"
    ]

    table2 = [
        "\n### RESULTS FOR RQ4-2: How do communities adopt licensing their projects?}",
        "",
        "| Licenses | ENVRI | ESCAPE | LSRI | PANOSC | RSD |",
        "|-----------------|--------|--------|-------|-----|-----|"
    ]

    table3 = [
        "\n### RESULTS FOR RQ4-3: How well documented are research projects?}}",
        "",
        "| Installation Instructions  | ENVRI | ESCAPE | LSRI | PANOSC | RSD |",
        "|-----------------|--------|--------|-------|-----|-----|"
    ]

    desc_data = {}
    spdx_data= {}
    inst_intruc = {}
    
    for cluster in clusters:
        if cluster in data:
            rq41 = data[cluster].get("rq4-1", {})
            desc_data[cluster] = {
                "long desc": rq41["long_desc"],
                "short desc": rq41["short_desc"],
                "None": rq41["None"]
            }
            
            rq42 = data[cluster]["rq4-2"]
            spdx_data[cluster] = {
                "spdx": rq42["spdx"],
                "other": rq42["other"],
                "no license": rq42["no_license"],
            }

            rq43 = data[cluster]["rq4-3"]
            inst_intruc[cluster] = {
                "requirements": rq43["requirements"],
                "installation": rq43["installation"],
                "documentation": rq43["documentation"],
            }

    # Table 1
    for desc_type in ["long desc", "short desc", "None"]:
        row = f"| {desc_type.capitalize()} | "
        for cluster in clusters:
            value = desc_data[cluster][desc_type]
            row += f"{value:.2f}% | "
        table1.append(row)

    # Table 2
    for spdx_type in ["spdx", "other", "no license"]:
        row = f"| {spdx_type.capitalize()} | "
        for cluster in clusters:
            value = spdx_data[cluster][spdx_type]
            row += f"{value:.2f}% | "
        table2.append(row)

    # Table 3
    for inst_intruc_type in ["requirements", "installation", "documentation"]:
        row = f"| {inst_intruc_type.capitalize()} | "
        for cluster in clusters:
            value = inst_intruc[cluster][inst_intruc_type]
            row += f"{value:.2f}% | "
        table3.append(row)

    full_markdown = "\n".join(table1) + "\n" + "\n".join(table2) + "\n".join(table3)

    output_file = output_path / f"results_rq{rq_number}.md"
    with open(output_file, 'w') as f:
        f.write(full_markdown)
    
    print(f"RQ4 tables saved to: {output_file}")

if __name__ == "__main__":
    generate_rq4_tables()