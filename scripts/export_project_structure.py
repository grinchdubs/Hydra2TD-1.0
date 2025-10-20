"""
TouchDesigner Project Structure Exporter
Exports the complete operator hierarchy and connections to a Markdown document
"""

import datetime
import os

def export_project_structure(output_path=None):
    """
    Export the current TouchDesigner project structure to a Markdown file.

    Args:
        output_path: Optional path to save the markdown file.
                    Defaults to documentation/PROJECT_STRUCTURE.md
    """

    # Default output path
    if output_path is None:
        project_root = "C:/Users/cuban/HydraToTD"
        output_path = os.path.join(project_root, "documentation", "PROJECT_STRUCTURE.md")

    # Ensure the directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Start building the markdown content
    lines = []
    lines.append("# TouchDesigner Project Structure")
    lines.append("")
    lines.append(f"**Generated:** {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append(f"**Project File:** {project.name}")
    lines.append("")
    lines.append("---")
    lines.append("")

    # Get project statistics
    stats = get_project_stats(root)
    lines.append("## Project Statistics")
    lines.append("")
    for key, value in stats.items():
        lines.append(f"- **{key}:** {value}")
    lines.append("")
    lines.append("---")
    lines.append("")

    # Export the hierarchy
    lines.append("## Operator Hierarchy")
    lines.append("")

    # Traverse from root
    traverse_hierarchy(root, lines, indent=0)

    lines.append("")
    lines.append("---")
    lines.append("")

    # Export connections summary
    lines.append("## Connections Summary")
    lines.append("")

    connections = get_all_connections(root)
    if connections:
        for conn in connections:
            lines.append(f"- `{conn['source']}` → `{conn['target']}`")
    else:
        lines.append("*No connections found*")

    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("*End of project structure export*")

    # Write to file
    content = "\n".join(lines)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"✓ Project structure exported to: {output_path}")
    print(f"  Total operators: {stats.get('Total Operators', 0)}")
    print(f"  Total connections: {len(connections)}")

    return output_path


def traverse_hierarchy(op, lines, indent=0):
    """
    Recursively traverse the operator hierarchy and add to markdown lines.

    Args:
        op: The operator to process
        lines: List of markdown lines to append to
        indent: Current indentation level
    """

    # Create indentation
    indent_str = "  " * indent

    # Get operator info
    op_type = op.OPType
    op_path = op.path
    op_name = op.name

    # Format the line with operator info
    if indent == 0:
        # Root level
        lines.append(f"### `{op_path}` ({op_type})")
    else:
        # Child operators - use list format
        marker = "- "

        # Add operator type badge
        type_badge = f"**[{op_type}]**"

        # Check for connections
        connections_info = get_operator_connections(op)

        if connections_info:
            lines.append(f"{indent_str}{marker}`{op_name}` {type_badge} — {connections_info}")
        else:
            lines.append(f"{indent_str}{marker}`{op_name}` {type_badge}")

    # Process children if this is a component
    if hasattr(op, 'children'):
        children = op.children

        # Sort children by type and name for better readability
        children_sorted = sorted(children, key=lambda x: (x.OPType, x.name))

        for child in children_sorted:
            traverse_hierarchy(child, lines, indent + 1)


def get_operator_connections(op):
    """
    Get connection information for an operator.

    Args:
        op: The operator to analyze

    Returns:
        String describing connections, or empty string if none
    """
    conn_parts = []

    # Check inputs
    if hasattr(op, 'inputs'):
        inputs = [inp for inp in op.inputs if inp is not None]
        if inputs:
            input_names = [inp.name for inp in inputs]
            conn_parts.append(f"← {', '.join(input_names)}")

    # Check outputs
    if hasattr(op, 'outputs'):
        outputs = [out for out in op.outputs if out is not None]
        if outputs:
            # Count number of outputs
            conn_parts.append(f"→ {len(outputs)} output(s)")

    return " | ".join(conn_parts) if conn_parts else ""


def get_all_connections(root_op):
    """
    Get all connections in the project.

    Args:
        root_op: Root operator to start traversal

    Returns:
        List of connection dictionaries
    """
    connections = []

    def traverse(op):
        # Check this operator's inputs
        if hasattr(op, 'inputs'):
            for i, inp in enumerate(op.inputs):
                if inp is not None:
                    connections.append({
                        'source': inp.path,
                        'target': op.path,
                        'target_input': i
                    })

        # Traverse children
        if hasattr(op, 'children'):
            for child in op.children:
                traverse(child)

    traverse(root_op)
    return connections


def get_project_stats(root_op):
    """
    Calculate project statistics.

    Args:
        root_op: Root operator to analyze

    Returns:
        Dictionary of statistics
    """
    stats = {
        'Total Operators': 0,
        'Components (COMPs)': 0,
        'Textures (TOPs)': 0,
        'Channels (CHOPs)': 0,
        'Surfaces (SOPs)': 0,
        'Data (DATs)': 0,
        'Materials (MATs)': 0,
        'Other': 0
    }

    def count_recursive(op):
        stats['Total Operators'] += 1

        # Count by type
        op_type = op.OPType
        if 'COMP' in op_type or hasattr(op, 'children'):
            stats['Components (COMPs)'] += 1
        elif 'TOP' in op_type:
            stats['Textures (TOPs)'] += 1
        elif 'CHOP' in op_type:
            stats['Channels (CHOPs)'] += 1
        elif 'SOP' in op_type:
            stats['Surfaces (SOPs)'] += 1
        elif 'DAT' in op_type:
            stats['Data (DATs)'] += 1
        elif 'MAT' in op_type:
            stats['Materials (MATs)'] += 1
        else:
            stats['Other'] += 1

        # Recurse through children
        if hasattr(op, 'children'):
            for child in op.children:
                count_recursive(child)

    count_recursive(root_op)
    return stats


# Main execution function
def run_export(custom_path=None):
    """
    Main function to run the export.
    Can be called from TouchDesigner with optional custom output path.
    """
    try:
        output_file = export_project_structure(custom_path)
        return output_file
    except Exception as e:
        print(f"✗ Error during export: {str(e)}")
        import traceback
        traceback.print_exc()
        return None


# Quick execution shortcut
if __name__ == "__main__":
    run_export()
