# ExternalFiles Callbacks
#
# Available callbacks:
#
# onPreSave(info) - Called before saving a component
#   Return False to abort the save
#
# onPostSave(info) - Called after saving a component
#
# The info dictionary contains:
#   'comp': The component being saved
#   'path': The save path
#   'isNew': Whether this is a new externalization
#   'version': Current version of the component
#   'timestamp': Current timestamp
#   'ownerComp': The ExternalFiles component


def onPreSave(info):
    """
    Called before saving a component.
    Return False to abort the save operation.
    """
    comp = info["comp"]
    print(f"About to save {comp.name} to {info['path']}")

    # Example: Unlock nodes for saving
    for child in comp.findChildren(tags=["tempLock"]):
        child.lock = False

    return True  # Continue with save


def onPostSave(info):
    """
    Called after saving a component.
    """
    comp = info["comp"]
    print(f"Successfully saved {comp.name}")

    # Example: Re-lock nodes after saving
    for child in comp.findChildren(tags=["tempLock"]):
        child.lock = True
