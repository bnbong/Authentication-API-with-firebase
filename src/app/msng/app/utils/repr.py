def repr_create(class_name : str,table_list : list) -> str:
    return_str = class_name + "("

    for table in table_list[:len(table_list)-1]:
        return_str += table+"={self."+table+"},"

    if table_list[-1]:
        return_str += table_list[-1]+"={self."+table_list[-1]+"}"

    return_str += ")"
    return return_str