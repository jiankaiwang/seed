#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: jiankaiwang
"""

import numpy as np
from collections import OrderedDict

class ObjectDetectionStandard:
    """
    Desc: Input (1) a set of image, (2) Ground truth labeling, (3) infered 
        labeling, then output several object detection indexes, evaluating the 
        model performance.
    """
    
    def transfrom_coord(self, coord, coord_type="yxyx"):
        """
        INPUT:
            coord: [val, val, val, val]
            coord_type:
                @yxyx: [y1, x1, y2, x2]
                @yyxx: [y1, y2, x1, x2]
        
        OUTPUT: 
            return [x1, y1, x2, y2]
        """
        if coord_type == "yyxx":
            return [coord[2], coord[0], coord[3], coord[1]]
        else:
            # "yxyx"
            return [coord[1], coord[0], coord[3], coord[2]]
    
    def single_IOU(self, boxA, boxB):
        """
        INPUT:
            boxA: [x1, y1, x2, y2]
            boxB: [x1, y1, x2, y2]
        
        OUTPUT: float (percentage)
        
        EXAMPLE.1
        print(single_IOU([348, 680, 546, 850],[345, 679, 545, 847]))
        
        EXAMPLE.2
        test_coord = [(680, 348, 850, 546), [679, 345, 847, 545]]
        print(single_IOU(__transfrom_coord(test_coord[0]), __transfrom_coord(test_coord[1])))
        """
        
        # get intersection area
        x_i1 = max(boxA[0], boxB[0])
        y_i1 = max(boxA[1], boxB[1])
        x_i2 = min(boxA[2], boxB[2])
        y_i2 = min(boxA[3], boxB[3])
        interArea = max(0, x_i2 - x_i1 + 1) * max(0, y_i2 - y_i1 + 1)
        
        # get each area
        boxA_Area = (boxA[2] - boxA[0] + 1) * (boxA[3] - boxA[1] + 1)
        boxB_Area = (boxB[2] - boxB[0] + 1) * (boxB[3] - boxB[1] + 1)
        
        # IOU
        iou = float(interArea) / float(boxA_Area + boxB_Area - interArea)
        
        return iou        
    
    def compare(self, data_list=None, threshold=5e-1):
        """
        INPUT:
            see valid_check()
        
        OUTPUT:
            return 
            {
                average_IOU: float,
                total_labeling_count(Z): int, 
                meet_labeling_count(M): int, 
                loss_labeling_count(L): int,
                infer_true_but_wrong_count(O): int,
                sensitivity = recall (M / (M+L)): float,
                precision (M / (M+O)) : float,
                accuracy ((Z-O-L) / Z): float,
                f1-score (2M / (2M+O+L)): float
            }
        """
        if data_list == None:
            return 0., "Data does not exist."
        
        data_check, _ = self.valid_check(data_list)
        if not data_check:
            return 0., "Data check failed."
        
        tmp_overlap = 0   # union
        total_labeling_count = 0   # Z
        meet_labeling_count = 0   # M
        loss_labeling_count = 0   # L
        infer_true_but_wrong_count = 0   # O
        
        tmp_IOU_list = []
        
        for idx in range(len(data_list)):
            
            filename = data_list[idx]['file_name']
            label = data_list[idx]['label_list']
            infer = data_list[idx]['object_list']
            
            label_count = len(label)
            infer_count = len(infer)
            
            # create a mapping matrix
            mapping_matrix = np.full([label_count, infer_count], fill_value=0.)
            
            # calculate IOU matrix
            for inferidx in range(infer_count):
                for labelidx in range(label_count):
                    tmpIOU = self.single_IOU(label[labelidx]['obj_coord'], \
                                             infer[inferidx]['obj_coord'])
                    mapping_matrix[labelidx, inferidx] = tmpIOU
        
            # IOU as the standard to the same object
            mapping_res = mapping_matrix >= threshold
            tmp_IOU_list += list(mapping_matrix[mapping_res])
            
            # count each indexes
            label_list, infer_list = np.where(mapping_res == True)
            tmp_overlap = len(label_list)   # calculate overlapping Z
            
            for clsidx in range(len(label_list)):
                if label[label_list[clsidx]]['obj_class'] == \
                    infer[infer_list[clsidx]]['obj_class']:
                    meet_labeling_count += 1   # add M
                else:
                    infer_true_but_wrong_count += 1  # add O
            
            # add L
            loss_labeling_count += label_count - len(label_list)
            
            # add O
            if infer_count > len(infer_list):
                infer_true_but_wrong_count += infer_count - len(infer_list)
                
            # calculate Z
            total_labeling_count += label_count + infer_count - tmp_overlap
        
        #return filename, mapping_matrix
        result_list = OrderedDict()
        
        result_list['average_IOU'] = np.average(tmp_IOU_list)
        result_list['sensitivity'] = \
            float(meet_labeling_count) / float(meet_labeling_count + loss_labeling_count)
        result_list['precision'] = \
            float(meet_labeling_count) / float(meet_labeling_count + infer_true_but_wrong_count)
        result_list['accuracy'] = \
            float(total_labeling_count - infer_true_but_wrong_count - loss_labeling_count) / float(total_labeling_count)
        result_list['f1-score'] = \
            float(2 * meet_labeling_count) / float(2 * meet_labeling_count + infer_true_but_wrong_count + loss_labeling_count)
        result_list['Total (Z)'] = total_labeling_count
        result_list['TP (M)'] = meet_labeling_count
        result_list['FN (L)'] = loss_labeling_count
        result_list['FP (O)'] = infer_true_but_wrong_count
        
        return result_list
        
        
    def valid_check(self, data_list):
        """
        INPUT:
            data_list = [
                {
                    'file_name':'',
                    'label_list':[
                        {
                            'obj_class': str,
                            'obj_score': float,
                            'obj_coord': [x1,y1,x2,y2]
                        },
                        {},
                        ...
                    ],
                    'object_list':[
                        {
                            'obj_class': str,
                            'obj_score': float,
                            'obj_coord': [x1,y1,x2,y2]
                        },
                        {},
                        ...
                    ]
                },
                {},
                ...
            ]
        OUTPUT: (True/False, message)
        """
        necessary_key = ['file_name','label_list','object_list']
        necessary_info = ['obj_class','obj_score','obj_coord']
        
        if type(data_list) != type([]):
            return False, "Not a data list."
        
        for data in data_list:
            
            if type(data) != type({}):
                return False, "Result in data is not dict."
            
            input_key_list = list(data.keys())
            for key in necessary_key:
                if key not in input_key_list:
                    return False, "Lost either file_name, label_list or object_list."
                
            for obj in data['label_list']:
                
                if type(obj) != type({}):
                    return False, "Label data is not dict."
                
                for item in necessary_info:
                    if item not in list(obj.keys()):
                        return False, "Lost obj_class, obj_score or obj_coord in label data."
                
            for obj in data['object_list']:
                
                if type(obj) != type({}):
                    return False, "Object type is not dict."
                
                for item in necessary_info:
                    if item not in list(obj.keys()):
                        return False, "Lost obj_class, obj_score or obj_coord in object data."
        return True, "Data is validated."
                
            
        
    def __init__(self):
        pass
    




















