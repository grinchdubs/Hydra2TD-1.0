"""
Test script to verify source tracing works correctly
Run this in TouchDesigner to test the updated apply_now() function
"""

# Load the updated manual_triggers_fixed module
exec(open(r'C:/Users/cuban/HydraToTD/scripts/manual_triggers_fixed.py', encoding='utf-8').read())

def test_source_tracing():
    """Test that we can trace from CodeManager selectDAT to source textDAT"""

    print("\n" + "="*60)
    print("TESTING SOURCE TRACING")
    print("="*60)

    # Get the current scene code (selectDAT in CodeManager)
    scene_code = get_current_scene_code()

    if not scene_code:
        print("ERROR: Could not find current scene code")
        return False

    print(f"\n1. Current scene in CodeManager: {scene_code.path}")
    print(f"   Type: {scene_code.OPType}")

    # Trace to find the source
    source_dat = trace_to_source_dat(scene_code)

    print(f"\n2. Traced source DAT: {source_dat.path}")
    print(f"   Type: {source_dat.OPType}")

    # Check if source has SceneCode tag
    has_scene_code_tag = 'SceneCode' in source_dat.tags
    print(f"   Has 'SceneCode' tag: {has_scene_code_tag}")

    # Show the tracing path
    print(f"\n3. Tracing path (following inputs):")
    current = scene_code
    depth = 0
    while current:
        print(f"   {'  ' * depth}→ {current.path} [{current.OPType}]")

        # Check tags
        if current.tags:
            print(f"   {'  ' * depth}  Tags: {', '.join(current.tags)}")
            # Check specifically for SceneCode tag
            if 'SceneCode' in current.tags:
                print(f"   {'  ' * depth}  ✓ Found SceneCode tag!")
        else:
            print(f"   {'  ' * depth}  (no tags)")

        # Show inputs
        if current.inputs:
            print(f"   {'  ' * depth}  Inputs: {len(current.inputs)} input(s)")
        else:
            print(f"   {'  ' * depth}  (no inputs)")

        # For selectDAT, show dat parameter info
        if current.OPType == 'selectDAT':
            # Check the 'dat' parameter
            if hasattr(current.par, 'dat'):
                dat_path = current.par.dat.eval()
                print(f"   {'  ' * depth}  dat parameter: {dat_path}")

        # Move to next DAT in chain
        next_dat = None

        if current.OPType == 'selectDAT':
            # First try inputs
            if current.inputs and len(current.inputs) > 0:
                next_dat = current.inputs[0]
                print(f"   {'  ' * depth}  → Following input wire")

            # If no input, try dat parameter
            if not next_dat and hasattr(current.par, 'dat'):
                dat_path = current.par.dat.eval()
                if dat_path:
                    next_dat = op(dat_path)
                    print(f"   {'  ' * depth}  → Following dat parameter")

            if next_dat:
                current = next_dat
                depth += 1
            else:
                print(f"   {'  ' * depth}  (no connection found)")
                break
        elif current.inputs and len(current.inputs) > 0:
            current = current.inputs[0]
            depth += 1
        else:
            break

        if depth > 10:  # Safety limit
            print("   (stopping - depth limit reached)")
            break

    print(f"\n4. Results:")
    if source_dat != scene_code:
        print(f"   ✓ Successfully traced to different source")
        print(f"   ✓ READ from: {scene_code.path}")
        print(f"   ✓ WRITE to: {source_dat.path}")
        result = True
    else:
        print(f"   ℹ Source is same as CodeManager DAT")
        print(f"   ℹ Both READ and WRITE to: {scene_code.path}")
        result = True

    print("\n" + "="*60)
    print("TEST COMPLETE")
    print("="*60)

    return result


# Run the test
if __name__ == '__main__':
    test_source_tracing()
