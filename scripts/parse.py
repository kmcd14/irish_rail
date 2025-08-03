import pandas as pd
import requests
import xml.etree.ElementTree as et

# Common namespace
NAMESPACE = {'ns': 'http://api.irishrail.ie/realtime/'}

def parse_xml_to_df(root, record_tag, field_map):
    """
    Converts XML to Pandas DataFrame based on a tag and field mapping.
    
    Args:
        root (ElementTree): Root XML element.
        record_tag (str): The XML tag for each record.
        field_map (dict): Mapping from desired column names to XML child tags.
    
    Returns:
        pd.DataFrame
    """
    records = []
    for record in root.findall(f'ns:{record_tag}', namespaces=NAMESPACE):
        row = {}
        for col_name, xml_tag in field_map.items():
            element = record.find(f'ns:{xml_tag}', namespaces=NAMESPACE)
            row[col_name] = element.text if element is not None else None
        records.append(row)
    return pd.DataFrame(records)