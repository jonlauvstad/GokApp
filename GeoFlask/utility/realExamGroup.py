class RealExamGroup:
    def __init__(self, exam_group_dics):
        name = exam_group_dics[0]['name']
        examId = exam_group_dics[0]['examId']
        for egd in exam_group_dics:
            if egd['name'] != name:
                raise ValueError("All names must be equal")
            if egd['examId'] != examId:
                raise ValueError("All examIDs must be equal")
        self.name = name
        self.examId = examId
        self.courseImplementationId = exam_group_dics[0]['courseImplementationId']
        self.courseImplementationCode = exam_group_dics[0]['courseImplementationCode']
        self.courseImplementationName = exam_group_dics[0]['courseImplementationName']
        self.participants = exam_group_dics
        self.partip_name_string = ", ".join([f"{item['firstName']} {item['lastName']}" for item in self.participants])

def make_groups(exam_group_dics):
    group_dic = {}
    for exd in exam_group_dics:
        if exd['name'] not in group_dic:
            group_dic[exd['name']] = [exd]
        else:
            group_dic[exd['name']].append(exd)
    return [RealExamGroup(value) for key, value in group_dic.items()]

