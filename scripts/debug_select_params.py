"""
Debug script to inspect selectDAT parameters
"""

def inspect_select_dat():
    """Inspect the selectDAT to see what parameters it has"""

    select_dat = op('/project1/hydra_system/code/CodeManager/select2')

    if not select_dat:
        print("ERROR: Could not find select2")
        return

    print(f"\n=== INSPECTING: {select_dat.path} ===")
    print(f"Type: {select_dat.OPType}")
    print(f"\nAll parameters:")

    # Show all parameters
    for par in select_dat.pars():
        # Skip internal parameters
        if not par.name.startswith('__'):
            val = par.eval()
            print(f"  {par.name}: {val} ({par.label})")

    print(f"\nInputs: {len(select_dat.inputs)}")
    for i, inp in enumerate(select_dat.inputs):
        if inp:
            print(f"  Input {i}: {inp.path}")

    print(f"\nOutputs: {len(select_dat.outputs)}")
    for i, out in enumerate(select_dat.outputs):
        if out:
            print(f"  Output {i}: {out.path}")

    print(f"\nTags: {select_dat.tags}")

# Run the inspection
inspect_select_dat()
