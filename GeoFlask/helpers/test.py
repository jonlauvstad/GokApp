class Test:
    def __init__(self, prop, snop):
        self.prop = prop
        self.snop = snop
        self.fields = {
            "prop": lambda x: x.prop,
            "snop": lambda x: x.sayBoo()
        }

    def sayBoo(self):
        return "boo"

    def serialize_x_keys(self, keys):
        # dic = {}
        # for field in self.fields:
        #     if field not in keys:
        #         dic[field] = self.fields[field](self)
        # return dic
        return {key: value(self) for (key, value) in self.fields.items() if key not in keys}

test = Test("balle", "pung")

ser_all = test.serialize_x_keys([])
ser_prop = test.serialize_x_keys(["snop"])

print(ser_all, ser_prop, sep="\n")
