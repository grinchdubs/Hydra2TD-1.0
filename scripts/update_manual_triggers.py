"""
Update the manual_triggers DAT in TouchDesigner with the latest fixed code
"""

def update_manual_triggers():
    """Update the manual_triggers DAT with the fixed source tracing code"""

    print("\n" + "="*60)
    print("UPDATING MANUAL TRIGGERS DAT")
    print("="*60)

    # Get the manual_triggers DAT
    triggers_dat = op('/project1/hydra_system/direct_param_controller/manual_triggers')

    if not triggers_dat:
        print("ERROR: Could not find manual_triggers DAT at:")
        print("  /project1/hydra_system/direct_param_controller/manual_triggers")
        return False

    print(f"\nFound DAT: {triggers_dat.path}")
    print(f"Type: {triggers_dat.OPType}")

    # Read the updated code from file
    script_path = r'C:/Users/cuban/HydraToTD/scripts/manual_triggers_fixed.py'

    try:
        with open(script_path, 'r', encoding='utf-8') as f:
            new_code = f.read()

        print(f"\nRead {len(new_code)} characters from: {script_path}")

    except Exception as e:
        print(f"ERROR: Could not read file: {e}")
        return False

    # Try to update the DAT
    try:
        # Check if locked
        if hasattr(triggers_dat.par, 'locked') and triggers_dat.par.locked.eval():
            print("  Unlocking DAT...")
            triggers_dat.par.locked = False

        # Check if file synced
        if hasattr(triggers_dat.par, 'syncfile') and triggers_dat.par.syncfile.eval():
            print("  Disabling file sync...")
            triggers_dat.par.syncfile = False

        # Write the new code
        triggers_dat.text = new_code

        print("\n✓ SUCCESS: Updated manual_triggers DAT")
        print(f"  DAT now has {len(triggers_dat.text)} characters")

        # Verify the functions are available
        print("\nVerifying functions...")
        if hasattr(triggers_dat.module, 'sync_now'):
            print("  ✓ sync_now found")
        else:
            print("  ✗ sync_now NOT FOUND")

        if hasattr(triggers_dat.module, 'apply_now'):
            print("  ✓ apply_now found")
        else:
            print("  ✗ apply_now NOT FOUND")

        if hasattr(triggers_dat.module, 'trace_to_source_dat'):
            print("  ✓ trace_to_source_dat found (NEW)")
        else:
            print("  ✗ trace_to_source_dat NOT FOUND")

        print("\n" + "="*60)
        print("UPDATE COMPLETE")
        print("="*60)
        print("\nYou can now use:")
        print("  op('/project1/hydra_system/direct_param_controller/button_helper').module.trigger_apply()")

        return True

    except Exception as e:
        print(f"\nERROR: Could not update DAT: {e}")
        return False

# Run the update
if __name__ == '__main__':
    update_manual_triggers()
