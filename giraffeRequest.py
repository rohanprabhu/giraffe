
class GiraffeRequest:
    def __init__(self, mobile_identifier, body):
        self.mobile_identifier = mobile_identifier
        self.body = body
        self.split_body()

    def dump_request(self):
        return "Mobile Identifier: " + self.mobile_identifier + " | Body: " + self.body

    def split_body(self):
        try:
            parameters = self.body.split(' ', 2)
            self.title = parameters[0]
            self.amount = parameters[1]
            self.user = parameters[2]
            self.users = self.user.split(' ')
        except:
            raise ValueError("Error in parsing the body in GiraffeRequest")
