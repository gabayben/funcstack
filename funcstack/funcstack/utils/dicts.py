from typing import Any

def normalize_metadata(
    metadata: dict[str, Any] | list[dict[str, Any]],
    sources_count: int
) -> list[dict[str, Any]]:
    """
    Normalize the metadata input for a converter.

    Given all the possible value of the meta input for a converter (None, dictionary or list of dicts),
    makes sure to return a list of dictionaries of the correct length for the converter to use.

    :param metadata: the meta input of the converter, as-is
    :param sources_count: the number of sources the converter received
    :returns: a list of dictionaries of the make length as the sources list
    """
    if metadata is None:
        return [{}] * sources_count
    if isinstance(metadata, dict):
        return [metadata] * sources_count
    if isinstance(metadata, list):
        if sources_count != len(metadata):
            raise ValueError("The length of the metadata list must match the number of sources.")
        return metadata
    raise ValueError("metadata must be either None, a dictionary or a list of dictionaries.")
