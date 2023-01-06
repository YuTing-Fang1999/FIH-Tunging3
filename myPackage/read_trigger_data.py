import xml.etree.ElementTree as ET
import os
from myPackage.Array_Parser import Array_Parser

def read_c7_trigger_data(key_config, project_path):
    xml_path = project_path + key_config["file_path"]

    tree = ET.parse(xml_path)
    root = tree.getroot()

    # 子節點與屬性
    mod_wnr24_aec_datas  =  root.findall(key_config["xml_node"])
    # hdr_aec_data 下面有多組 gain 的設定 (mod_wnr24_aec_data)
    # 每組mod_wnr24_aec_data分別有 aec_trigger 與 wnr24_rgn_data
    # 其中 aec_trigger 代表在甚麼樣的ISO光源下觸發
    # wnr24_rgn_data 代表所觸發的參數

    aec_trigger_datas = []
    for ele in mod_wnr24_aec_datas:
        data = []
        aec_trigger = ele.find("aec_trigger")
        data.append(aec_trigger.find("lux_idx_start").text)
        data.append(aec_trigger.find("lux_idx_end").text)
        data.append(aec_trigger.find("gain_start").text)
        data.append(aec_trigger.find("gain_end").text)
        aec_trigger_datas.append(data)

    return aec_trigger_datas

def read_c6_trigger_data(key_config, project_path):
    project_name = os.listdir(project_path+'/src')[0]
    # print(project_name)
    path = project_path + '/src/' + project_name + key_config["file_path"] + project_name + "_snapshot_cpp.h"
    # print(path)

    with open(path, 'r', encoding='cp1252') as f:
        text = f.read()

    main_node = Array_Parser(list(text))
    for i in key_config["main_node"]:
        main_node = main_node.get(i)
    
    aec_trigger_datas = []
    print(main_node.length())
    for i in range(main_node.length()):
        data = []
        data.append(''.join(main_node.get(i).get(key_config["trigger_node"]).get(2).text))
        data.append(''.join(main_node.get(i).get(key_config["trigger_node"]).get(1).text))
        data.append(''.join(main_node.get(i).get(key_config["trigger_node"]).get(0).text))
        data.append(''.join(main_node.get(i).get(key_config["trigger_node"]).get(1).text))
        aec_trigger_datas.append(data)

    # print(''.join(main_node.reconstruct()))
    print(aec_trigger_datas)
    return aec_trigger_datas