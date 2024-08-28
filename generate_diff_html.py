import sys
import json
from datetime import datetime
from deepdiff import DeepDiff

def format_diff(diff):
    """Format the differences into a markdown string."""
    markdown_diff = []


    if 'dictionary_item_added' in diff:
        markdown_diff.append("### Added:")
        for item in diff['dictionary_item_added']:
            markdown_diff.append(f"- **{item}**: {json.dumps(diff['dictionary_item_added'][item], indent=4)}")

    if 'dictionary_item_removed' in diff:
        markdown_diff.append("### Removed:")
        for item in diff['dictionary_item_removed']:
            markdown_diff.append(f"- **{item}**: {json.dumps(diff['dictionary_item_removed'][item], indent=4)}")

    if 'values_changed' in diff:
        markdown_diff.append("### Changed:")
        for item in diff['values_changed']:
            markdown_diff.append(f"- **{item}**: Changed from `{diff['values_changed'][item]['old_value']}` to `{diff['values_changed'][item]['new_value']}`")

    if 'iterable_item_added' in diff:
        markdown_diff.append("### List Items Added:")
        for item in diff['iterable_item_added']:
            markdown_diff.append(f"- **{item}**: {json.dumps(diff['iterable_item_added'][item], indent=4)}")

    if 'iterable_item_removed' in diff:
        markdown_diff.append("### List Items Removed:")
        for item in diff['iterable_item_removed']:
            markdown_diff.append(f"- **{item}**: {json.dumps(diff['iterable_item_removed'][item], indent=4)}")

    return "\n".join(markdown_diff)

def generate_diff_html(previous_json_file, current_json_file):
    # Load the previous and current JSON data
    with open(previous_json_file, 'r') as f:
        previous_data = json.load(f)

    with open(current_json_file, 'r') as f:
        current_data = json.load(f)

    # Compute the differences
    diff = DeepDiff(previous_data, current_data, ignore_order=True, verbose_level=2)

    current_date_nice = datetime.now().strftime("%Y-%m-%d")
    html_content = f"""
        <h2>TCB Change Log - {current_date_nice}</h1>
    """

    if not diff:
        html_content += "<p>No changes detected.</p>"
    else:
        markdown_diff = format_diff(diff)
        html_content += "<pre>" + markdown_diff + "</pre>"

    # Write the HTML content to the output file
    print(html_content)

if __name__ == "__main__":
    generate_diff_html(sys.argv[1], sys.argv[2])