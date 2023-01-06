import xml.etree.ElementTree as ET
from myPackage.Array_Parser import Array_Parser
import os

def read_c7_param_value(key_config, project_path, trigger_idx):
    xml_path = project_path + key_config["file_path"]

    tree = ET.parse(xml_path)
    root = tree.getroot()

    # 子節點與屬性
    node  =  root.findall(key_config["xml_node"])

    param_value = []
    for i, ele in enumerate(node):
        if i==trigger_idx:
            rgn_data = ele.find(key_config["data_node"])
            for param_name in key_config['range_names']:
                parent = rgn_data.find(param_name+'_tab')
                if parent:
                    p = parent.find(param_name).text.split(' ') 
                    p = [float(x) for x in p]
                    
                else:
                    print(param_name)
                    parent = rgn_data.find(param_name)
                    p = parent.text.split(' ') 
                    p = [float(x) for x in p]

                # ASF 暫定64取1
                if param_name in ["layer_1_gain_positive_lut",
                                    "layer_1_gain_negative_lut",
                                ]:
                    p = [p[0]]
                
                # ABF 暫定2取1
                if param_name in ["noise_prsv_lo",
                                    "noise_prsv_hi"]:
                    p = [p[0]]

                # WNR 暫定2取1
                if param_name in ["denoise_weight_chroma"]:
                    p = [p[0],p[2]]

                param_value.append(p)
            break

    # converting 2d list into 1d
    param_value = sum(param_value, [])
    return param_value



def read_c6_param_value(key_config, project_path, trigger_idx):
    project_name = os.listdir(project_path+'/src')[0]
    # print(project_name)
    path = project_path + '/src/' + project_name + key_config["file_path"] + project_name + "_snapshot_cpp.h"

    with open(path, 'r', encoding='cp1252') as f:
        text = f.read()

    main_node = Array_Parser(list(text))
    for i in key_config["main_node"]:
        main_node = main_node.get(i)

    param_node = main_node.get(trigger_idx)

    param_value = []
    for param_idx in key_config["param_node"]:
        for i in range(param_node.get(param_idx).length()):
            param_value.append(float(''.join(param_node.get(param_idx).get(i).text)))

    print(param_value)
    return param_value


