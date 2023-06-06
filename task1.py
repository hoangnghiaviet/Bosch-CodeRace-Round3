import pandas as pd
import xml.etree.ElementTree as ET
import json

ns = {
    "reqif": "http://www.omg.org/spec/ReqIF/20110401/reqif.xsd",
    "xsi": "http://www.w3.org/2001/XMLSchema-instance"
}

ELEMENT_NAMESPACE = '{http://www.omg.org/spec/ReqIF/20110401/reqif.xsd}'
ELEMENT_NAMESPACE_DIV = '{http://www.w3.org/1999/xhtml}'

Sample_Object = {
    "Attribute Type": "Attribute Type",
    "Status": "Status",
    "ReqIF.ForeignID": "Identifier",
    "Safety Classification": "Safety Classification",
    "CRQ": "CRQ",
    "ReqIF.Text": "ReqIF.Text",
    "ReqIF.Name": "Title",
    "ReqIF.ChapterName": "ReqIF.Text",
    "Verification Criteria": "Verification Criteria",
    "ReqIF.ForeignCreatedOn": "Created On",
    "ReqIF.Description": "Description",
    "VAR_FUNC_SYS": "VAR_FUNC_SYS",
    "Allocation": "Allocation",
    "ReqIF.ForeignModifiedOn": "Modified On",
    "ReqIF.ForeignModifiedBy": "Contributor" ,
    "ReqIF.ForeignCreatedBy": "Creator",
    "Artifact Format": "Artifact Format"
}

originSchema = {
    "Identifier": "Identifier",
    "Title": "Title"
}

def checkAttributeType(identifier,root):
    """Check the type of attribute based on the identifier"""
    for element in root.iter(ELEMENT_NAMESPACE+'SPEC-OBJECT-TYPE'):
        if element.attrib['IDENTIFIER'] == identifier:
            return element.attrib['LONG-NAME']
def getObjectType(spec,root):
    """Get the object type for each SPEC-OBJECT"""
    attribute_type = ''
    for element in spec.iter(ELEMENT_NAMESPACE+'SPEC-OBJECT-TYPE-REF'):
        attribute_type = checkAttributeType(element.text,root)
    return attribute_type

def checkAttributeDateType(identifier,root):
    """Check the attribute date type based on the identifier"""
    for element in root.iter(ELEMENT_NAMESPACE+'ATTRIBUTE-DEFINITION-DATE'):
        if element.attrib['IDENTIFIER'] == identifier:
            return element.attrib['LONG-NAME'] 
def getObjectAttributeDate(spec,root,dict):
    """Get the attribute date values for each SPEC-OBJECT"""
    for element1, element2 in zip(spec.iter(ELEMENT_NAMESPACE+'ATTRIBUTE-VALUE-DATE'),spec.iter(ELEMENT_NAMESPACE+'ATTRIBUTE-DEFINITION-DATE-REF')):
        identifier = element2.text
        attribute_name = Sample_Object[f'{checkAttributeDateType(identifier,root)}']
        dict[f'{attribute_name}'] = element1.attrib['THE-VALUE']

def checkAttributeStringType(identifier,root):
    """Check the attribute string type based on the identifier"""
    for element in root.iter(ELEMENT_NAMESPACE+'ATTRIBUTE-DEFINITION-STRING'):
        if element.attrib['IDENTIFIER'] == identifier:
            return element.attrib['LONG-NAME']
def getObjectAttributeString(spec,root,dict):
    """Get the attribute string values for each SPEC-OBJECT"""
    for element1, element2 in zip(spec.iter(ELEMENT_NAMESPACE+'ATTRIBUTE-VALUE-STRING'),spec.iter(ELEMENT_NAMESPACE+'ATTRIBUTE-DEFINITION-STRING-REF')):
        identifier = element2.text
        attribute_name = Sample_Object[f'{checkAttributeStringType(identifier,root)}']
        if checkAttributeStringType(identifier,root) == "ReqIF.ForeignID":
            dict[f'{attribute_name}'] = int(element1.attrib['THE-VALUE'])
        else:
            dict[f'{attribute_name}'] = element1.attrib['THE-VALUE']

def checkAttributeEnumerationType(identifier,root):
    """Check the attribute enumeration type based on the identifier"""
    for element in root.iter(ELEMENT_NAMESPACE+'ATTRIBUTE-DEFINITION-ENUMERATION'):
        if element.attrib['IDENTIFIER'] == identifier:
            return element.attrib['LONG-NAME']
def getAttributeEnumerationValue(identifier,root):
    """Get the value of an attribute enumeration based on the identifier"""
    for element in root.iter(ELEMENT_NAMESPACE+'ENUM-VALUE'):
        if element.attrib['IDENTIFIER'] == identifier:
            return element.attrib['LONG-NAME']
def getObjectAttributeEnumeration(spec,root,dict):
    """Get the attribute enumeration values for each SPEC-OBJECT"""
    for element1, element2 in zip(spec.iter(ELEMENT_NAMESPACE+'ATTRIBUTE-DEFINITION-ENUMERATION-REF'),spec.iter(ELEMENT_NAMESPACE+'ENUM-VALUE-REF')):
        attribute_name = Sample_Object[f'{checkAttributeEnumerationType(element1.text,root)}']
        dict[f'{attribute_name}'] = getAttributeEnumerationValue(element2.text,root)

