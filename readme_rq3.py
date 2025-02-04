import json
from pathlib import Path

def generate_rq3_tables(rq_number=3, output_dir="tables"):

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
        "### RESULTS FOR RQ3: How do projects adopt versioning? (Distribution of Releases)",
        "",
        "| Releases    | ESCAPE | PANOSC | LSRI | ENVRI | RSD |",
        "|-------------|--------|--------|-------|-----|-----|"
    ]

    table2 = [
        "\n### RESULTS FOR RQ3: How do projects adopt versioning? (Types of versioning)}",
        "",
        "| Type of Release | ESCAPE | PANOSC | LSRI | ENVRI | RSD |",
        "|-------------|--------|--------|-------|-----|-----|"
    ]

    release_data = {}
    versioning_data = {}
    
    for cluster in clusters:
        if cluster in data:
            rq31 = data[cluster]["rq3-1"]
            release_data[cluster] = {
                "releases": rq31["releases"],
                "consistency": rq31["consistency"]
            }
            
            rq32 = data[cluster]["rq3-2"]
            versioning_data[cluster] = {
                "semantic": rq32["semantic"],
                "calendar": rq32["calendar"],
                "alphanumeric": rq32["Alphanumeric"],
                "other": rq32["other"]
            }

    # Table 1
    table1.append(
        f"| Releases | {release_data['escape']['releases']:.2f}% | "
        f"{release_data['panosc']['releases']:.2f}% | "
        f"{release_data['lsri']['releases']:.2f}% | "
        f"{release_data['envri']['releases']:.2f}% | "
        f"{release_data['rsd']['releases']:.2f}% |"
    )
    
    table1.append(
        f"| Consistent Version Naming Scheme | {release_data['escape']['consistency']:.2f}% | "
        f"{release_data['panosc']['consistency']:.2f}% | "
        f"{release_data['lsri']['consistency']:.2f}% | "
        f"{release_data['envri']['consistency']:.2f}% | "
        f"{release_data['rsd']['consistency']:.2f}% |"
    )

    # Table 2
    for version_type in ["semantic", "calendar", "alphanumeric", "other"]:
        row = f"| {version_type.capitalize()} | "
        for cluster in ["escape", "panosc", "lsri", "envri", "rsd"]:
            value = versioning_data[cluster][version_type]
            row += f"{value:.2f}% | "
        table2.append(row)

    full_markdown = "\n".join(table1) + "\n" + "\n".join(table2)

    output_file = output_path / f"results_rq{rq_number}.md"
    with open(output_file, 'w') as f:
        f.write(full_markdown)
    
    print(f"RQ3 tables saved to: {output_file}")

if __name__ == "__main__":
    generate_rq3_tables()