def checkAttributeXHTMLType(identifier,root):
    """Check the attribute XHTML type based on the identifier"""
    for element in root.iter(ELEMENT_NAMESPACE+'ATTRIBUTE-DEFINITION-XHTML'):
        if element.attrib['IDENTIFIER'] == identifier:
            return element.attrib['LONG-NAME']
def getObjectAttributeXHTML(spec,root,dict):
    """Get the attribute XHTML values for each SPEC-OBJECT"""
    for element1, element2 in zip(spec.iter(ELEMENT_NAMESPACE_DIV+'div'),spec.iter(ELEMENT_NAMESPACE+'ATTRIBUTE-DEFINITION-XHTML-REF')):
        identifier = element2.text
        attribute_name = Sample_Object[f'{checkAttributeXHTMLType(identifier,root)}']
        dict[f'{attribute_name}'] = ET.tostring(element1, encoding='unicode')

def getObjectValues(spec,root,dict):
    """Get all the attribute values for each SPEC-OBJECT"""
    # Get attribute date
    getObjectAttributeDate(spec,root,dict)
    # Get attribute string
    getObjectAttributeString(spec,root,dict)
    # Get attribute enumeration
    getObjectAttributeEnumeration(spec,root,dict)
    # Get attribute XHTML
    getObjectAttributeXHTML(spec,root,dict)

def findSpec(identifier,root):
    """Find a SPEC-OBJECT based on the identifier"""
    for element in root.iter(ELEMENT_NAMESPACE+'SPEC-OBJECT'):
        if element.attrib['IDENTIFIER'] == identifier:
            return element

def getObjects(root):
    """Get object information"""
    final_list_object = []
    spec_objects = []
    # Collocation SPEC-OBJECT
    object_order = root.find(".//reqif:SPECIFICATIONS", ns)
    for element in object_order.iter(ELEMENT_NAMESPACE+'SPEC-OBJECT-REF'):
        spec_objects.append(findSpec(element.text,root))
    for spec_object in spec_objects:
        object_dict = {}
        # Get type of objects
        object_dict["Attribute Type"] = getObjectType(spec_object,root)
        # Get values of objects
        getObjectValues(spec_object,root,object_dict)
        final_list_object.append(object_dict)
    return final_list_object

def readAttributeMapping(file_path,sheet_name,list):
    """Processing attribute mapping follow config file"""
    config_info = pd.read_excel(file_path,sheet_name=sheet_name)
    for spec in list:
        for index , row in config_info.iterrows():
            old_attribute_name = row['Attribute Name']
            new_attribute_name = row['New Attribute Name']
            if old_attribute_name != new_attribute_name:
                originSchema[old_attribute_name] = new_attribute_name
            if old_attribute_name in spec:
                tmpValue = spec[f'{old_attribute_name}']
                del spec[f'{old_attribute_name}']
                spec[f'{new_attribute_name}'] =tmpValue
    return list

def readValueMapping(file_path,sheet_name,list):
    """Processing value mapping follow config file"""
    config_info = pd.read_excel(file_path,sheet_name=sheet_name)
    for spec in list:
        for index, row in config_info.iterrows():
            attribute_name = row['Attribute Name']
            old_value = row['Old Value']
            new_value = row['New Value']
            if attribute_name in spec:
                if str(old_value) == str(spec[attribute_name]):
                    spec[attribute_name] = new_value
    return list

def objectOption(list):
    """Return obbject option"""
    return list

def stringOption(list):
    """Return String option follow config file"""
    attribiteNeed = originSchema["Title"]
    newList = []
    for spec in list:
        newList.append(spec[attribiteNeed])
    return newList

def intOption(list):
    """Return Integer option follow config file"""
    attribiteNeed = originSchema["Identifier"]
    newList = []
    for spec in list: 
        newList.append(spec[attribiteNeed])
    return newList

def ArrayMapping(file_path,sheet_name,list):
    """Processing array mapping follow config file"""
    config_info = pd.read_excel(file_path,sheet_name=sheet_name)
    for index,row in config_info.iterrows():
        artifact_type = row["Artifact Type"]
        if artifact_type == "Object":
            return objectOption(list)
        elif artifact_type == "String":
            return stringOption(list)
        elif artifact_type == "Integer":
            return intOption(list)

def readReqifFile(file_path):
    """Read a ReqIF file and extract relevant information."""
    result = {}
    tree = ET.parse(file_path)  
    root = tree.getroot()
    result["Module Name"] = root.find(".//reqif:SPECIFICATION",ns).attrib["LONG-NAME"]
    result["Module Type"] = root.find(".//reqif:SPECIFICATION-TYPE",ns).attrib["LONG-NAME"] 
    fileConfig = 'config.xlsx'
    listAfterAttributeMapping = readAttributeMapping(fileConfig,"AttributeMapping",getObjects(root))
    listAfterValueMapping = readValueMapping(fileConfig,"ValueMapping",listAfterAttributeMapping)
    result["List Artifact Info"] = ArrayMapping(fileConfig,"ArrayMapping",listAfterValueMapping)
    return result

if __name__ == "__main__":        
    file_path = 'Requirements.reqif'
    spec_objects = readReqifFile(file_path)
    filename = 'Output/data.json'
    with open(filename, 'w') as file:
        json.dump(spec_objects, file, indent=4)
